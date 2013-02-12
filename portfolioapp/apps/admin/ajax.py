# admin/ajax.py
from django.template.loader import render_to_string
from django.contrib.auth.decorators import user_passes_test

from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax

from portfolioapp.apps.core.decorators import is_admin
from .views import dajax_paged_stocks

@user_passes_test(is_admin)
@dajaxice_register
def paged_stocks(request, p):

    items = dajax_paged_stocks(p)
    render = render_to_string('admin/markets/stocks/dajax_paged_content.html', {'items': items})

    dajax = Dajax()
    dajax.assign('#pagination', 'innerHTML', render)
    return dajax.json()