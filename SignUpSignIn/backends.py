from django.contrib.auth.backends import BaseBackend
from .models import CustomUser


class CustomBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(username=username)
            if user.check_password(password):
                return user
            else:
                print("Password is incorrect")
        except CustomUser.DoesNotExist:
            print("User does not exist")
            return None

    def get_user(self, username):
        try:
            return CustomUser.objects.get(pk=username)
        except CustomUser.DoesNotExist:
            return None
