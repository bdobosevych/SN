from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from posts.service import PostService


@login_required(login_url='/users/login/')
def feed(request):
    if request.method == "GET":
        return render(
            request,
            'feed.html',
            {
                "posts": PostService.get_posts_for_user(request.user.username),
                "username": request.user.username
            }
        )
