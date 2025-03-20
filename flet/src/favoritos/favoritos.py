import flet as ft
import json
import os
from anuncio_page.PaginaAnuncio import PaginaAnuncio
from anuncio_page.Utils import navigationBar
from profile_view.components import crear_header
FONT_FAMILY = "Comforta"


# Clase para la pantalla de favoritos
class FavoritesScreen(ft.UserControl):
    def __init__(self, page: ft.Page,alertacoches):
        """Constructor de la clase FavoritesScreen
        Args:
            page (ft.Page): Página principal de la app
        """
        super().__init__()
        self.page = page
        self.expand=True
        self.turquoise = "#007C7E"
        # Archivo donde se guardan los favoritos
        self.favorites_file = "favorites.json"
        self.favorites = self.load_favorites()  # Cargamos los favoritos guardados

        self.header = crear_header(self.page)  # Creamos el header de la página
        self.init_ui()  # Iniciamos la interfaz de usuario
        self.alertacoches=alertacoches

    def init_ui(self):
        """
        Inicializa los elementos visuales de la pantalla de favoritos
        creando una cuadrícula (grid) para mostrarlos
        """
        # Se crea una cuadrícula para mostrar los favoritos
        self.favorites_grid = ft.GridView(
            expand=True,
            # Adaptamos el número de columnas según el ancho
            runs_count=2 if self.page.width > 700 else 1,
            # Calcula el ancho máximo de cada elemento según el tamaño de la pantalla
            max_extent=self.page.width * \
            (0.4 if self.page.width > 700 else 0.8),
            # Define la proporción alto/ancho de cada elemento
            # >1 será más ancho que alto, <1 será más alto que ancho
            child_aspect_ratio=0.85,
            # Espacio vertical entre tarjetas 2% del ancho de la pantalla
            spacing=self.page.width * 0.20,
            # Espacio horizontal entre tarjetas 1% del ancho de la pantalla
            run_spacing=self.page.width * 0.03,
            # Espacio alrededor de toda la cuadricula
            padding=self.page.width * 0.01
        )

        # Contenedor principal de la pantalla
        # Se añadirá la cuadrícula de favoritos o un mensaje de favoritos vacíos
        self.content_container = ft.Container(
            expand=True,
            margin=ft.margin.symmetric(
                horizontal=self.page.width * 0.01,
                vertical=0  # Margen vertical fijo más pequeño
            ),
            padding=ft.padding.only(bottom=100)
        )

        self.initial_content()

    def load_favorites(self):
        """
        Carga los favoritos guardados en el archivo favorites.json
        """
        try:
            if os.path.exists(self.favorites_file):  # Si existe el archivo
                with open(self.favorites_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if self.page.auth_state.is_authenticated:  # Si el usuario está autenticado
                        # Obtenemos el email del usuario
                        user_email = self.page.auth_state.user['email']
                        # Devolvemos los favoritos del usuario
                        return data.get(user_email, [])
            return []
        except Exception as e:
            print(f"Error cargar favoritos: {e}")
            return []

    def save_favorites(self):
        """
        Guarda los favoritos en el archivo favorites.json
        """
        try:
            data = {}  # Diccionario para guardar los favoritos
            if os.path.exists(self.favorites_file):
                with open(self.favorites_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

            if self.page.auth_state.is_authenticated:
                user_email = self.page.auth_state.user['email']
                # Guardamos los favoritos del usuario
                data[user_email] = self.favorites

            # Escribimos los favoritos en el archivo
            with open(self.favorites_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error al guardar favoritos: {e}")

    def initial_content(self):
        """
        Prepara el contenido inicial de la pantalla de favoritos
        mostrando los favoritos o un mensaje de favoritos vacíos
        """
        if not self.favorites:
            # Si no hay favoritos, mostramos un mensaje de favoritos vacíos
            self.content_container.content = self.show_empty_state()
        else:
            self.favorites_grid.controls.clear()
            # Añadimos las tarjetas de los favoritos a la cuadrícula
            for car in self.favorites:
                self.favorites_grid.controls.append(
                    self.create_favorite_card(car)
                )
            # Añadimos la cuadrícula al contenedor principal
            self.content_container.content = self.favorites_grid
        self.update()  # Actualizamos la pantalla
        self.page.update()  # Actualizamos la página

    def build(self):
        """
        Define la estructura de la pantalla de favoritos
        Devuelve una columna con el título y el contenido principal
        """
        return ft.Container(
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    self.header,
                    ft.ListView(
                        expand=True,
                        controls=[
                            ft.Text(
                                "Tus favoritos",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color=ft.colors.GREY_800,
                                font_family=FONT_FAMILY
                            ),
                            self.content_container
                        ],
                    )

                ],
                spacing=10,
            ),
        )

    def show_empty_state(self):
        """
        Crea un mensaje de favoritos vacíos
        Mostrando una imagen y un texto
        """
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Image(
                        src="/favorito_vacio.svg",
                        width=200,
                        height=200,
                        fit=ft.ImageFit.CONTAIN,
                    ),
                    ft.Text(
                        "¡Añade nuevos favoritos para verlos aquí!",
                        size=16,
                        color=ft.colors.GREY_600,
                        weight=ft.FontWeight.W_500,
                        text_align=ft.TextAlign.CENTER,
                        font_family=FONT_FAMILY
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
            alignment=ft.alignment.center,
            expand=True
        )

    def create_favorite_card(self, car):
        """
        Crea una tarjeta para mostrar un favorito
        con la imagen, título, precio y botón de ver
        Args:
            car: Diccionario con los datos del coche

        Returns: ft.Column con la tarjeta del favorito
        """
        # Calculamos el ancho de la tarjeta según el tamaño de la pantalla
        card_width = self.page.width * \
            (0.35 if self.page.width > 700 else 0.75)
        image_height = card_width * 0.65  # Proporción de la imagen

        return ft.Column([
            # Tarjeta con la imagen del coche
            ft.Card(
                content=ft.Container(
                    content=ft.Stack(  # Apilamos la imagen y el botón de eliminar
                        controls=[
                            ft.Image(
                                # Si car["images"] está vacío, se asigna None sino se asigna la primera imagen car["images"][0]
                                src=car["images"][0] if car["images"] else None,
                                fit=ft.ImageFit.COVER,
                                border_radius=ft.border_radius.all(8),
                                width=card_width,
                                height=image_height,
                            ),
                            ft.Container(
                                content=ft.IconButton(
                                    icon=ft.icons.DELETE_ROUNDED,
                                    icon_color=self.turquoise,
                                    icon_size=24,
                                    # car_id=car["id"]: guarda el ID del coche actual
                                    # self.remove_from_favorites(car_id): función que se ejecutará cuando se haga clic
                                    on_click=lambda e, car_id=car["id"]: self.remove_from_favorites(
                                        car_id),
                                ),
                                alignment=ft.alignment.top_right,
                                padding=ft.padding.all(8)
                            ),
                        ],
                    ),
                    border_radius=8,
                    width=card_width,
                    height=image_height,
                )
            ),
            # Contenedor con el título, precio y botón de ver
            ft.Container(
                content=ft.Row([
                    ft.Column([
                        ft.Text(
                            car["title"],
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color=self.turquoise,
                            font_family=FONT_FAMILY,
                            overflow=ft.TextOverflow.ELLIPSIS
                        ),
                        ft.Text(
                            f"{car['price']}€",
                            size=16,
                            color=ft.colors.RED,
                            weight=ft.FontWeight.BOLD,
                            font_family=FONT_FAMILY
                        ),
                    ], spacing=4),
                    ft.FilledButton(
                        text="Ver",
                        style=ft.ButtonStyle(
                            bgcolor=self.turquoise,
                            shape=ft.RoundedRectangleBorder(radius=8),
                        ),
                        height=30,
                        on_click=lambda e, car_id=car["id"]: self.handle_view_car(
                            e, car_id)
                    ),
                ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    wrap=True
                ),
                padding=ft.padding.all(8),
                bgcolor=ft.colors.with_opacity(0.8, ft.colors.WHITE),
                width=card_width,
                margin=ft.margin.only(top=-8),
            ),
        ], spacing=0)

    def add_car_to_favorites(self, car_data):
        """
        Añade un coche a la lista de favoritos
        Verifica si el usuario está autenticado y si el coche ya está en favoritos
        Args:
            car_data: Diccionario con los datos del coche
        """
        if not self.page.auth_state.is_authenticated:
            self.page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text("Inicia sesión para añadir favoritos"),
                    bgcolor=ft.colors.RED_100,
                    action="CERRAR"
                )
            )
            return

        # Si el coche no está en favoritos, lo añadimos
        if not any(car["id"] == car_data["id"] for car in self.favorites):
            self.favorites.append(car_data)  # Añadimos el coche a favoritos
            self.save_favorites()  # Guardamos los favoritos
            self.initial_content()  # Actualizamos la pantalla
            self.show_snackbar("Añadido a favoritos")

    def remove_from_favorites(self, car_id):
        """
        Elimina un coche de la lista de favoritos
        """
        if not self.page.auth_state.is_authenticated:
            return

        # Filtra la lista de favoritos eliminando el coche con el id indicado
        new_favorites = []
        for car in self.favorites:
            if car["id"] != car_id:  # Si el ID no coincide con el que queremos eliminar
                new_favorites.append(car)  # Lo mantenemos en la lista
        self.favorites = new_favorites  # Actualizamos la lista
        self.save_favorites()
        self.initial_content()
        self.show_snackbar("Eliminado de favoritos", "warning")

    def handle_view_car(self, e, car_id):
        """
        Muestra la página de un anuncio al hacer clic en el botón de ver
        Args:
            e: Evento de clic
            car_id: Identificador del coche
        """
        try:
            self.page.update()
            self.page.clean()

            # Buscamos el coche en la lista de favoritos
            car = next(
                (car for car in self.favorites if car["id"] == car_id), None)
  
            if car:
                anuncio_screen = navigationBar(
                    self.page,
                    PaginaAnuncio(
                        self.page,
                        car_id,
                        self.alertacoches.getFilters(),
                        self.alertacoches
                    ),
                    self.alertacoches,
                    True,
                    car_id
                )

                self.page.add(anuncio_screen)
                self.page.update()

        except Exception as e:
            print(f"Error en handle_view_car: {e}")
            self.show_snackbar("Error al cargar el anuncio", "error")

    def show_snackbar(self, message: str, tipo="success"):
        """
        Muestra un mensaje temporal en la parte inferior de la pantalla
        Args:
            message (str): Mensaje a mostrar
            tipo (str): Tipo de mensaje ('success', 'error' o 'warning')
        """
        if tipo == "error":
            color_texto = ft.colors.RED_900
            color_accion = ft.colors.RED_700
            color_fondo = ft.colors.RED_100
        elif tipo == "warning":
            color_texto = ft.colors.ORANGE_900
            color_accion = ft.colors.ORANGE_700
            color_fondo = ft.colors.ORANGE_100
        else:
            color_texto = ft.colors.GREEN_900
            color_accion = ft.colors.GREEN_700
            color_fondo = ft.colors.GREEN_100

        snack = ft.SnackBar(
            content=ft.Text(message, color=color_texto,
                            font_family=FONT_FAMILY),
            action="CERRAR",
            action_color=color_accion,
            bgcolor=color_fondo,
            duration=3000
        )

        self.page.overlay.append(snack)
        snack.open = True
        self.page.update()
