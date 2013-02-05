# portfolios/managers.py
from django.db import models

from portfolioapp.apps.core import mixins

class PortfolioManager(models.Manager, mixins.ORMMixin):
    def detailed_view(self, user_id):
        """
        Returns a query that is used for the detailed list view with custom logic at the database
        """
        from django.db import connection

        # from https://docs.djangoproject.com/en/dev/topics/db/managers/#adding-extra-manager-methods
        cursor = connection.cursor()
        cursor.execute('''
            SELECT
                pp.id,
                pp.name,
                COALESCE(SUM(pt.quantity*pt.value), 0) as book_value
            FROM
                portfolios_portfolio pp
                LEFT JOIN portfolios_holding ph ON pp.id = ph.portfolio_id
                LEFT JOIN portfolios_transaction pt ON ph.id = pt.holding_id
            WHERE pp.user_id = %s
            GROUP BY pp.id
            ORDER BY pp.name''', [user_id])

        # the following maps the arbitrary values back to the original model and then some extra attributes such as total_quantity, total_cost etc
        # mentioned that there may be a potential performance hit somewhere
        portfolios = []
        for row in cursor.fetchall():
            portfolio = self.model(id=row[0], name=row[1])
            portfolio.book_value = row[2]
            portfolios.append(portfolio)

        return portfolios


class HoldingManager(models.Manager, mixins.ORMMixin):
    def detailed_view(self, portfolio_id):
        """
        Returns a query that is used for the detailed list view with custom logic at the database
        """
        from django.db import connection

        cursor = connection.cursor()
        cursor.execute('''
            SELECT
                ph.id,
                ph.name,
                ph.symbol,
                mm.acr,
                23.00 as last_price,
                COALESCE(SUM(pt.quantity), 0) as total_quantity,
                COALESCE(AVG(pt.value), 0) as avg_cost,
                COALESCE(MAX(pt.value), 0) as max_cost,
                COALESCE(MIN(pt.value), 0) as min_cost,
                COALESCE(SUM(pt.quantity * pt.value), 0) as book_value,
                (COALESCE(SUM(pt.quantity), 0) * 23.00) as market_value,
		COALESCE(SUM(pt.quantity) * 23.00 - SUM(pt.quantity * pt.value), 0) as net_gain_dollar,
		COALESCE((SUM(pt.quantity) * 23.00 - SUM(pt.quantity * pt.value)) / SUM(pt.quantity * pt.value) * 100, 0) as net_gain_percent
            FROM
                portfolios_holding ph
                LEFT JOIN portfolios_transaction pt ON ph.id = pt.holding_id
                INNER JOIN portfolios_portfolio pp ON pp.id = ph.portfolio_id
                INNER JOIN markets_market mm on ph.market_id = mm.id
            WHERE pp.id = %s
            GROUP BY ph.id, mm.acr
            ORDER BY ph.name''', [portfolio_id])

        holdings = []
        for row in cursor.fetchall():
            holding = self.model(id=row[0], name=row[1], symbol=row[2])
            holding.market_name = row[3]
            holding.last_price = row[4]
            holding.total_quantity = row[5]
            holding.avg_cost = row[6]
            holding.max_cost = row[7]
            holding.min_cost = row[8]
            holding.book_value = row[9]
            holding.market_value = row[10]
            holding.net_gain_dollar = row[11]
            holding.net_gain_percent = row[12]
            holdings.append(holding)

        return holdings