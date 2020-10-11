from django.shortcuts import render

from posts.service import PostService
from profiles.service import ProfileService


def view_profile(request, username):
    """

    :param request:
    :param username:
    :return:
    """
    if request.method == "GET":
        user = ProfileService.get_profile(username)
        return render(
            request,
            'profile.html',
            {
                "user": user,
                "posts": PostService.get_posts_by_author(username),
                "current": request.user.username == username,
                "followers_c": len(user['followers']),
                "follows_c": len(user['follows']),
            }
        )
