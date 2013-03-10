# cash/managers.py

from django.db import models
from django.db.models import Sum

class CashManager(models.Manager):
    def summary_view(self, user_id, portfolio_id):
        return self.filter(user_id=user_id, portfolio_id=portfolio_id).aggregate(total_amount=Sum('amount'))
