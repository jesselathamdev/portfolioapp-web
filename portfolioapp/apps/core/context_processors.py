from portfolioapp.apps.profiles.forms import LoginForm

def global_login_form(request):
    login_form = LoginForm()
    return {'login_form': login_form}