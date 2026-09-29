import json
import csv

with open("partidas_publicas_brutas.json", "r", encoding="utf-8") as arquivo:
    partidas = json.load(arquivo)

participacoes = []
partidas_incompletas = 0

for partida in partidas:
    radiant = partida.get("radiant_team") or []
    dire = partida.get("dire_team") or []

    # Só criamos as dez participações quando os dois times estão completos.
    if (
    len(radiant) != 5
    or len(dire) != 5
    or any(hero_id == 0 for hero_id in radiant + dire)
):
        partidas_incompletas += 1
        continue

    for lado, herois in (("Radiant", radiant), ("Dire", dire)):
        for posicao, hero_id in enumerate(herois, start=1):
            participacoes.append({
                "match_id": partida["match_id"],
                "lado": lado,
                "posicao": posicao,
                "hero_id": hero_id
            })

print("Partidas lidas:", len(partidas))
print("Partidas com times incompletos:", partidas_incompletas)
print("Participações criadas:", len(participacoes))
print("Primeiras participações:", participacoes[:3])

with open(
    "participacoes_publicas_tratadas.csv",
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

print("CSV salvo com sucesso!")