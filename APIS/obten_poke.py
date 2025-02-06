import requests as rq
import json

def encontrar_poke(nombre, offset =0 ):
   
    nombre_poke = nombre
    args = {'offset':offset}
    url = "https://pokeapi.co/api/v2/pokemon-form"
    response = rq.get(url, json=args)
    #comprueba que la respuesta se hecho con exito
    if response.status_code == 200:
       payload = response.json()
       resultados = dict(payload).get('results', [])
      #comprueba que no se ha incluido texto vacio
       if nombre != "":
          for poke in resultados:#recorre los resultados y los compara con el nombre que se busca
              if poke['name'] == nombre_poke:
                print(f"pokemon: {poke['name']} encontrado😁")
                return True
          if 'next' in payload and payload['next'] is not None:#comprueba que no se han terminado los datos 
             print(f"No se encontró en este grupo de resultados. Buscando más...")
             return encontrar_poke(nombre_poke, offset + 20)#le agrega 20 al limite de resultados
          else:
            print(f"Pokémon {nombre_poke} no encontrado. 😔")
            return False   
                


if __name__=="__main__":
     nombre_poke = input("ingresa el nombre del pokemon: ")
     encontrar_poke(nombre_poke)

     

   