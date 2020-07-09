from itertools import chain

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import PostForm
from .models import ProblemPost, GeneralPost


class PostCreateView(CreateView):
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
