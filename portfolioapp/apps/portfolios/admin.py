# portfolios/admin.py
from django.contrib import admin
from .models import Portfolio, Holding, Transaction


class PortfolioAdmin(admin.ModelAdmin):
    class Meta:
        model = Portfolio

    list_display = ('name', 'date_created', 'date_updated',)
    readonly_fields = ('date_created', 'date_updated',)
    fields = ('user', 'name', ('date_created', 'date_updated',),)


class HoldingAdmin(admin.ModelAdmin):
    class Meta:
        model = Holding

    list_display = ('name', 'date_created', 'date_updated',)
    readonly_fields = ('date_created', 'date_updated',)
    fields = ('portfolio', 'name', 'market', 'symbol', ('date_created', 'date_updated',),)


class TransactionAdmin(admin.ModelAdmin):
    class Meta:
        model = Transaction

    list_display = ('holding', 'get_type', 'quantity', 'cost', 'date_transacted',)
    readonly_fields = ('date_created', 'date_updated',)
    fields = ('holding', 'type', 'quantity', 'cost', 'date_transacted', ('date_created', 'date_updated',),)

    # returns the friendly name of the select key/value pair so that it can be used in the admin column header
    def get_type(self, object):
        return '%s' % object.get_type_display()

    get_type.short_description = 'Type'


admin.site.register(Portfolio, PortfolioAdmin)
admin.site.register(Holding, HoldingAdmin)
admin.site.register(Transaction, TransactionAdmin)