WITH partidas_ranked_validas AS (

    SELECT DISTINCT
        p.match_id

    FROM partidas_publicas AS p

    INNER JOIN participacoes_publicas AS pp
        ON pp.match_id = p.match_id

    WHERE p.lobby_type = 7
),

total_publicas AS (

    SELECT
        COUNT(*) AS total_partidas

    FROM partidas_ranked_validas
),

picks_publicas AS (

    SELECT
        pp.hero_id,
        COUNT(DISTINCT pp.match_id) AS picks_publicas

    FROM participacoes_publicas AS pp

    INNER JOIN partidas_ranked_validas AS pv
        ON pv.match_id = pp.match_id

    GROUP BY pp.hero_id
),

popularidade_publicas AS (

    SELECT
        p.hero_id,
        p.picks_publicas,

        ROUND(
            100.0 * p.picks_publicas
            / NULLIF(t.total_partidas, 0),
            2
        ) AS presenca_publicas

    FROM picks_publicas AS p

    CROSS JOIN total_publicas AS t
),

total_ti AS (

    SELECT
        COUNT(*) AS total_partidas

    FROM partidas_ti
),

picks_ti AS (

    SELECT
        hero_id,
        COUNT(DISTINCT match_id) AS picks_ti

    FROM participacoes_ti

    GROUP BY hero_id
),

popularidade_ti AS (

    SELECT
        p.hero_id,
        p.picks_ti,

        ROUND(
            100.0 * p.picks_ti
            / NULLIF(t.total_partidas, 0),
            2
        ) AS presenca_ti

    FROM picks_ti AS p

    CROSS JOIN total_ti AS t
),

comparacao AS (

    SELECT
        h.hero_id,
        h.nome,

        COALESCE(pb.picks_publicas, 0) AS picks_publicas,
        COALESCE(pb.presenca_publicas, 0) AS presenca_publicas,

        COALESCE(ti.picks_ti, 0) AS picks_ti,
        COALESCE(ti.presenca_ti, 0) AS presenca_ti,

        ROUND(
            COALESCE(ti.presenca_ti, 0)
            - COALESCE(pb.presenca_publicas, 0),
            2
        ) AS diferenca_presenca

    FROM herois AS h

    LEFT JOIN popularidade_publicas AS pb
        ON pb.hero_id = h.hero_id

    LEFT JOIN popularidade_ti AS ti
        ON ti.hero_id = h.hero_id
)

SELECT
    hero_id,
    nome,
    picks_publicas,
    presenca_publicas,
    picks_ti,
    presenca_ti,
    diferenca_presenca,

    DENSE_RANK() OVER (
        ORDER BY presenca_ti DESC
    ) AS ranking_popularidade_ti

FROM comparacao

WHERE picks_ti >= 5

ORDER BY
    diferenca_presenca DESC,
    picks_ti DESC;