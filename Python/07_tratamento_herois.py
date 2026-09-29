# CONSULTAR CADASTRO DE HERÓIS
import requests
url_herois = "https://api.opendota.com/api/heroes"

resposta_herois = requests.get(url_herois, timeout=30)
resposta_herois.raise_for_status()

lista_herois = resposta_herois.json()

print("\nQuantidade de heróis:", len(lista_herois))

for heroi in lista_herois[:5]:
    print(
        heroi["id"],
        heroi["localized_name"],
        heroi["primary_attr"],
        heroi["attack_type"],
        heroi["roles"]
    )
