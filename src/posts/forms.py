from django import forms
from django.core.validators import ValidationError

from .models import GeneralPost, Comment


class PostForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))

    class Meta:
        model = GeneralPost
        fields = ('title', 'description', 'img', )

    def clean_description(self):
        desc = self.cleaned_data.get('description')
        if len(desc) < 10:
            raise ValidationError('Description too short')
        return desc


class CommentForm(forms.ModelForm):
    body = forms.CharField(label='', widget=forms.Textarea(
        attrs={'rows': 3, 'placeholder': 'Your comment here...'}))

    class Meta:
        model = Comment
        fields = ('body',)
