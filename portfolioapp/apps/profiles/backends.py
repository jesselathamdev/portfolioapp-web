# profiles/backends.py

from .models import User


class Auth(object):
    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user

        except User.DoesNotExist:
            return None


    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            if user.is_active:
                return user

        except User.DoesNotExist:
            return None