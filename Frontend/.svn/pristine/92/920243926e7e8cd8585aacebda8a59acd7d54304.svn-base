CREATE VIEW v_usd_non_preserve AS
    SELECT
        t2.issuer_name,
        t2.prod_name,
        t2.currency,
        t2.tenor_desc,
        t2.expected_highest_yield,
        t3.max AS 1m_max,
        t3.avg AS 1m_avg
    FROM
        (SELECT
            MAX(expected_highest_yield) AS max, tenor_desc
        FROM
            t_product
        WHERE
            data_source = 'MN' AND status = '在售'
                AND currency = 'USD'
                AND preservable <> 'Y'
                AND DATE(update_time) = (SELECT
                    MAX(DATE(update_time))
                FROM
                    t_product)
        GROUP BY tenor_desc) AS t1,
        (SELECT
            *
        FROM
            t_product
        WHERE
            data_source = 'MN' AND status = '在售'
                AND currency = 'USD'
                AND preservable <> 'Y') AS t2,
        (SELECT
            MAX(expected_highest_yield) AS max,
                AVG(expected_highest_yield) AS avg,
                tenor_desc
        FROM
            t_product
        WHERE
            DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= STR_TO_DATE(start_date, '%Y%m%d')
                AND data_source = 'MN'
                AND currency = 'USD'
                AND preservable <> 'Y'
        GROUP BY tenor_desc) AS t3
    WHERE
        t1.max = t2.expected_highest_yield
            AND t1.tenor_desc = t2.tenor_desc
            AND t1.tenor_desc = t3.tenor_desc