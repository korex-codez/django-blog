from django import forms
from .models import Post, Comment, Profile
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'category', 'content', 'image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "image",
            "bio",
        ]