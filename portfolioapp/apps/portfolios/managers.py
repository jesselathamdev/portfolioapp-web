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
            SELECT id,
                name,
                symbol,
                acr,
                last_price,
                date_last_price_updated,
                total_quantity,
                avg_cost,
                max_cost,
                min_cost,
                book_value,
                market_value,
                net_gain_dollar,
                net_gain_percent,
                market_value/sum(market_value) OVER () * 100 AS portfolio_makeup_percent
            FROM (
                SELECT
                    ph.id,
                    ms.name,
                    ms.symbol,
                    mm.acr,
                    ms.last_price,
                    ms.date_last_price_updated,
                    COALESCE(SUM(pt.quantity), 0) as total_quantity,
                    COALESCE(AVG(NULLIF(pt.value, 0)), 0) as avg_cost,
                    COALESCE(MAX(pt.value), 0) as max_cost,
                    COALESCE(MIN(NULLIF(pt.value, 0)), 0) as min_cost,
                    COALESCE(SUM(pt.quantity * pt.value), 0) as book_value,
                    (COALESCE(SUM(pt.quantity), 0) * ms.last_price) as market_value,
                    COALESCE(SUM(pt.quantity) * ms.last_price - SUM(pt.quantity * pt.value), 0) as net_gain_dollar,
                    COALESCE((SUM(pt.quantity) * ms.last_price - SUM(pt.quantity * pt.value)) / SUM(pt.quantity * pt.value) * 100, 0) as net_gain_percent

                FROM
                    portfolios_holding ph
                    LEFT JOIN portfolios_transaction pt ON ph.id = pt.holding_id
                    INNER JOIN portfolios_portfolio pp ON pp.id = ph.portfolio_id
                    INNER JOIN markets_stock ms on ph.stock_id = ms.id
                    INNER JOIN markets_market mm on ms.market_id = mm.id
                WHERE pp.id = %s
                GROUP BY ph.id, ms.name, ms.symbol, mm.acr, ms.last_price, ms.date_last_price_updated
            ) as holdings
            ORDER BY name''', [portfolio_id])

        holdings = []
        for row in cursor.fetchall():
            holding = self.model(id=row[0])
            holding.stock_name = row[1]
            holding.stock_symbol = row[2]
            holding.market_code = row[3]
            holding.last_price = row[4]
            holding.date_last_price_updated = row[5]
            holding.total_quantity = row[6]
            holding.avg_cost = row[7]
            holding.max_cost = row[8]
            holding.min_cost = row[9]
            holding.book_value = row[10]
            holding.market_value = row[11]
            holding.net_gain_dollar = row[12]
            holding.net_gain_percent = row[13]
            holding.portfolio_makeup_percent = row[14]
            holdings.append(holding)

        return holdings