import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
from obten_ability import obtener_abily
from obtener_img import obtner_img
import requests
from io import BytesIO

cache_habilidades = {}

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=3)
        self.fuentes = {
            'font1': ('Pokemon Classic', 30),
            'font2': ('Pokemon Classic', 12),
            'font3': ('Pokemon Classic', 15, "bold")
        }
        
        colores = {
            'rojo': '#FF0000',
            'amarillo': '#FFFF00',
            'azul_claro': '#87CEEB',
            'blanco': '#FFFFFF',
            'verde_claro': '#98FB98',
            'verde_oscuro': '#006400',
            'negro': '#000000',
            'gris_claro': '#D3D3D3',
            'naranja': '#FFA500',
            'morado': '#800080'
        }
        self.geometry("400x400")
        self.title("Pokedex")
        self.marco = ctk.CTkFrame(self, fg_color=colores['azul_claro'], )
        self.marco.grid(column=0, row=0, sticky="nwes", ipady=10)
        # configuracion
        self.marco.columnconfigure(0, weight=1)
        self.marco.rowconfigure(0, weight=1)
        self.marco.rowconfigure(1, weight=2)
        
        # título
        self.titulo = ctk.CTkLabel(self.marco, text="Pokedex", font=self.fuentes['font1'], text_color=colores['blanco'], fg_color=colores['azul_claro'], bg_color=colores['negro'])
        self.titulo.grid(column=0, row=0, sticky="n", rowspan=3)

        # entrada
        self.nombre = tk.StringVar()
        self.marco2 = ctk.CTkFrame(self, fg_color=colores['azul_claro'])
        self.marco2.grid(column=0, row=1, sticky="nsew")
        # configuraciones
        self.marco2.columnconfigure(1, weight=2)
        self.marco2.rowconfigure(1, weight=2)
        self.marco2.rowconfigure((0, 2), weight=1)

        # fin de configuraciones
        self.ent_nom = ctk.CTkEntry(self.marco2, width=20, font=self.fuentes['font2'], textvariable=self.nombre)
        self.ent_nom.grid(column=0, row=0, sticky="new", columnspan=2, padx=50)
        # label de resultados
        self.result = ctk.CTkLabel(self.marco2, font=self.fuentes['font3'], text="")
        self.result.grid(column=0, row=1, sticky="n", columnspan=2)
        # buscar
        imaen = "img/pokemon.png"
        self.btn_buscar = ctk.CTkButton(self.marco2, image=self.tratar_img(imaen), fg_color=colores['amarillo'], text="Buscar", text_color=colores['negro'], font=self.fuentes['font2'], command=self.obtener_pokemon,
                                        hover_color=colores['naranja'])
        self.btn_buscar.grid(column=0, row=2, sticky="w", padx=10)
        # borrar
        borro = "img/borrar.png"
        self.btn_limpiar = ctk.CTkButton(self.marco2, image=self.tratar_img(borro), fg_color=colores['rojo'], text="limpiar", text_color=colores['negro'], font=self.fuentes['font2'], command=self.limpiar,
                                         hover_color=colores['morado'])
        self.btn_limpiar.grid(column=1, row=2, sticky="e", padx=10)

        # Label para la imagen del Pokémon
        self.img_label = ctk.CTkLabel(self.marco, text="Imagen")
        self.img_label.grid(row=2, column=0, padx=10, pady=10, ipadx=10, ipady = 10)

    def tratar_img(self, ruta):
        imagen = Image.open(ruta)
        imagen = imagen.resize((16, 16))
        logo = ImageTk.PhotoImage(imagen)
        return logo

    def obtener_pokemon(self):
        nombre = self.nombre.get()
        if nombre != "":
            # Verificar si las habilidades ya están en caché
            if nombre in cache_habilidades:
                habilidades = cache_habilidades[nombre]
            else:
                habilidades = obtener_abily(nombre)
                if habilidades:
                    cache_habilidades[nombre] = habilidades  # Guardar en caché

            if habilidades:
                self.cargar_imagen(nombre)
                resultados = "\n".join(habilidades)
                self.result.configure(text=f"Habilidades:\n{resultados}")
                self.ent_nom.delete(0, "end")
            else:
                self.result.configure(text="Habilidades:\n no encontradas 😫")
        else:
            messagebox.showerror("Error", "Ingrese un valor válido")

    def limpiar(self):
        self.ent_nom.delete(0, "end")
        self.result.configure(text="")
        self.img_label.configure(image=None)  # Limpiar la imagen mostrada

    def cargar_imagen(self, poke_name):
        url = f"https://pokeapi.co/api/v2/pokemon/{poke_name.lower()}/"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            img_url = data['sprites']['front_default']

            # Descargar la imagen
            img_response = requests.get(img_url)
            if img_response.status_code == 200:
                img = Image.open(BytesIO(img_response.content))
                img_resized = img.resize((150, 150), Image.Resampling.LANCZOS)  # Redimensionar la imagen
                imagen_tk = ImageTk.PhotoImage(img_resized)

                # Mostrar la imagen en un CTkLabel usando grid
                self.img_label.configure(image=imagen_tk)
                self.img_label.image = imagen_tk  # Mantener la referencia a la imagen
            else:
                print("Error al obtener la imagen del Pokémon.")
        else:
            print("Error al obtener los datos del Pokémon.")


app = App()

app.iconbitmap('img\pokebola.ico')
app.mainloop()
