import flet as ft
import re
import requests
import tldextract


# Constante para la fuente que se usa en toda la app
FONT_FAMILY = "Comforta"

################# Navigation bar con icono de buscar y favoritos########################


class navigationBar(ft.UserControl):
    def __init__(self, pg, pagina_anuncio, pagina_alertacoches,favorito,id_coche):
        super().__init__()
        self.page = pg
        self.pg = pg
        self.animation_style = ft.animation.Animation(
            500, ft.AnimationCurve.DECELERATE)
        self.turquoise = "#007C7E"
        self.selected_color = "#007C7E"  # Color cuando está seleccionado
        self.deselected_color = "grey"  # Color cuando no está seleccionado
        self.hover_color = 'lightgrey'  # Color cuando está en hover
        self.pagina = pagina_anuncio
        self.pag_alertacoches = pagina_alertacoches
        self.favorito=favorito

        self.selected_index = 0
        self.icono_no_favorito= ft.Container(content=ft.Icon(ft.icons.FAVORITE_BORDER_OUTLINED, color="black"),
                            border_radius=10,
                            width=40, height=40,
                            bgcolor="white",
                            shadow=ft.BoxShadow(
                                color="grey", blur_radius=5, spread_radius=1),
                            on_click=lambda e: add_favoritos(
                                e, id_coche, self.page,self.pagina.car_information)
                            )
        self.icono_favorito= ft.Container(content=ft.Icon(ft.icons.FAVORITE, color="white"),
                            border_radius=10,
                            width=40, height=40,
                            bgcolor="red",
                            shadow=ft.BoxShadow(
                                color="grey", blur_radius=5, spread_radius=1),
                            on_click=lambda e: add_favoritos(
                                e, id_coche, self.page,self.pagina.car_information)
                            )

        self.init_helper()

    def init_helper(self):
        # Definir botones de navegación como tabs
        # navbar con botones para cambiar de paginas
        self.nav_bar = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
            controls=[
                ft.Container(content=ft.Icon(ft.icons.SEARCH, color="white"),
                            border_radius=10,
                            bgcolor=self.turquoise,
                            width=40, height=40,
                            shadow=ft.BoxShadow(
                                color="grey", blur_radius=5, spread_radius=1),
                            on_click=self.back_to_home),
                self.icono_favorito if self.favorito else self.icono_no_favorito
            ]
        )

        # Estructura principal
        self.page.add(
            ft.Column(
                expand=True,
                controls=[
                    ft.Container(
                        expand=True,
                        content=self.pagina,
                        padding=0,  # Sin padding interno
                        margin=0   # Sin margen
                    ),
                    ft.Container(
                        height=80,
                        bgcolor="white",
                        content=ft.Column(
                            expand=True,
                            alignment=ft.MainAxisAlignment.START,
                            controls=[self.nav_bar]
                        ), alignment=ft.alignment.top_center,
                        shadow=ft.BoxShadow(
                            color="grey", blur_radius=5, spread_radius=1),
                        padding=0,  # Sin padding interno
                        margin=0,   # Sin margen
                    ),
                ],
            )
        )

    def back_to_home(self, e):
        from mainpage_menu.Utils import create_mainpage
        self.pg.clean()
        self.pg.update()
        create_mainpage(self.pg,None)


