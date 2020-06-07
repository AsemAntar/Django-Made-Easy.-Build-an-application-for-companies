from django.shortcuts import render
from django.http import HttpResponse
from .models import Profile


def profile(request):
    pass


def test_user(request):
    if request.user.is_authenticated:
        user = request.user
        profile = Profile.objects.get(user=user)
    else:
        profile = 'no profile'

    context = {
        'user': profile,
    }

    return render(request, 'profiles/test.html', context)
