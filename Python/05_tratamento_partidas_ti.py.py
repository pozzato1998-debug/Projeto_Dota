import csv
import json
from datetime import datetime, timezone

import requests


# 1. Ler as 147 partidas detalhadas já salvas
with open("partidas_ti_brutas.json", "r", encoding="utf-8") as arquivo:
    partidas = json.load(arquivo)


# 2. Consultar a lista resumida da liga, que contém os nomes das equipes
league_id = 19719
url_liga = f"https://api.opendota.com/api/leagues/{league_id}/matches"

resposta_liga = requests.get(url_liga, timeout=30)
resposta_liga.raise_for_status()

partidas_resumidas = resposta_liga.json()

# Permite encontrar o resumo de uma partida pelo match_id
resumos_por_id = {
    resumo["match_id"]: resumo
    for resumo in partidas_resumidas
}


# 3. Preparar uma linha para cada partida
partidas_tratadas = []

for partida in partidas:
    match_id = partida["match_id"]

    if match_id not in resumos_por_id:
        raise ValueError(f"Partida {match_id} não encontrada na lista da liga")

    resumo = resumos_por_id[match_id]

    data_partida = datetime.fromtimestamp(
        partida["start_time"],
        tz=timezone.utc
    )

    nome_radiant = resumo.get("radiant_team_name")
    nome_dire = resumo.get("dire_team_name")

    if partida["radiant_win"]:
        equipe_vencedora = nome_radiant
    else:
        equipe_vencedora = nome_dire

    partidas_tratadas.append({
        "match_id": match_id,
        "data_partida": data_partida.strftime("%Y-%m-%d %H:%M:%S"),
        "duracao_segundos": partida["duration"],
        "radiant_win": partida["radiant_win"],
        "leagueid": partida["leagueid"],
        "radiant_team_id": partida.get("radiant_team_id"),
        "radiant_team_name": nome_radiant,
        "dire_team_id": partida.get("dire_team_id"),
        "dire_team_name": nome_dire,
        "equipe_vencedora": equipe_vencedora,
        "radiant_score": partida.get("radiant_score"),
        "dire_score": partida.get("dire_score"),
        "series_id": partida.get("series_id"),
        "series_type": partida.get("series_type")
    })


# 4. Salvar o CSV atualizado
with open(
    "partidas_ti_tratadas.csv",
    "w",
    newline="",
    encoding="utf-8"
) as arquivo:
    escritor = csv.DictWriter(
        arquivo,
        fieldnames=partidas_tratadas[0].keys()
    )

    escritor.writeheader()
    escritor.writerows(partidas_tratadas)


# 5. Conferir o resultado
sem_nome_vencedor = sum(
    partida["equipe_vencedora"] is None
    for partida in partidas_tratadas
)

print("Partidas brutas:", len(partidas))
print("Partidas tratadas:", len(partidas_tratadas))
print("Partidas sem nome da equipe vencedora:", sem_nome_vencedor)
print("Primeira partida tratada:", partidas_tratadas[0])
print("CSV salvo: partidas_ti_tratadas.csv")