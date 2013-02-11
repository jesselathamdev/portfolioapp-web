# admin/ajax.py
from django.template.loader import render_to_string

from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax

from .views import get_pagination_page

@dajaxice_register
def pagination(request, p):
    items = get_pagination_page(p)
    render = render_to_string('admin/markets/stocks/pagination_page.html', {'items': items})

    dajax = Dajax()
    dajax.assign('#pagination', 'innerHTML', render)
    return dajax.json()
