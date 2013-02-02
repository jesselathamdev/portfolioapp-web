from django.db import models

class PortfolioManager(models.Manager):
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
                COALESCE(SUM(pt.quantity*pt.cost), 0) as book_value
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


class HoldingManager(models.Manager):
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
                ph.market,
                ph.symbol,
                COALESCE(SUM(pt.quantity), 0) as total_quantity,
                COALESCE(SUM(pt.cost), 0) as total_cost,
                COALESCE(AVG(pt.cost), 0) as avg_cost,
                COALESCE(MAX(pt.cost), 0) as max_cost,
                COALESCE(MIN(pt.cost), 0) as min_cost,
                (COALESCE(SUM(pt.quantity), 0) * COALESCE(SUM(pt.cost), 0)) as book_value,
                (SELECT 45.00) as last_price,
                (COALESCE(SUM(pt.quantity), 0) * (SELECT 45)) as market_value
            FROM
                portfolios_holding ph
                LEFT JOIN portfolios_transaction pt ON ph.id = pt.holding_id
                INNER JOIN portfolios_portfolio pp ON pp.id = ph.portfolio_id
            WHERE pp.id = %s
            GROUP BY ph.id
            ORDER BY ph.name''', [portfolio_id])

        holdings = []
        for row in cursor.fetchall():
            holding = self.model(id=row[0], name=row[1], market=row[2], symbol=row[3])
            holding.total_quantity = row[4]
            holding.total_cost = row[5]
            holding.avg_cost = row[6]
            holding.max_cost = row[7]
            holding.min_cost = row[8]
            holding.book_value = row[9]
            holding.last_price = row[10]
            holding.market_value = row[11]
            holdings.append(holding)

        return holdings