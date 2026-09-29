WITH base_publicas AS (

    SELECT
        pp.hero_id,
        p.match_id,

        CASE
            WHEN p.radiant_win = TRUE
                AND pp.lado = 'Radiant'
                THEN 1

            WHEN p.radiant_win = FALSE
                AND pp.lado = 'Dire'
                THEN 1

            ELSE 0
        END AS venceu

    FROM partidas_publicas AS p

    INNER JOIN participacoes_publicas AS pp
        ON pp.match_id = p.match_id

    -- Considera somente partidas ranked
    WHERE p.lobby_type = 7
),

win_rate_publicas AS (

    SELECT
        hero_id,

        COUNT(DISTINCT match_id) AS partidas_publicas,

        SUM(venceu) AS vitorias_publicas,

        ROUND(
            100.0
            * SUM(venceu)
            / NULLIF(COUNT(DISTINCT match_id), 0),
            2
        ) AS win_rate_publicas

    FROM base_publicas

    GROUP BY hero_id
),

base_ti AS (

    SELECT
        pt.hero_id,
        p.match_id,

        CASE
            WHEN p.radiant_win = TRUE
                AND pt.lado = 'Radiant'
                THEN 1

            WHEN p.radiant_win = FALSE
                AND pt.lado = 'Dire'
                THEN 1

            ELSE 0
        END AS venceu

    FROM partidas_ti AS p

    INNER JOIN participacoes_ti AS pt
        ON pt.match_id = p.match_id
),

win_rate_ti AS (

    SELECT
        hero_id,

        COUNT(DISTINCT match_id) AS partidas_ti,

        SUM(venceu) AS vitorias_ti,

        ROUND(
            100.0
            * SUM(venceu)
            / NULLIF(COUNT(DISTINCT match_id), 0),
            2
        ) AS win_rate_ti

    FROM base_ti

    GROUP BY hero_id
),

comparacao AS (

    SELECT
        h.hero_id,
        h.nome,

        COALESCE(pb.partidas_publicas, 0)
            AS partidas_publicas,

        COALESCE(pb.vitorias_publicas, 0)
            AS vitorias_publicas,

        pb.win_rate_publicas,

        ti.partidas_ti,
        ti.vitorias_ti,
        ti.win_rate_ti,

        ROUND(
            ti.win_rate_ti - pb.win_rate_publicas,
            2
        ) AS diferenca_win_rate

    FROM herois AS h

    LEFT JOIN win_rate_publicas AS pb
        ON pb.hero_id = h.hero_id

    INNER JOIN win_rate_ti AS ti
        ON ti.hero_id = h.hero_id
)

SELECT
    hero_id,
    nome,
    partidas_publicas,
    vitorias_publicas,
    win_rate_publicas,
    partidas_ti,
    vitorias_ti,
    win_rate_ti,
    diferenca_win_rate,

    DENSE_RANK() OVER (
        ORDER BY win_rate_ti DESC
    ) AS ranking_win_rate_ti

FROM comparacao


WHERE partidas_ti >= 5

ORDER BY
    win_rate_ti DESC,
    partidas_ti DESC,
    nome;
