# portfolios/managers.py
from django.db import models

from portfolioapp.apps.core import mixins

class PortfolioManager(models.Manager, mixins.ORMMixin):
    def summary_view(self, user_id):
        """
        Returns a query that is used for the detailed list view with custom logic at the database
        """
        from django.db import connection

        # from https://docs.djangoproject.com/en/dev/topics/db/managers/#adding-extra-manager-methods
        cursor = connection.cursor()
        cursor.execute('''
            WITH portfolios AS
            (SELECT
                pp.id,
                pp.name,
                COUNT(DISTINCT ph.id) AS holding_count,
                SUM(COALESCE(pt.quantity, 0.00) * COALESCE(pt.value, 0.00)) AS book_value,
                SUM(COALESCE(pt.quantity, 0.00) * COALESCE(ms.last_price, 0.00)) AS market_value
            FROM
                portfolios_portfolio pp
                LEFT JOIN portfolios_holding ph ON ph.portfolio_id = pp.id
                LEFT JOIN portfolios_transaction pt ON pt.holding_id = ph.id
                LEFT JOIN markets_stock ms ON ms.id = ph.stock_id
            WHERE
                pp.user_id = 2
            GROUP BY
                pp.user_id, pp.id, pp.name)
            SELECT
                pp.id,
                pp.name,
                pp.holding_count,
                COALESCE(SUM(cc.amount), 0.00) + pp.book_value AS book_value,
                COALESCE(SUM(cc.amount), 0.00) + pp.market_value AS market_value,
                (COALESCE(SUM(cc.amount), 0.00) + pp.market_value) - (COALESCE(SUM(cc.amount), 0.00) + pp.book_value) AS net_gain_dollar,
                COALESCE(((COALESCE(SUM(cc.amount), 0.00) + pp.market_value) - (COALESCE(SUM(cc.amount), 0.00) + pp.book_value)) / NULLIF(COALESCE(SUM(cc.amount), 0.00) + pp.book_value, 0.00), 0.00) * 100 AS net_gain_percent
            FROM
                portfolios pp
                LEFT JOIN cash_cash cc ON cc.portfolio_id = pp.id
            GROUP BY
                pp.id, pp.name, pp.holding_count, pp.book_value, pp.market_value
            ORDER BY
                LOWER(pp.name)''', {'user_id': user_id})

        # the following maps the arbitrary values back to the original model and then some extra attributes such as total_quantity, total_cost etc
        # mentioned that there may be a potential performance hit somewhere
        portfolios = []
        for row in cursor.fetchall():
            portfolio = self.model(id=row[0], name=row[1])
            portfolio.holding_count = row[2]
            portfolio.book_value = row[3]
            portfolio.market_value = row[4]
            portfolio.net_gain_dollar = row[5]
            portfolio.net_gain_percent = row[6]
            portfolios.append(portfolio)

        return portfolios


    # def summary_view(self, user_id):
    #     from django.db import connection
    #
    #     cursor = connection.cursor()
    #     cursor.execute('''
    #         SELECT
    #             COALESCE(SUM(book_value), 0.00) as book_value,
    #             COALESCE(SUM(market_value), 0.00) as market_value,
    #             COALESCE(SUM(market_value) - SUM(book_value), 0.00) as net_gain_dollar
    #         FROM (
    #             SELECT
    #                 pp.id,
    #                 pp.name,
    #                 COALESCE(SUM(pt.quantity*pt.value), 0.00) as book_value,
    #                 (COALESCE(SUM(pt.quantity), 0.00) * ms.last_price) as market_value
    #             FROM
    #                 portfolios_portfolio pp
    #                 LEFT JOIN portfolios_holding ph ON pp.id = ph.portfolio_id
    #                 LEFT JOIN portfolios_transaction pt ON ph.id = pt.holding_id
    #                 LEFT JOIN markets_stock ms ON ph.stock_id = ms.id
    #             WHERE pp.user_id = %s
    #             GROUP BY pp.id, pp.name, ms.last_price
    #         ) as portfolios''', [user_id])
    #
    #     summary = {}
    #     for row in cursor.fetchall():
    #         summary['total_book_value'] = row[0]
    #         summary['total_market_value'] = row[1]
    #         summary['total_net_gain_dollar'] = row[2]
    #
    #     return summary


class HoldingManager(models.Manager, mixins.ORMMixin):
    def detailed_view(self, user_id, portfolio_id):
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
                COALESCE(market_value / NULLIF(SUM(market_value) OVER () + (SELECT SUM(c.amount) as cash_total FROM cash_cash c WHERE c.user_id = %(user_id)s AND c.portfolio_id = %(portfolio_id)s), 0), 0.00) * 100 AS portfolio_makeup_percent
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
                    portfolios_holding ph
                    LEFT JOIN portfolios_transaction pt ON ph.id = pt.holding_id
                    INNER JOIN portfolios_portfolio pp ON pp.id = ph.portfolio_id
                    INNER JOIN markets_stock ms on ph.stock_id = ms.id
                    INNER JOIN markets_market mm on ms.market_id = mm.id
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

    def summary_view(self, user_id, portfolio_id):
        """
        Returns a query that is used for the summary list view with custom logic at the database
        """
        from django.db import connection

        cursor = connection.cursor()
        cursor.execute('''
            SELECT
                SUM(book_value) as book_value,
                SUM(market_value) as market_value,
                SUM(net_gain_dollar) as net_gain_dollar
            FROM (
                SELECT
                    COALESCE(SUM(pt.quantity * pt.value), 0.00) as book_value,
                    (COALESCE(SUM(pt.quantity), 0.00) * ms.last_price) as market_value,
                    COALESCE(SUM(pt.quantity) * ms.last_price - SUM(pt.quantity * pt.value), 0.00) as net_gain_dollar
                FROM
                    portfolios_holding ph
                    LEFT JOIN portfolios_transaction pt ON ph.id = pt.holding_id
                    INNER JOIN portfolios_portfolio pp ON pp.id = ph.portfolio_id
                    INNER JOIN markets_stock ms on ph.stock_id = ms.id
                    INNER JOIN markets_market mm on ms.market_id = mm.id
                WHERE
                    pp.id = %(portfolio_id)s
                AND pp.user_id = %(user_id)s
                    GROUP BY ph.id, ms.last_price, ms.date_last_price_updated
                UNION ALL
                SELECT
                    SUM(amount) as book_value,
                    SUM(amount) as market_value,
                    0 as net_gain_dollar
                FROM
                    cash_cash c
                WHERE
                    c.user_id = %(user_id)s AND
                    c.portfolio_id = %(portfolio_id)s
            ) as holdings''', {'user_id': user_id, 'portfolio_id': portfolio_id})

        summary = {}
        for row in cursor.fetchall():
            summary['total_book_value'] = row[0]
            summary['total_market_value'] = row[1]
            summary['total_net_gain_dollar'] = row[2]

        return summary