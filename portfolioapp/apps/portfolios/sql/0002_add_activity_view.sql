DROP VIEW IF EXISTS activity;

CREATE VIEW activity AS
WITH activity AS
	(SELECT
		pt.date_transacted,
		pt.type,
		ms.id AS stock_id,
		ms.name,
		ms.symbol,
		mm.acr,
		pt.quantity,
		pt.value,
		pt.commission,
		pt.comment,
		pp.user_id,
		pp.id as portfolio_id
	FROM
		transactions pt
		INNER JOIN holdings ph ON pt.holding_id = ph.id
		INNER JOIN stocks ms ON ph.stock_id = ms.id
		INNER JOIN markets mm ON ms.market_id = mm.id
		INNER JOIN portfolios pp ON ph.portfolio_id = pp.id
	UNION ALL
	SELECT
		date_created,
		CASE type
		    WHEN 0 THEN 10
		    WHEN 1 THEN 11
		END AS type,
		-1 AS stock_id,
		'Cash' AS name,
		'' AS symbol,
		'' AS acr,
		0.00 quantity,
		amount AS value,
		0.00 AS commission,
		comment,
		user_id,
		portfolio_id
	FROM
		cash)
SELECT row_number() OVER (ORDER BY date_transacted) AS id, *
	FROM activity;

-- GRANT SELECT ON activity TO portfolioapp;