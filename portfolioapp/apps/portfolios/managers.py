from django.db import models

class PortfolioManager(models.Manager):
    def detailed_view(self, user_id):
        """
        Returns ID, Name, Holding Count and Book Value for the detailed view of the portfolio, typically on list pages
        """
        from django.db import connection

        cursor = connection.cursor()
        cursor.execute('''
            SELECT pp.id, pp.name, COUNT(ph.id) as holding_count, COALESCE(SUM(pt.quantity*pt.price), 0) as book_value
                FROM portfolios_portfolio pp
                LEFT JOIN portfolios_holding ph ON pp.id = ph.portfolio_id
                LEFT JOIN portfolios_transaction pt ON ph.id = pt.holding_id
                WHERE pp.user_id = %s
                GROUP BY pp.id
                ORDER BY pp.name''', [user_id])

        portfolios = []
        for row in cursor.fetchall():
            portfolio = self.model(id=row[0], name=row[1])
            portfolio.holding_count = row[2]
            portfolio.book_value = row[3]
            portfolios.append(portfolio)

        return portfolios


class HoldingManager(models.Manager):
    def current_activity(self, user_id):
        # from https://docs.djangoproject.com/en/dev/topics/db/managers/#adding-extra-manager-methods
        from django.db import connection

        cursor = connection.cursor()
        cursor.execute('''
            SELECT ph.id, ph.name, ph.market, ph.symbol,
                  COALESCE(COUNT(pt.id), 0) as total_quantity,
                  COALESCE(SUM(pt.price), 0) as total_price,
                  (COALESCE(COUNT(pt.id), 0) * COALESCE(SUM(pt.price), 0)) as book_value
                FROM portfolios_holding ph
                LEFT JOIN portfolios_transaction pt ON ph.id = pt.holding_id
                INNER JOIN portfolios_portfolio pp ON pp.id = ph.portfolio_id
                WHERE pp.user_id = %s
                GROUP BY ph.id
                ORDER BY ph.name''', [user_id])

        # the following maps the arbitrary values back to the original model and then some extra attributes such as total_quantity, total_price etc
        # mentioned that there may be a potential performance hit somewhere
        holdings = []
        for row in cursor.fetchall():
            holding = self.model(id=row[0], name=row[1], market=row[2], symbol=row[3])
            holding.total_quantity = row[4]
            holding.total_price = row[5]
            holding.book_value = row[6]
            holdings.append(holding)

        return holdings