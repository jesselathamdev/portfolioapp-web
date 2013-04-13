# portfolios/managers.py
from django.db import models

from portfolioapp.apps.core import mixins


class HoldingManager(models.Manager, mixins.ORMMixin):
    def summary_view(self, user_id, portfolio_id):
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
                COALESCE(market_value / NULLIF(SUM(market_value) OVER () + (SELECT SUM(c.amount) as cash_total FROM cash c WHERE c.user_id = %(user_id)s AND c.portfolio_id = %(portfolio_id)s), 0), 0.00) * 100 AS portfolio_makeup_percent
            FROM (
                SELECT
                    ph.id,
                    ms.name,
                    ms.symbol,
                    mm.acr,
                    ms.last_price,
                    ms.date_last_price_updated,
                    COALESCE(SUM(pt.quantity), 0.00) as total_quantity,
                    COALESCE(AVG(NULLIF(pt.value, 0.00)), 0) as avg_cost,
                    COALESCE(MAX(pt.value), 0.00) as max_cost,
                    COALESCE(MIN(NULLIF(pt.value, 0)), 0.00) as min_cost,
                    COALESCE(SUM(pt.quantity * pt.value), 0.00) as book_value,
                    (COALESCE(SUM(pt.quantity), 0.00) * ms.last_price) as market_value,
                    COALESCE(SUM(pt.quantity) * ms.last_price - SUM(pt.quantity * pt.value), 0.00) as net_gain_dollar,
                    COALESCE((SUM(pt.quantity) * ms.last_price - SUM(pt.quantity * pt.value)) / NULLIF(SUM(pt.quantity * pt.value), 0) * 100, 0.00) as net_gain_percent

                FROM
                    holdings ph
                    LEFT JOIN transactions pt ON ph.id = pt.holding_id
                    INNER JOIN portfolios pp ON pp.id = ph.portfolio_id
                    INNER JOIN stocks ms on ph.stock_id = ms.id
                    INNER JOIN markets mm on ms.market_id = mm.id
                WHERE
                    pp.id = %(portfolio_id)s AND
                    pp.user_id = %(user_id)s
                GROUP BY ph.id, ms.name, ms.symbol, mm.acr, ms.last_price, ms.date_last_price_updated
            ) as holdings
            ORDER BY LOWER(name)''', {'user_id': user_id, 'portfolio_id': portfolio_id})

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