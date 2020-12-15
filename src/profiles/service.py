"""
profiles service
"""

from social.settings import DB, NEO4J


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

            # add neo4j relation
            NEO4J.run("MATCH (a {username:$follower}), (b {username:$user}) "
                      "CREATE (a)-[:follows]->(b)",
                      {'follower': follower_name, 'user': user_name})
            return True
        return False

    @staticmethod
    def unfollow_user(follower_name, user_name):
        """
        :param follower_name:
        :param user_name:
        :return: True if Updated, else False
        """
        if follower_name == user_name:
            return False

        user = ProfileService.get_profile(user_name)
        follower = ProfileService.get_profile(follower_name)
        if follower_name not in user['followers']:
            return True

        if user and follower:
            USERS.find_one_and_update(
                {"username": user_name},
                {"$pull": {"followers": follower_name}},
                upsert=True)

            USERS.find_one_and_update(
                {"username": follower_name},
                {"$pull": {"follows": user_name}},
                upsert=True)

            # delete neo4j relation
            NEO4J.run("MATCH (a {username:$follower})-[f:follows]->(b {username:$user}) DELETE f",
                      {'follower': follower_name, 'user': user_name})
            return True
        return False

    @staticmethod
    def get_all_profiles():
        """
        :return:
        """
        result = list(USERS.find({}))
        return result

    @staticmethod
    def get_distance(user_from, user_to):
        """
        get distance from one user to another
        :param user_from:
        :param user_to:
        :return: list of usernames from shortest path or empty list if:
         there is no path or > 10 nodes in path or both parameters are the same
        """

        distance = []

        if user_from != user_to:
            result = NEO4J.run("MATCH p = shortestPath((f:User)-[*..10]-(t:User)) "
                               "WHERE f.username=$user_from AND t.username=$user_to RETURN p",
                               {'user_from': user_from, 'user_to': user_to})

            if result.forward():
                for node in result.current[0].nodes:
                    distance.append(node['username'])
                distance.remove(user_from)
        return distance