# core/context_processors.py

from portfolioapp.apps.profiles.forms import LoginForm


def global_login_form(request):
    login_form = LoginForm()

    return {'login_form': login_form}


def base_template_selector(request):

    # check if the user object exists, and if so proceed to check if it is authenticated, else fall back to the
    # unauthenticated template suitable for a home page and other static files
    if request.user:
        if request.user.is_authenticated():
            return {'base_template': 'base_app_two_columns.html'}

    return {'base_template': 'base_static_one_column.html'}