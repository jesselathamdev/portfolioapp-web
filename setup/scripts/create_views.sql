DROP VIEW IF EXISTS portfolios_activity;

CREATE VIEW portfolios_activity AS
WITH activity AS 
	(SELECT		
		pt.date_transacted,
		pt.type,
		ms.name || ' (' || ms.symbol || ':' || mm.acr || ')' AS name,
		pt.quantity,
		pt.value,
		pt.commission,
		pt.comment, 
		pp.user_id,
		pp.id as portfolio_id                
	FROM
		portfolios_transaction pt
		INNER JOIN portfolios_holding ph ON pt.holding_id = ph.id
		INNER JOIN markets_stock ms ON ph.stock_id = ms.id
		INNER JOIN markets_market mm ON ms.market_id = mm.id
		INNER JOIN portfolios_portfolio pp ON ph.portfolio_id = pp.id
	UNION ALL
	SELECT
		date_created,
		CASE type
		    WHEN 0 THEN 10
		    WHEN 1 THEN 11
		END AS type,
		'Cash' AS name,
		0.00 quantity,
		amount AS value,
		0.00 as commission,
		comment,
		user_id,
		portfolio_id
	FROM
		cash_cash)
SELECT row_number() OVER (ORDER BY date_transacted) AS id, * 
	FROM activity;

GRANT SELECT ON portfolios_activity TO portfolioapp;