# portfolios/admin.py
from django import forms
from django.contrib import admin
from .models import Portfolio

class PortfolioAdmin(admin.ModelAdmin):

    class Meta:
        model = Portfolio

    list_display = ('name', 'date_created', 'date_updated',)
    readonly_fields = ('date_created', 'date_updated',)
    fields = ('name', ('date_created', 'date_updated',),)


admin.site.register(Portfolio, PortfolioAdmin)