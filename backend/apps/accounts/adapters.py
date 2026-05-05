"""
Allauth adapters — humara User model username use nahi karta, sirf email.
"""
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class AccountAdapter(DefaultAccountAdapter):
    def populate_username(self, request, user):
        """Username field disable hai; kuch mat karo."""
        return

    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=False)
        user.email = form.cleaned_data.get("email") or user.email
        if commit:
            user.save()
        return user


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        if not user.email and sociallogin.account.extra_data.get("email"):
            user.email = sociallogin.account.extra_data["email"]
        return user
