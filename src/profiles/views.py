from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from posts.service import PostService
from profiles.service import ProfileService


@login_required
def view_profile(request, username):
    """
    :param request:
    :param username:
    :return:
    """
    user = ProfileService.get_profile(username)
    current = request.user.username == username
    is_following = request.user.username in user['followers']
    if request.method == "POST":
        if not current:
            if is_following:
                ProfileService.unfollow_user(
                    follower_name=request.user.username,
                    user_name=username
                )
            else:
                ProfileService.follow_user(
                    follower_name=request.user.username,
                    user_name=username
                )

    user = ProfileService.get_profile(username)
    is_following = request.user.username in user['followers']
    distance = ProfileService.get_distance(
        user_from=request.user.username,
        user_to=username
    )
    return render(
        request,
        'profile.html',
        {
            "user": user,
            "posts": PostService.get_posts_by_author(username),
            "current": current,
            "is_following": is_following,
            "distance": distance,
            "current_user": request.user.username,
        }
    )


@login_required
def view_users(request):
    """
    :param request:
    :return:
    """
    users = ProfileService.get_all_profiles()
    return render(
        request,
        'users.html',
        {
            "users": users,
            "current": request.user.username
        }
    )