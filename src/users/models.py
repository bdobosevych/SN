"""User model"""
from django.core.exceptions import ObjectDoesNotExist
from djongo.sql2mongo import SQLDecodeError
from django.contrib.auth.models import User
from neobolt.exceptions import DatabaseError
from py2neo import Node

from social.settings import DB, NEO4J

USERS = DB["auth_user"]


def create_user(username, password, email):
    """
    Creates user instance and tries to add it into database.
    Returns:
        user instance if added successfully,
        None otherwise.
    """

    try:
        found = USERS.find_one({"username": username})
        if found:
            return None
        # create instance
        user = User.objects.create_user(username=username, email=email, password=password)

        # save to mongo
        user.save()
        USERS.find_one_and_update(
            {"username": username},
            {"$set": {"followers": [], "follows": []}},
            upsert=True)

        # save to neo4j
        create_neo_user(username=username)

        return user
    except (SQLDecodeError, DatabaseError):
        return None


def get_by_username(username):
    """
    Returns:
        user instance if found,
        None otherwise.
    """
    try:
        return User.objects.get(username=username)
    except ObjectDoesNotExist:
        return None


def change_password(username, new_password):
    """
    Method to change user password.
    Returns:
        user instance if password was changed,
        None otherwise.
    """
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        return None
    user.set_password(new_password)
    try:
        user.save()
        return user
    except SQLDecodeError:
        return None


def create_neo_user(username):
    """
    add user to neo4j
    :param username:
    :return:
    """
    found = NEO4J.run("MATCH (u:User {username:$username}) "
                      "RETURN u", username=username)
    if found.forward():
        return None
    user = NEO4J.run("CREATE (u:User {username:$username}) "
                     "RETURN u", {'username': username}).current
    return user