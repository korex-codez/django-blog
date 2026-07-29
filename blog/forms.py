from django import forms
from django.contrib.auth.models import User

from .models import (
    Post,
    Comment,
    Profile,
    Newsletter,
    Contact,
)


# ==========================================
# CREATE / EDIT POST
# ==========================================

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            "title",
            "category",
            "content",
            "image",
            "featured",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter blog title"
                }
            ),

            "category": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 10,
                    "placeholder": "Write your blog..."
                }
            ),

            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "featured": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            ),
        }


# ==========================================
# COMMENTS
# ==========================================

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ["content"]

        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Write your comment..."
                }
            )
        }


# ==========================================
# USER UPDATE
# ==========================================

class UserUpdateForm(forms.ModelForm):

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    class Meta:
        model = User

        fields = [
            "username",
            "email",
        ]

        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            )
        }


# ==========================================
# PROFILE UPDATE
# ==========================================

class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile

        fields = [
            "image",
            "bio",
            "website",
        ]

        widgets = {

            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "bio": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Tell us about yourself..."
                }
            ),

            "website": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://example.com"
                }
            ),
        }


# ==========================================
# NEWSLETTER
# ==========================================

class NewsletterForm(forms.ModelForm):

    class Meta:
        model = Newsletter

        fields = [
            "email"
        ]

        widgets = {

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your email"
                }
            )

        }


# ==========================================
# CONTACT FORM
# ==========================================

class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact

        fields = [
            "name",
            "email",
            "subject",
            "message",
        ]

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Your Name"
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Your Email"
                }
            ),

            "subject": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Subject"
                }
            ),

            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 6,
                    "placeholder": "Write your message..."
                }
            ),

        }