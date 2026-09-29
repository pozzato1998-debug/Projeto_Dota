import json
import time
import requests

league_id = 19719
url_liga = f"https://api.opendota.com/api/leagues/{league_id}/matches"

resposta = requests.get(url_liga, timeout=30)
resposta.raise_for_status()

lista_partidas = resposta.json()
partidas_detalhadas = []

print("Partidas encontradas na liga:", len(lista_partidas))

for numero, partida_resumida in enumerate(lista_partidas, start=1):
    match_id = partida_resumida["match_id"]
    url_detalhes = f"https://api.opendota.com/api/matches/{match_id}"

    try:
        resposta_detalhes = requests.get(url_detalhes, timeout=30)
        resposta_detalhes.raise_for_status()
    except requests.RequestException as erro:
        print(f"Falha na partida {match_id}: {erro}")
        break

    partida = resposta_detalhes.json()

    if partida.get("leagueid") != league_id:
        print(f"Liga divergente na partida {match_id}")
        break

    partidas_detalhadas.append(partida)

    print(
        f"{numero}/{len(lista_partidas)}",
        "ID:", match_id,
        "Jogadores:", len(partida.get("players", []))
    )

    time.sleep(1)

with open("partidas_ti_brutas.json", "w", encoding="utf-8") as arquivo:
    json.dump(partidas_detalhadas, arquivo, ensure_ascii=False, indent=2)

print("Partidas detalhadas salvas:", len(partidas_detalhadas))
print("Arquivo salvo: partidas_ti_brutas.json")