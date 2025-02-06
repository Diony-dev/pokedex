import requests as rq
from io import BytesIO
from PIL import Image, ImageTk

URL = "https://pokeapi.co/api/v2/pokemon-form/"

def obtner_img(poke, url = URL):
     if poke != "":
        nom_poke = poke
        response = rq.get(url+nom_poke.lower())
        
        if response.status_code == 200:
            result = dict(response.json())
            img_url = result['sprites']['front_default']
            img_response = rq.get(img_url)
            if img_response.status_code == 200:
                img = Image.open(BytesIO(img_response.content))
                img = img.resize((32,32))
                imagen_f= ImageTk.PhotoImage(img)
                
                return imagen_f
            else:
                return False
        
        
        
     else:
        return False
        
        
