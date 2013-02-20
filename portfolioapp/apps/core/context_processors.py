from portfolioapp.apps.profiles.forms import LoginForm

def global_login_form(request):
    login_form = LoginForm()
    return {'login_form': login_form}


def view_name(request):
    """
    Defines a variable that returns the name of the current view.  Useful for defining current navigation.  Used
    in conjunction with custom middleware ViewNameMiddleware
    """
    return {'view_name': request.session['view_name']}