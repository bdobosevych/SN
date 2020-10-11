"""
profiles service
"""
import datetime

from pymongo.errors import DuplicateKeyError

from social.settings import DB


USERS = DB["auth_user"]


class ProfileService:
    """
    profile service class
    """

    @staticmethod
    def get_profile(username):
        """
        get profile by username

        :param username: string
        :return: profile instance if found, else None
        """
        profile = USERS.find_one({'username': username})
        return profile

    @staticmethod
    def follow_user(follower_name, user_name):
        """

        :param follower_name:
        :param user_name:
        :return: True if Updated, else False
        """
        if follower_name == user_name:
            return False

        user = ProfileService.get_profile(user_name)
        follower = ProfileService.get_profile(follower_name)
        if follower_name in user['followers']:
            return True
        if user and follower:
            # add follower to user
            USERS.find_one_and_update(
                {"username": user_name},
                {"$push": {"followers": follower_name}},
                upsert=True)
            # add follows to follower
            USERS.find_one_and_update(
                {"username": follower_name},
                {"$push": {"follows": user_name}},
                upsert=True)
            return True
        return False
