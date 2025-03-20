import asyncio
from datetime import datetime
import json
import os
import flet as ft
import httpx
from recientes_page.utils import LineaTemporal

FONT_FAMILY = "Comforta"

class PaginaRecientes(ft.Column):
    def __init__(self, page):
        super().__init__()
        self.pg = page
        self.turquesa = "#007C7E"
        self.scroll = ft.ScrollMode.AUTO
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.height = self.pg.height
        self.width = self.pg.width
        self.expand = True
        self.filename = "recientes.json"
        self.lista_recientes = []  # Inicializar lista vacía


    async def init_async(self):
        #Cargamos los datos de las busquedas y los mostramos en la pantalla
        await self.cargar_recientes()
        self.update_content(filename=self.filename)
        self.build_ui()
        self.pg.update()


    async def cargar_recientes(self):
        jsondoc=await self.get_searchs()
        resultadojson=jsondoc if jsondoc else []

        resultado = await self.get_lista()
        resultado_lista = resultado if resultado else []

        # Combina ambas listas sin duplicados
        if resultadojson or resultado_lista:
            # Convertir a conjunto para eliminar duplicados
            recientes_combinados = {json.dumps(item, sort_keys=True) for item in resultadojson + resultado_lista}
            # Volver a lista de diccionarios
            self.lista_recientes = [json.loads(item) for item in recientes_combinados]
        else:
            self.lista_recientes = []
        # Ordenar por fecha más reciente (descendente)
        self.lista_recientes = sorted(
            self.lista_recientes,
            key=lambda x: datetime.fromisoformat(x["date"]),
            reverse=True  # True para más reciente primero
)


    async def get_searchs(self):
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if self.pg.auth_state.is_authenticated:
                        user_email = self.pg.auth_state.user['email']
                        return data.get(user_email, [])
            return []
        except Exception as e:
            print(f"Error loading recientes: {e}")
            return []
    async def get_lista(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"http://backend:8000/api/recientes/{self.page.auth_state.user['email']}"
                )

                if response.status_code == 200:
                    data = response.json()
                    recientes = data["recientes"]
                    return recientes
                else:
                    print("Error al obtener las búsquedas recientes:", response.json())
                    return []


        except Exception as e:
            print(f"Error en registro: {e}")
            return []

    def update_content(self, filename):
        """
        Crea o actualiza un archivo JSON con los datos del historial.
        """
        if self.pg.auth_state.is_authenticated:
            user_email = self.pg.auth_state.user['email']
            if not os.path.exists(filename):
                print(f"Creando archivo {filename}...")
                with open(filename, 'w', encoding='utf-8') as json_file:
                    json.dump({user_email: self.lista_recientes}, json_file, ensure_ascii=False, indent=4)
            else:
                with open(filename, 'r+', encoding='utf-8') as json_file:
                    data = json.load(json_file)
                    data[user_email] = self.lista_recientes
                    json_file.seek(0)
                    json.dump(data, json_file, ensure_ascii=False, indent=4)
                    json_file.truncate()
                print(f"Archivo {filename} actualizado.")

    def build_ui(self):
        """
        Construye la interfaz gráfica después de cargar los datos.
        """
        self.header = ft.Container(
            expand=True,
            bgcolor="white",
            alignment=ft.alignment.center,
            padding=ft.padding.only(left=300, right=300, bottom=15, top=15),
            content=ft.Row(
                expand=True,
                controls=[
                    ft.Column(
                        controls=[
                            ft.Row(
                                spacing=5,
                                controls=[
                                    ft.Container(
                                        image_src=os.path.join("images", "logo.png"),
                                        border_radius=10,
                                        image_fit=ft.ImageFit.FIT_WIDTH,
                                        height=40,
                                        width=40,
                                        on_click=self.back_to_home,
                                    ),
                                    ft.Container(
                                        image_src=os.path.join("/", "alertacoches.png"),
                                        height=50,
                                        width=200,
                                        image_fit=ft.ImageFit.FILL,
                                        on_click=self.back_to_home,
                                    ),
                                ]
                            )
                        ]
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            shadow=ft.BoxShadow(color="grey", blur_radius=8, spread_radius=2),
        )

        texto_historial = ft.Container(
            content=ft.Text("Tu historial de búsquedas", font_family=FONT_FAMILY, size=24),
            margin=ft.margin.only(top=20, bottom=20),
        )

        recientes = ft.Column(
            controls=[
                LineaTemporal(filters, self.pg) for filters in self.lista_recientes[:10]
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            width=self.width,
            spacing=0,
        )

        self.container = ft.Container(
            content=ft.Column([texto_historial, recientes]),
            alignment=ft.alignment.center,
            width=self.width,
            expand=True,
            padding=ft.padding.only(left=500, right=300),
        )

        self.controls = [self.header, self.container]

        self.pg.on_resize=self.update_controls(None)

    def update_controls(self, e):
        """
        Actualiza el diseño según el ancho de la ventana.
        """
        if self.pg.width > 900:
            self.horizontal_alignment=ft.CrossAxisAlignment.CENTER
            self.container.padding = ft.padding.only(left=500, right=300)
            self.header.padding = ft.padding.only(left=300, right=300, bottom=15, top=15)
            self.header.content.controls[0].controls[0].controls = [
                ft.Container(
                    image_src="//alertacoches_logo.jpeg",
                    border_radius=10,
                    image_fit=ft.ImageFit.FIT_WIDTH,
                    height=40,
                    width=40,
                    on_click=self.back_to_home,
                ),
                ft.Container(
                    image_src="//alertacoches.png",
                    height=50,
                    width=200,
                    image_fit=ft.ImageFit.FILL,
                    on_click=self.back_to_home,
                ),
            ]
        else:
            self.horizontal_alignment=ft.CrossAxisAlignment.CENTER
            self.container.padding = ft.padding.all(10)
            self.header.padding = ft.padding.only(left=20, right=10, bottom=15, top=30)
            """ self.header.content.controls[0].controls[0].controls = [
                ft.Container(
                    image_src="//alertacoches_logo.jpeg",
                    border_radius=10,
                    image_fit=ft.ImageFit.FIT_WIDTH,
                    height=40,
                    width=40,
                    on_click=self.back_to_home,
                )
            ]"""
        self.pg.update()
    def back_to_home(self, e):
        """
        Regresa a la página principal.
        """
        from mainpage_menu.Utils import create_mainpage
        self.page.clean()
        self.page.update()
        create_mainpage(self.page,None)

