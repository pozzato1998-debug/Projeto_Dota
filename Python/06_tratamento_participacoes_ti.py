import csv
import json

with open("partidas_ti_brutas.json", "r", encoding="utf-8") as arquivo:
    partidas = json.load(arquivo)

participacoes = []

for partida in partidas:
    jogadores = partida["players"]

    radiant = [
        jogador for jogador in jogadores
        if jogador["isRadiant"] is True
    ]

    dire = [
        jogador for jogador in jogadores
        if jogador["isRadiant"] is False
    ]

    if len(radiant) != 5 or len(dire) != 5:
        raise ValueError(
            f"Times incompletos na partida {partida['match_id']}"
        )

    for lado, time in (("Radiant", radiant), ("Dire", dire)):
        for posicao, jogador in enumerate(time, start=1):
            participacoes.append({
                "match_id": partida["match_id"],
                "lado": lado,
                "posicao": posicao,
                "hero_id": jogador["hero_id"]
            })

with open(
    "participacoes_ti_tratadas.csv",
    "w",
    newline="",
    encoding="utf-8"
) as arquivo:
    escritor = csv.DictWriter(
        arquivo,
        fieldnames=["match_id", "lado", "posicao", "hero_id"]
    )
    escritor.writeheader()
    escritor.writerows(participacoes)

print("Partidas lidas:", len(partidas))
print("Participações criadas:", len(participacoes))
print("Primeiras participações:", participacoes[:3])
print("CSV salvo: participacoes_ti_tratadas.csv")
