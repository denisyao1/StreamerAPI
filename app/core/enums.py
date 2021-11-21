from enum import Enum


class TwitchUrlEnum(Enum):
    """
    Enum class of twitch API' urls
    """
    AUTH = 'https://id.twitch.tv/oauth2/token'
    USERS = 'https://api.twitch.tv/helix/users'
