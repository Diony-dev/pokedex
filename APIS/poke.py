import requests as rq
import json


if __name__ == "__main__":
    url = "https://pokeapi.co/api/v2/pokemon-form?offset=20&limit=50"

    response = rq.get(url)

    if response.status_code == 200:
        payload = response.json()
        nombres = dict(payload)
        ressult = nombres.get("results", [])

        if ressult:
            i = 1
            for pk in ressult:
                print(f"{i}-Pokemon: {pk['name']}")
                i+=1
