import json
from os import environ
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Tuple

import httpx

from ..core.enums import TwitchUrlEnum


class TwitchService:
    """
    Service Class use to get token and informations from Twitch API
    """
    client_id = environ.get('TWITCH_CLIENT_ID')
    client_secret = environ.get('TWITCH_CLIENT_SECRET')
    file_path = Path(__file__).resolve().parent.parent.joinpath('token.json')

    def __init__(self):
        self.access_token = ''
        self.expire_at = None

    @classmethod
    def get_token_from_platform(cls) -> Tuple[str, datetime]:
        """
        Get access token from Twitch API
        :return: access token and it's expiration datetime
        """
        params = {
            'client_id': cls.client_id,
            'client_secret': cls.client_secret,
            'grant_type': 'client_credentials',
            'scope': 'user_read'
        }
        r = httpx.post(TwitchUrlEnum.AUTH.value, params=params)
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
    def save_to_file(cls, value: dict) -> None:
        """
        Save access token and it's expiration date to a json file
        """
        with open(cls.file_path, 'w') as token_file:
            json.dump(value, token_file, indent=4)

    @classmethod
    def get_token_from_file(cls) -> Tuple[str, datetime]:
        """
        Get access token and it's expiration date from json file
        :return: access token and it's expiration datetime
        """
        with open(cls.file_path, 'r') as token_file:
            values = json.load(token_file)

        return values['access_token'], datetime.fromisoformat(values['expire_at'])

    @classmethod
    def get_token(cls) -> Tuple[str, datetime]:
        """
        Get access token and it's expiration date
        :return: access token and it's expiration datetime
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
        Retrieve user information from switch API
        :return: a dict of needed user informations
        """
        # get a valide access token
        if not self.access_token:
            self.access_token, self.expire_at = self.get_token()
        elif self.expire_at < datetime.now():
            self.access_token, self.expire_at = self.get_token_from_platform()

        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Client-Id': self.client_id
        }
        params = {'login': username}
        r = httpx.get(TwitchUrlEnum.USERS.value, params=params, headers=headers)
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
