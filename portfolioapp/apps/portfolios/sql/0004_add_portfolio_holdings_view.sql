DROP VIEW IF EXISTS portfolio_holdings;

CREATE VIEW portfolio_holdings AS

WITH portfolio_holdings AS (
SELECT
    ph.id,
    pp.id as portfolio_id,
    pp.user_id,
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
GROUP BY ph.id, pp.id, pp.user_id, ms.name, ms.symbol, mm.acr, ms.last_price, ms.date_last_price_updated)

SELECT
    id,
    portfolio_id,
    user_id,
    name as stock_name,
    symbol as stock_symbol,
    acr as market_code,
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
    COALESCE(market_value / NULLIF(SUM(market_value) OVER () + (SELECT SUM(c.amount) as cash_total FROM cash c WHERE c.user_id = user_id AND c.portfolio_id = portfolio_id), 0), 0.00) * 100 AS portfolio_makeup_percent
FROM
    portfolio_holdings
ORDER BY LOWER(name)

-- GRANT SELECT ON portfolio_holdings TO portfolioapp;