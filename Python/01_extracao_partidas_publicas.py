import requests
import time
from datetime import datetime, timezone
import json

url = "https://api.opendota.com/api/publicMatches"

ponto_consulta = 8992000000
salto_diario = 1300000

data_inicial = datetime(
    2026, 6, 13,
    tzinfo=timezone.utc
)

todas_partidas = []
numero_amostra = 1

while True:

    parametros = {
        "less_than_match_id": ponto_consulta
    }

    resposta = requests.get(
        url,
        params=parametros,
        timeout=30
    )

    print("Amostra:", numero_amostra)
    print("Status:", resposta.status_code)

    if resposta.status_code != 200:
        print("Erro:", resposta.text)
        break

    partidas = resposta.json()

    if len(partidas) == 0:
        print("Nenhuma partida encontrada")
        break

    partida_mais_antiga = min(
        partidas,
        key=lambda partida: partida["start_time"]
    )

    data_mais_antiga = datetime.fromtimestamp(
        partida_mais_antiga["start_time"],
        tz=timezone.utc
    )

    print("Data:", data_mais_antiga)
    print("Partidas recebidas:", len(partidas))

    # Interrompe quando ultrapassar a data inicial
    if data_mais_antiga < data_inicial:
        print("Data inicial alcançada")
        break

    todas_partidas.extend(partidas)

    print("Total acumulado:", len(todas_partidas))
    print("--------------------------")

    ponto_consulta = ponto_consulta - salto_diario
    numero_amostra += 1

    time.sleep(1)

print("\nTotal final:", len(todas_partidas))

if len(todas_partidas) > 0:

    partida_mais_antiga = min(
        todas_partidas,
        key=lambda partida: partida["start_time"]
    )

    partida_mais_recente = max(
        todas_partidas,
        key=lambda partida: partida["start_time"]
    )

    menor_data = datetime.fromtimestamp(
        partida_mais_antiga["start_time"],
        tz=timezone.utc
    )

    maior_data = datetime.fromtimestamp(
        partida_mais_recente["start_time"],
        tz=timezone.utc
    )

    print("Menor data armazenada:", menor_data)
    print("Maior data armazenada:", maior_data)

with open(
    "partidas_publicas_brutas.json",
    "w",
    encoding="utf-8"
) as arquivo:

    json.dump(
        todas_partidas,
        arquivo,
        ensure_ascii=False,
        indent=4
    )

print("Arquivo salvo com sucesso!")
