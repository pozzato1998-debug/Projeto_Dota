WITH base_ti AS (

    SELECT
        p.match_id,
        p.radiant_win,
        pt.hero_id,
        pt.lado

    FROM partidas_ti AS p

    LEFT JOIN participacoes_ti AS pt
        ON pt.match_id = p.match_id

),

duplas AS (

    SELECT
        a.match_id,
        a.hero_id AS hero_id_1,
        b.hero_id AS hero_id_2,

        CASE
            WHEN a.lado = 'Radiant'
                 AND a.radiant_win = TRUE THEN 1

            WHEN a.lado = 'Dire'
                 AND a.radiant_win = FALSE THEN 1

            ELSE 0
        END AS venceu

    FROM base_ti AS a

    LEFT JOIN base_ti AS b
        ON b.match_id = a.match_id
        AND b.lado = a.lado
        AND a.hero_id < b.hero_id

    WHERE b.hero_id IS NOT NULL

),

desempenho_duplas AS (

    SELECT
        hero_id_1,
        hero_id_2,
        COUNT(DISTINCT match_id) AS partidas_juntas,
        SUM(venceu) AS vitorias,

        ROUND(
            100.0 * SUM(venceu)
            / NULLIF(COUNT(DISTINCT match_id), 0),
            2
        ) AS win_rate

    FROM duplas

    GROUP BY
        hero_id_1,
        hero_id_2

),

resultado AS (

    SELECT
        h1.nome AS heroi_1,
        h2.nome AS heroi_2,
        d.partidas_juntas,
        d.vitorias,
        d.win_rate,

        DENSE_RANK() OVER (
            ORDER BY
                d.win_rate DESC,
                d.partidas_juntas DESC
        ) AS ranking_sinergia

    FROM desempenho_duplas AS d

    LEFT JOIN herois AS h1
        ON h1.hero_id = d.hero_id_1

    LEFT JOIN herois AS h2
        ON h2.hero_id = d.hero_id_2

    WHERE d.partidas_juntas >= 3

)

SELECT
    ranking_sinergia,
    heroi_1,
    heroi_2,
    partidas_juntas,
    vitorias,
    win_rate

FROM resultado

ORDER BY
    ranking_sinergia,
    partidas_juntas DESC;