############# Texto y icono en columna###############
class Icon_Text(ft.Container):
    def __init__(self, icono, caracteristica):
        super().__init__()

        self.content = ft.Column(controls=[
            ft.Icon(name=icono, color=ft.colors.BLACK87, size=22),
            ft.Text(value=caracteristica, color=ft.colors.BLACK54,
                    size=12, font_family=FONT_FAMILY)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)


############# Texto y icono en columna###############
class Image_Text(ft.Container):
    def __init__(self, imagen, caracteristica):
        super().__init__()

        self.content = ft.Column(controls=[
            ft.Image(src=imagen, height=30, width=30,
                     fit=ft.ImageFit.SCALE_DOWN),
            ft.Text(value=caracteristica, color=ft.colors.BLACK54,
                    size=12, font_family=FONT_FAMILY)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

############# Plantilla para mostrar el contenido de los coches similares al del anuncio###############


class CardContainer(ft.Container):
    def __init__(self, titulo, precio, imagen, ubicacion, domain,id,filters,alertacoches, page):
        super().__init__()
        self.page = page
        self.turquesa = "#007C7E"
        self.width = 200 if self.page.width > 900 else self.page.width / 2
        self.height = 700 if self.page.width > 900 else 400
        self.on_click = self.on_click_event
        self.id_coche = id
        self.filters = filters
        self.alertacoches=alertacoches
        #self.padding=ft.padding.only(left=20, right=20, top=5, bottom=5) if self.page.width > 900 else ft.padding.only(left=5, right=5, top=5, bottom=15)
        image_container = ft.Container(image_src=imagen, border_radius=10,
                                    content=ft.IconButton(
                                        icon=ft.icons.FAVORITE_OUTLINE_ROUNDED),
                                    image_fit=ft.ImageFit.FILL, height=300 if self.page.width > 900 else 200, width=300 if self.page.width > 900 else 200,
                                    alignment=ft.alignment.top_left)
        self.content = ft.Column(controls=[
            image_container,
            ft.Text(titulo, font_family=FONT_FAMILY,color=self.turquesa),
            ft.Row(controls=[
                ft.Text(f"{precio}€", color=ft.colors.RED,
                        size=18, font_family=FONT_FAMILY),
                ft.Container(border=ft.border.all(width=1, color=self.turquesa),
                            content=ft.Text(value=domain, color=self.turquesa, font_family=FONT_FAMILY),padding=ft.padding.all(5))
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row(controls=[
                ft.Icon(name=ft.icons.LOCATION_ON,color=self.turquesa),
                ft.Text(ubicacion,
                        width=self.width - 40,  # Resta espacio para el ícono
                        max_lines=2,  # Limita a 2 líneas si es necesario
                        overflow="visible",
                        font_family=FONT_FAMILY,color=self.turquesa
                        )
            ])
        ])
    def on_click_event(self, e):
        from anuncio_page.PaginaAnuncio import PaginaAnuncio
        self.page.clean()
        favorito=False
        if self.page.auth_state.is_authenticated:
            #Cargamos la lista de favoritos correspondiente al usuario
            lista_favoritos=self.page.favorites_screen.load_favorites()
                #Vemos si el coche está en favoritos
            for coche in lista_favoritos:
                if coche["id"] == self.id_coche:
                    favorito=True

        #Abrimos página del anuncio correspondiente
        anuncio_content = PaginaAnuncio(
            self.page, self.id_coche, self.filters,self.alertacoches)
        anuncio_screen = navigationBar(
            self.page, anuncio_content, self.alertacoches,favorito,self.id_coche)
        self.page.add(anuncio_screen)

        self.page.update()


def create_container(titulo, descripcion, color, icono, texto_boton, page):
    turquesa = "#007C7E"
    return ft.Container(margin=ft.margin.only(top=20, bottom=20),
                        content=ft.Column(
        controls=[
            ft.Text(titulo, size=18, weight=ft.FontWeight.BOLD,
                    color=turquesa, font_family=FONT_FAMILY),
            ft.Text(descripcion, width=page.width,  # Resta espacio para el ícono
                    max_lines=5,  # Limita líneas si es necesario
                    overflow="visible", font_family=FONT_FAMILY,size=12),
            ft.FilledButton(text=texto_boton, style=ft.ButtonStyle(
                color="white", bgcolor=color, text_style=ft.TextStyle(font_family=FONT_FAMILY)
            ), width=page.width, height=50),
            ft.Row(controls=[
                ft.Image(src=icono, fit=ft.ImageFit.FIT_WIDTH,
                         width=100, height=50)
            ], width=580, expand=True, alignment=ft.MainAxisAlignment.CENTER),


        ]), border=ft.Border(
            left=ft.BorderSide(1, "grey"),
            top=ft.BorderSide(1, "grey"),
            right=ft.BorderSide(1, "grey"),
            bottom=ft.BorderSide(1, "grey"),
    ),
        border_radius=8,
        padding=10,
        height=300
    )
################## Cargamos la informacion del coche seleccionado mediante el id##############


def load_car_information(id):
    # url de la api para buscar resultados
    defaultURL = "https://api.alertacoches.es/api/element/"
    try:
        # obtenemos resultados con la url y los filtros indicados
        response = requests.get(f"{defaultURL}{id}")
        response.raise_for_status()
        data = response.json()
        print("Datos de la API:", data)
        return data
    except requests.RequestException as error:
        print("Error al cargar datos:", error)
        return None

######### cargamos los coches disponibles con los filtros seleccionados y los mostramos en pantalla##########


def load_filtered_results(filters, page):
    print(filters)
    # url de la api para buscar resultados
    defaulURL = "https://api.alertacoches.es/api/search"
    try:
        # obtenemos resultados con la url y los filtros indicados
        response = requests.get(defaulURL, params=filters)
        response.raise_for_status()
        data = response.json()
        print("Datos de la API:", data)
        # Llamamos a la funcion que muestra en pantalla los resultados
        display_results(page, data)
    except requests.RequestException as error:
        print("Error al cargar datos:", error)


############ FUNCION PARA MOSTRAR LOS RESULTADOS DE COCHES SIMILARES POR PANTALLA##########
def display_results(page, data):
    for car in data.get("data", []):  # recorremos el diccionario que devuelve la api
        location = car.get("location", "Desconocido")
        city = location["city_name"]
        images = car.get("images", [])
        link = car.get("link", "Desconocido")
        id=car.get("id","Desconocido")
        # Extraer componentes de la URL
        extracted = tldextract.extract(link)

        # Combinar el subdominio, el dominio y el TLD para obtener el nombre completo
        domain_name = f"{extracted.domain}.{extracted.suffix}"

        # Obtiene la primera imagen si la lista existe y tiene elementos
        # image_url = car.get("images",[])[0] if car.get("images") and len(car.get("images")) > 0 else None
        page.images.controls.append(  # añadimos cada carta con los datos de los coches a la gridview
            CardContainer(car.get("title", "Desconocido"),
                        car.get("price", "Desconocido"),
                        images[0],
                        city,
                        domain_name,id,page.filters,page.alertacoches, page)
        )
        # Añadir `self.images` a `results_container` si no está ya añadido
    if page.images not in page.results_container.controls:
        page.results_container.controls.append(page.images)
    if page.results_container in page.controls:
        page.images.update()
        page.results_container.update()
        page.update()


########## Clase coche donde se almacena la información de anuncio#########
class Car:
    def __init__(self, information,filters):
        self.filters=filters
        # Manejo de la información del coche
        self.car_information = information
        self.price = self.car_information.get("price", "Desconocido")
        self.title = self.car_information.get("title", "Desconocido")
        self.images = self.car_information.get("images", [])
        self.link = self.car_information.get("link", "Desconocido")
        # Extraer componentes de la URL
        extracted = tldextract.extract(self.link)

        # Combinar el subdominio, el dominio y el TLD para obtener el nombre completo
        self.domain_name = f"{extracted.domain}.{extracted.suffix}"

        # Acceder a propiedades
        for prop in self.car_information.get("properties", []):
            if prop.get("key") == "year":
                self.year = prop.get("value", "Desconocido")
            elif prop.get("key") == "km":
                self.km = prop.get("value", "Desconocido")
            elif prop.get("key") == "cv":
                self.cv = prop.get("value", "Desconocido")
            elif prop.get("key") == "fuel":
                self.fuel = prop.get("value", "Desconocido")
            elif prop.get("key") == "gear_type":
                self.gear_type = prop.get("value", "Desconocido")

            # Acceder a ubicación
        location = self.car_information.get("location", {})
        self.city_name = location.get("city_name", "Desconocido")
        self.zip_code = location.get("zip_code", "Desconocido")
        self.province = location.get("province", "Desconocido")
        # Expresión regular para buscar la fecha
        match = re.search(
            r'\d{4}-\d{2}-\d{2}', self.car_information.get("createdAt", "Desconocido"))
        # Extraer la fecha si se encuentra
        if match:
            self.date = match.group(0)
        else:
            print("No se encontró una fecha en la cadena.")
            self.date = None

############### Función favoritos#############################

def add_favoritos(e, id, page, car_information):
    favorito=False
    if not page.auth_state.is_authenticated:
            page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text(
                        "Inicia sesión para añadir favoritos", font_family=FONT_FAMILY),
                    bgcolor=ft.colors.RED_100,
                    action="CERRAR",
                    action_color=ft.colors.RED_700
                )
            )
            return
    #Cargamos la lista de favoritos correspondiente al usuario
    lista_favoritos=page.favorites_screen.load_favorites()
    #Vemos si el coche está en favoritos
    for coche in lista_favoritos:
        if coche["id"] == id:
            favorito=True

    print(favorito)
    if favorito:#SI YA ES FAVORITO LO ELIMINAMOS DE FAVORITOS
        try:
            page.favorites_screen.remove_from_favorites(id)
        except:
            pass
        # Cambiamos color del boton al eliminar el coche a favoritos
        e.control.content.name = ft.icons.FAVORITE_BORDER_OUTLINED
        e.control.bgcolor = "white"
        e.control.content.color = "black"
        favorito=False
        
    else:
        try:
            #SI NO ESTÁ EN FAVORITOS LO AÑADIMOS
            page.favorites_screen.add_car_to_favorites(car_information)

        except:
            pass
        # Cambiamos color del boton al aañadir el coche a favoritos
        e.control.bgcolor = "red"
        e.control.content.name = ft.icons.FAVORITE
        e.control.content.color = "white"
        

    e.control.update()
    page.update()
