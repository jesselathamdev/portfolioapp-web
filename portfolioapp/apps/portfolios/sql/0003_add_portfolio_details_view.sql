DROP VIEW IF EXISTS portfolio_details;

CREATE VIEW portfolio_details AS

WITH portfolios AS
(SELECT
    pp.id,
    pp.user_id,
    pp.name,
    COUNT(DISTINCT ph.id) AS holding_count,
    SUM(COALESCE(pt.quantity, 0.00) * COALESCE(pt.value, 0.00)) AS book_value,
    SUM(COALESCE(pt.quantity, 0.00) * COALESCE(ms.last_price, 0.00)) AS market_value
FROM
    portfolios pp
    LEFT JOIN holdings ph ON ph.portfolio_id = pp.id
    LEFT JOIN transactions pt ON pt.holding_id = ph.id
    LEFT JOIN stocks ms ON ms.id = ph.stock_id
GROUP BY
    pp.user_id, pp.id, pp.name)

SELECT
    pp.id,
    pp.user_id,
    pp.name,
    pp.holding_count,
    ROUND(COALESCE(SUM(cc.amount), 0.00) + pp.book_value, 5) AS book_value,
    ROUND(COALESCE(SUM(cc.amount), 0.00) + pp.market_value, 5) AS market_value,
    ROUND((COALESCE(SUM(cc.amount), 0.00) + pp.market_value) - (COALESCE(SUM(cc.amount), 0.00) + pp.book_value), 5) AS net_gain_dollar,
    ROUND(COALESCE(((COALESCE(SUM(cc.amount), 0.00) + pp.market_value) - (COALESCE(SUM(cc.amount), 0.00) + pp.book_value)) / NULLIF(COALESCE(SUM(cc.amount), 0.00) + pp.book_value, 0.00), 0.00), 5) * 100 AS net_gain_percent
FROM
    portfolios pp
    LEFT JOIN cash cc ON cc.portfolio_id = pp.id
GROUP BY
    pp.id, pp.user_id, pp.name, pp.holding_count, pp.book_value, pp.market_value
ORDER BY
    LOWER(pp.name)

-- GRANT SELECT ON portfolio_details TO portfolioapp;