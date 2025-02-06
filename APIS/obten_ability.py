import requests as rq
import json

def obtener_abily(nombre):
    if nombre !="":
      poke = nombre.lower()
    
    url = f"https://pokeapi.co/api/v2/pokemon/{poke}/"
    
    response = rq.get(url)
    
    if response.status_code == 200:
        payload = dict(response.json())
        result = payload.get('abilities', [])
        habilidades = [habilidad['ability']['name'] for habilidad in result]
        if habilidades:
            return habilidades
        
        else:
            
            return False
        
        
        
    else:
        return False
        
        
        
    
if __name__=="__main__":
     nombre_poke = input("ingresa el nombre del pokemon: ")
     print(obtener_abily(nombre_poke))
