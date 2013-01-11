from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the Portfolio index page.")

def detail(request, portfolio_id):
    return HttpResponse("This is the details page for portfolio with id %s" % portfolio_id)
