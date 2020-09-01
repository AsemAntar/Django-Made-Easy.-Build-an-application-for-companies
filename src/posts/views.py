from itertools import chain

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from .forms import PostForm
from .models import ProblemPost, GeneralPost, Post, Like
from .mixins import FormUserRequiredMixin
from profiles.models import Profile


class ProblemDetailView(LoginRequiredMixin, DetailView):
    model = ProblemPost
    template_name = 'posts/detail.html'
    pk_url_kwarg = 'pk1'
    context_object_name = 'post'


class GeneralDetailPost(LoginRequiredMixin, DetailView):
    model = GeneralPost
    template_name = 'posts/detail.html'


class PostCreateView(FormUserRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'posts/board.html'
    success_url = reverse_lazy('posts:post_list')

    def get_context_data(self, **kwargs):
        qs1 = ProblemPost.objects.get_public()
        qs2 = GeneralPost.objects.all()
        qs = sorted(chain(qs1, qs2), reverse=True, key=lambda obj: obj.created)
        context = super().get_context_data(**kwargs)
        context["object_list"] = qs
        return context


def like_post(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id=post_id)

        if profile in post.liked.all():
            post.liked.remove(profile)
        else:
            post.liked.add(profile)

    like, created = Like.objects.get_or_create(user=profile, post_id=post_id)
    if not created:
        if Like.value == "Like":
            Like.value = "Unlike"
        else:
            Like.value = "Like"
    like.save()
    return redirect('posts:post_list')
