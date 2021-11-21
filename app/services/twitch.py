import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import httpx


class TwitchAPIService:
    client_id = os.environ.get('TWITCH_CLIENT_ID')
    client_secret = os.environ.get('TWITCH_CLIENT_SECRET')
    file_path = Path(__file__).resolve().parent.parent.joinpath('token.json')

    def __init__(self):
        self.access_token = ''
        self.expire_at = None
        self.filename = 'token.json'
        print(self.filename)

    @classmethod
    def get_token_from_platform(cls):
        url = 'https://id.twitch.tv/oauth2/token'
        params = {
            'client_id': cls.client_id,
            'client_secret': cls.client_secret,
            'grant_type': 'client_credentials',
            'scope': 'user_read'
        }
        r = httpx.post(url, params=params)
        if r.status_code == 200:
            access_token = r.json()['access_token']
            expires_in = r.json()['expires_in']
            expire_at = datetime.now() + timedelta(seconds=expires_in - 10)
            r_dict = {
                'access_token': access_token,
                'expire_at': expire_at.isoformat()
            }
            cls.save_to_file(r_dict)
            return access_token, expire_at
        else:
            raise Exception('Cannot get access to token from Twitch platform')

    @classmethod
    def save_to_file(cls, value: dict):
        print('file_path : ', cls.file_path)
        with open(cls.file_path, 'w') as token_file:
            json.dump(value, token_file, indent=4)

    @classmethod
    def get_token_from_file(cls):
        with open(cls.file_path, 'r') as token_file:
            values = json.load(token_file)

        return values['access_token'], datetime.fromisoformat(values['expire_at'])

    @classmethod
    def get_token(cls) -> tuple:
        """try to get token from file
            if not get it from server
        """
        if not cls.file_path.is_file():
            return cls.get_token_from_platform()
        else:
            access_token, expire_at = cls.get_token_from_file()
            if expire_at > datetime.now():
                access_token, expire_at = cls.get_token_from_platform()
        return access_token, expire_at

    def retrieve_user_info(self, username: str) -> Optional[dict]:
        """
        retrieve user information from switch platform
        """
        if not self.access_token:
            self.access_token, self.expire_at = self.get_token()
        elif self.expire_at < datetime.now():
            self.access_token, self.expire_at = self.get_token_from_platform()

        url = 'https://api.twitch.tv/helix/users'
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Client-Id': self.client_id
        }
        params = {'login': username}
        print()
        print('headers :', headers)
        r = httpx.get(url, params=params, headers=headers)
        if r.status_code == 200:
            if r.json().get('data'):
                return {
                    'platform': 'Twitch',
                    'username': r.json().get('data')[0].get('login'),
                    'profile_picture_url': r.json().get('data')[0].get('profile_image_url')
                }
            else:
                return None
        else:
            print('status_code : ', r.status_code)
            print(r.json())
            raise Exception('Unable to get user informations from twitch')
