"""
Post service
"""
import datetime

from pymongo.errors import DuplicateKeyError

from posts.models import Post
from social.settings import DB


POSTS = DB["posts_post"]
from cassandra.io.libevreactor import LibevConnection
from cassandra.cluster import Cluster



class PostService:
    """
    Post service class
    """

    @staticmethod
    def create_post(author, title, content):
        """

        :param author:
        :param title:
        :param content:
        :return:
        """
        cluster = Cluster()
        session = cluster.connect('Post')
        post = {
            "author": author,
            "title": title,
            "content": content,
            "date": datetime.datetime.utcnow(),
            "comments": []
        }
        post_found = POSTS.find_one({"author": author, "title": title})
        if post_found is not None:
            return post_found
        session.execute("INSERT INTO Post (author, title,content,date,comments) VALUES ", post)
        post = POSTS.insert_one(post)

        return post

    @staticmethod
    def add_comment(post_author, post_title, comment_author, comment):
        """

        :param post_author:
        :param post_title:
        :param comment_author:
        :param comment:
        :return:
        """
        post = POSTS.find_one({"author": post_author, "title": post_title})
        if post:
            print(post["comments"])
            POSTS.find_one_and_update(
                {"author": post_author, "title": post_title},
                {"$push": {"comments": {"author": comment_author, "comment": comment}}},
                upsert=True)
        print(post)

    @staticmethod
    def get_all_posts():
        result = POSTS.find()
        cluster = Cluster()
        session = cluster.connect('Post')
        return session.execute("Select * From Post")
