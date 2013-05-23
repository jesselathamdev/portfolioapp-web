# core/decorators.py


def is_admin(user):
    """
    decorator to check if the user is their admin flag set; used in conjunction with @user_passes_test
    """
    return True if not user.is_anonymous() and user.is_admin else False