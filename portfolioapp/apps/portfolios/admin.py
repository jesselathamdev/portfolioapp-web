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

    list_display = ('quantity', 'amount',)
    readonly_fields = ('date_created', 'date_updated',)
    fields = ('holding', 'quantity', 'amount', ('date_created', 'date_updated',),)

admin.site.register(Portfolio, PortfolioAdmin)
admin.site.register(Holding, HoldingAdmin)
admin.site.register(Transaction, TransactionAdmin)