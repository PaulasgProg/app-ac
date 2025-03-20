import asyncio
import flet as ft
from mainpage_menu.PaginaPrincipal import MainPage
from login_register.register import RegisterScreen
from login_register.recoverpass import RecoverPasswordScreen
from login_register.login import LoginScreen
from profile_view.profile import ProfileScreen
from anuncio_page.PaginaAnuncio import PaginaAnuncio
from anuncio_page.Utils import navigationBar as navigationBarAnuncio
from favoritos.favoritos import FavoritesScreen
from recientes_page.pagina_recientes import PaginaRecientes

# Constante para la fuente que se usa en toda la app
FONT_FAMILY = "Comforta"

alerta_page = ""


def create_mainpage(page,filters):
    global alerta_page
    # creamos instancia de alertacoches
    navigationBar(page, alerta_page)

    if filters:
        del filters["date"]
        filters["make"]=alerta_page.marcas_id[filters["make"]]
        filters_marca = {"parentValueId": filters["make"]}
        alerta_page.fetch_data(
                "https://api.alertacoches.es/api/filter/2/",
                filters=filters_marca,
                dropdown=alerta_page.dropdown_modelo,
                options_dict=alerta_page.modelo_id,
                reset_dropdown=True
            )
        filters["model"]=alerta_page.modelo_id[filters["model"]] if filters["model"] != None and filters["model"]!="" else None
        filters["geartype"]=alerta_page.cambio[filters["geartype"]] if filters["geartype"] != None else None
        filters["fueltype"]=alerta_page.combustible[filters["fueltype"]] if filters["fueltype"] != None else None
        filters["province"]=alerta_page.provincias[filters["province"]] if filters["province"] != None else None
        filters["page"]=1
        print(filters)
        # Cuenta los coches con filtros aplicados
        alerta_page.fetch_data("https://api.alertacoches.es/api/search/count",
                            filters=filters, update_button_text=True)

            # Carga y muestra los resultados filtrados en pantalla
        alerta_page.fetch_data("https://api.alertacoches.es/api/search",
                            filters=filters, display_results=True)



class navigationBar(ft.UserControl):
    def __init__(self, pg, alertacoches):
        super().__init__()
        self.pg = pg
        self.auth_state = self.pg.auth_state
        self.favorites_screen = self.pg.favorites_screen
        self.recientes_page=self.pg.recientes_page
        self.animation_style = ft.animation.Animation(
            500, ft.AnimationCurve.DECELERATE)
        self.turquoise = "#007C7E"
        self.selected_color = "#007C7E"  # Color cuando está seleccionado
        self.deselected_color = "grey"  # Color cuando no está seleccionado
        self.hover_color = 'lightgrey'  # Color cuando está en hover
        self.selected_index = 0
        self.alerta = alertacoches
        self.init_helper()

    def init_helper(self):
        # Definir botones de navegación como tabs
        # Indicador de navegación
        self.indicator = ft.Container(
            width=70,  # Igual al ancho de cada icono
            height=4,
            bgcolor=self.selected_color,
            offset=ft.transform.Offset(0, 0),
            animate_offset=self.animation_style,
            alignment=ft.alignment.bottom_center,
        )

        # Inicializar las pantallas de autenticación
        self.login_screen = LoginScreen(
            self.pg,
            self.show_register_page,  # Navega a registro
            self.show_recover_page,  # Navega a recuperar contraseña
            self.handle_login_success  # Maneja cuando el login tuvo éxito
        )

        self.register_screen = RegisterScreen(
            self.pg,
            self.show_login_page  # Función para volver al login
        )

        self.recover_screen = RecoverPasswordScreen(
            self.pg,
            self.show_login_page  # Función para volver al login
        )

        self.favorites_screen = FavoritesScreen(self.pg,self.alerta)

        # navbar con botones para cambiar de paginas
        self.nav_bar = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Container(width=420 if self.pg.width > 900 else self.pg.width, alignment=ft.alignment.center,
                            content=ft.Column(controls=[
                                self.indicator,
                                ft.Row([
                                    ft.Container(
                                        data=0,
                                        on_click=lambda e: self.switch_page(
                                            e, 'page1'),
                                        width=70,
                                        height=150,
                                        content=ft.Column([ft.Icon(ft.icons.SEARCH, color=self.selected_color), ft.Text(
                                            "Inicio", color=self.selected_color, size=12, font_family=FONT_FAMILY)], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                        ),
                                    ft.Container(
                                        data=1.1,
                                        on_click=lambda e: self.switch_page(
                                            e, 'page2'),
                                        width=70,
                                        height=150,
                                        content=ft.Column([ft.Icon(ft.icons.FAVORITE_BORDER_ROUNDED, color=self.deselected_color), ft.Text(
                                            "Favoritos", color=self.deselected_color, size=12,
                                            font_family=FONT_FAMILY)], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                    ),
                                    ft.Container(
                                        data=2.3,
                                        on_click=lambda e: self.switch_page(
                                            e, 'page3'),
                                        width=70,
                                        height=150,
                                        content=ft.Column([ft.Icon(ft.icons.TIMER_OUTLINED, color=self.deselected_color), ft.Text(
                                            "Recientes", color=self.deselected_color, size=12,
                                            font_family=FONT_FAMILY)], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                    ),
                                    ft.Container(
                                        data=3.4,
                                        on_click=lambda e: self.switch_page(
                                            e, 'page4'),
                                        width=70,
                                        height=150,
                                        content=ft.Column([ft.Icon(
                                            # Cambiar el icono según el estado de autenticación
                                            ft.icons.FACE if self.auth_state.is_authenticated else ft.icons.ACCOUNT_CIRCLE,
                                            color=self.deselected_color
                                        ),
                                            ft.Text("Mi perfil" if self.auth_state.is_authenticated else "Conéctate",
                                                    color=self.deselected_color, size=12,
                                                    font_family=FONT_FAMILY)],
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                        ),
                                    ),
                                    ft.Container(
                                        data=4.6,
                                        on_click=lambda e: self.switch_page(
                                            e, 'page5'),
                                        width=70,
                                        height=150,
                                        content=ft.Column([ft.Icon(ft.icons.NOTIFICATIONS, color=self.deselected_color), ft.Text(
                                            "Alertas", color=self.deselected_color, size=12, font_family=FONT_FAMILY)], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                    ),])
                            ]))
            ]
        )

        header = Header(self.pg, self.alerta)
        # pasamos la instancia a la paginaprincipal
        self.main_view = MainPage(self.alerta, self.pg, header)

        # Definir páginas del contenido
        self.page1 = ft.Container(
            alignment=ft.alignment.center,
            offset=ft.transform.Offset(0, 0),
            animate_offset=self.animation_style,
            bgcolor=ft.colors.GREY_100,
            content=self.main_view,
        )

        self.page2 = ft.Container(
            alignment=ft.alignment.center,
            offset=ft.transform.Offset(2, 0),
            animate_offset=self.animation_style,
            bgcolor=ft.colors.GREY_100,
            content=self.favorites_screen if self.auth_state.is_authenticated else self.login_screen.build()
        )

        self.page3 = ft.Container(
            alignment=ft.alignment.center,
            offset=ft.transform.Offset(2, 0),
            animate_offset=self.animation_style,
            bgcolor=ft.colors.GREY_100,
            content=self.recientes_page if self.auth_state.is_authenticated else self.login_screen.build()
        )
        self.page4 = ft.Container(
            alignment=ft.alignment.center,
            offset=ft.transform.Offset(2, 0),
            animate_offset=self.animation_style,
            bgcolor=ft.colors.GREY_100,
            content=self.login_screen.build()
        )
        self.page5 = ft.Container(
            alignment=ft.alignment.center,
            offset=ft.transform.Offset(2, 0),
            animate_offset=self.animation_style,
            bgcolor=ft.colors.GREY_100,
            content=self.login_screen.build()
        )

        # Controlador de cambio de página
        self.switch_control = {
            'page1': self.page1,
            'page2': self.page2,
            'page3': self.page3,
            'page4': self.page4,
            'page5': self.page5
        }
        # Estructura principal
        self.pg.add(
            ft.Column(
                expand=True,
                controls=[
                    ft.Container(
                        expand=True,
                        content=ft.Stack(
                            controls=[self.page1, self.page2, self.page3, self.page4, self.page5])
                    ),
                    ft.Container(
                        height=80,
                        bgcolor="white",
                        content=ft.Column(
                            alignment="center",
                            controls=[self.nav_bar]
                        ),
                    ),
                ]
            )
        )
        # Cargamos los datos de la app alertacoches
        self.alerta.load_filtered_results(None)  # cargamos resultados

        def update_controls(e):  # actualiza el tamaño de los filtros
            print("Resize detected")  # Debugging line
            self.alerta.update_controls()
            self.main_view.header.update_controls()
            self.alerta.update()
            self.pg.update()
        # cada vez que se redimensiona la pantalla se ejecuta la funcion
        self.pg.on_resize = update_controls
        update_controls(None)
        self.pg.update()

    # cambia el color de los botones segun pa pantalla seleccionada
    def on_click_event(self, e):
        self.selected_index = e.control.data
        icon = e.control.content.controls[0]
        text = e.control.content.controls[1]

        # Actualizar el icono si es el botón de favoritos
        if self.selected_index == 1.1:
            icon.name = ft.icons.FAVORITE

        icon.color = self.selected_color
        text.color = self.selected_color
        # los botones que no coincidan con el data les cambiamos el color a deseleccionados
        for container in self.nav_bar.controls[0].content.controls[1].controls:
            if self.selected_index != container.data:
                container_icon = container.content.controls[0]
            # Restaurar el icono de favoritos cuando no está seleccionado
                if container.data == 1.1:
                    container_icon.name = ft.icons.FAVORITE_BORDER_ROUNDED
                container.content.controls[0].color = self.deselected_color
                container.content.controls[1].color = self.deselected_color
        self.nav_bar.update()

    def switch_page(self, e, point):
        self.last_click_event = e
        self.last_requested_page = point

        # Si no está autenticado y no es la página principal
        if not self.auth_state.is_authenticated and point != 'page1':
            self.show_login_page(e)

        self.on_click_event(e)

        # Ocultar todas las páginas desplazándolas fuera de vista
        for page in self.switch_control.values():
            page.offset.x = 2
            page.update()

        # Mostrar la página seleccionada moviéndola a x = 0
        self.switch_control[point].offset.x = 0
        self.switch_control[point].update()

        # actualizamos la posicion del indicador segun el boton seleccionado
        button_index = e.control.data

        # Actualizamos la posicion del indicador
        self.indicator.offset.x = button_index
        self.indicator.update()

    # Manejador de login exitoso
    def handle_login_success(self, e):
        """
        Este método se ejecuta cuando el login es exitoso.
        Marca al usuario como autenticado.
        Cambia el texto "Conéctate" por "Mi perfil" en la navbar.
        Actualiza el contenido de las páginas.
        Muestra un mensaje de éxito al usuario
        """
        self.auth_state.is_authenticated = True  # Actualiza el estado

        # Actualizar el texto y el icono del botón de perfil
        profile_button = self.nav_bar.controls[0].content.controls[1].controls[3]
        # Actualizar icono
        profile_button.content.controls[0].name = ft.icons.FACE
        # Actualizar texto
        profile_button.content.controls[1].value = "Mi perfil"
        self.nav_bar.update()

        # Recrear FavoritesScreen con la página actualizada
        self.pg.favorites_screen = FavoritesScreen(self.pg,self.alerta)
        self.favorites_screen = self.pg.favorites_screen

        #Construimos la página de favoritos con los datos guardados
        asyncio.create_task(self.recientes_page.init_async())


        # Actualizar contenido de las páginas protegidas
        self.page2.content = self.favorites_screen
        self.page3.content = self.recientes_page
        self.page4.content = ProfileScreen(self.pg, self.handle_logout).build()
        self.page5.content = ft.Text('Page 5', size=50)

        self.pg.update()

    def handle_logout(self, e):
        self.auth_state.is_authenticated = False
        self.auth_state.user = None  # Reiniciar el estado de autenticación

        # Actualizar el texto del botón de perfil
        self.nav_bar.controls[0].content.controls[1].controls[3].content.controls[1].value = "Conéctate"
        self.nav_bar.update()

        # Actualizar el texto y el icono del botón de perfil
        profile_button = self.nav_bar.controls[0].content.controls[1].controls[3]
        # Actualizar icono
        profile_button.content.controls[0].name = ft.icons.ACCOUNT_CIRCLE
        # Actualizar texto
        profile_button.content.controls[1].value = "Conéctate"
        self.nav_bar.update()

        # Reiniciar los campos del login
        self.login_screen.email.value = ""  # Vaciar campo de email
        self.login_screen.password.value = ""  # Vaciar campo de contraseña

        # Actualizar contenido de las páginas protegidas para mostrar login
        self.page2.content = self.login_screen.build()
        self.page3.content = self.login_screen.build()
        self.page4.content = self.login_screen.build()
        self.page5.content = self.login_screen.build()

        # Mostrar mensaje
        self.pg.show_snack_bar(
            ft.SnackBar(
                content=ft.Text("Sesión cerrada correctamente",
                                color=ft.colors.GREEN_900, font_family=FONT_FAMILY),
                bgcolor=ft.colors.GREEN_100,
                action_color=ft.colors.GREEN_700,
                action="CERRAR",
                duration=3000,
            )
        )
        self.pg.update()

    def show_login_page(self, e):
        """
        Muestra la pantalla de login sólo si el usuario no está autenticado
        Usa la última página seleccionada como contenedor
        """
        if not self.auth_state.is_authenticated:
            current_page = self.switch_control[self.last_requested_page]
            current_page.content = self.login_screen.build()
            current_page.update()

    def show_register_page(self, e):
        """
        Muestra la pantalla de registro
        """
        current_page = self.switch_control[self.last_requested_page]
        current_page.content = self.register_screen.build()
        current_page.update()

    def show_recover_page(self, e):
        """
        Muestra la pantalla de recuperar contraseña
        """
        current_page = self.switch_control[self.last_requested_page]
        current_page.content = self.recover_screen.build()
        current_page.update()


class Header(ft.Container):
    def __init__(self, page, alerta):
        super().__init__()
        self.page = page
        self.border_radius = 20 if self.page.width>=900 else 0
        self.image_src = f"/coche.jpg"
        self.image_fit = ft.ImageFit.COVER
        self.width = 1300
        self.height = 250
        self.margin = ft.margin.only(bottom=10)
        self.marcas_id = {}
        self.modelo_id = {}
        self.alertacoches = alerta

        # Retrieve controls from AlertaCoches
        shared_controls = self.alertacoches.get_shared_controls()
        self.dropdown_marca = shared_controls["dropdown_marca"]
        self.dropdown_modelo = shared_controls["dropdown_modelo"]
        self.open_modal_button = shared_controls["open_modal_button"]
        self.search_button = shared_controls["boton_modal"]
        self.search_button.data = "modal"
        self.search_button.on_click = self.execute_load_filtered_results

        self.recientes = shared_controls["recientes"]
        # VENTANA MODAL DE MAS  FILTROS
        self.modal = ft.AlertDialog(
            title=ft.Text("Filtros", font_family=FONT_FAMILY),
            content=ft.Column(
                [
                    self.dropdown_marca,
                    self.dropdown_modelo,
                    self.recientes,
                    # abre la ventana modal de filtros avanzados que esté en la clase AlertaCoches
                    self.open_modal_button

                ], scroll=ft.ScrollMode.AUTO, expand=True, width=800, horizontal_alignment=ft.CrossAxisAlignment.END
            ),
            actions=[
                ft.ElevatedButton("Cerrar", on_click=self.close_modal),
                self.search_button
            ]
        )
        # filtro para pantallas pequeñas
        self.container_filtro_pequeño = ft.Container(content=ft.Row(controls=[
            ft.IconButton(icon=ft.icons.SEARCH, on_click=self.open_modal),
            ft.Container(ft.Column(controls=[
                ft.Text("¿Qué coche buscas?", size=14,
                        font_family=FONT_FAMILY),
                ft.Text("Marca/Modelo/Fecha publicación",
                        color=ft.colors.GREY_500, size=12, font_family=FONT_FAMILY)
            ], horizontal_alignment=ft.CrossAxisAlignment.START, alignment=ft.MainAxisAlignment.CENTER,spacing=5),
            on_click=self.open_modal),
            ft.IconButton(icon=ft.icons.SETTINGS,
                        on_click=self.alertacoches.open_modal)
        ], expand=True, alignment=ft.MainAxisAlignment.SPACE_BETWEEN), bgcolor=ft.colors.WHITE, border_radius=20, alignment=ft.alignment.center, width=500,margin=ft.margin.only(right=15,left=15))
        self.container_filtro_grande = ft.Container()

    def execute_load_filtered_results(self, e):
        # Aquí llamamos al método de la otra clase
        self.alertacoches.load_filtered_results(e)  # Llama a la función que está en la otra clase
        self.close_modal(e)  # Cierra la modal

        

    # FUNCIONN PARA QUE CAMBIE EL CONTENIDO CON RESPECTO AL TAMAÑO DE LA PAGINA
    def update_controls(self):
        # Configuración para pantallas pequeñas
        if self.page.width < 900:
            # Configuración para pantallas pequeñas
            self.dropdown_marca.width = 800
            self.dropdown_modelo.width = 800
        else:
            # Configuración para pantallas grandes
            self.dropdown_marca.width = 180
            self.dropdown_modelo.width = 160

        self.contenido_header = (
            self.container_filtro_pequeño if self.page.width < 900 else self.container_filtro_grande
        )

        # Update self.content with the current header layout
        self.content = ft.Column(
            controls=[
                ft.Container(content=ft.Column(controls=[
                    ft.Text(value="alertacoches.es", size=20 if self.page.width >
                            900 else 16, color=ft.colors.WHITE, font_family=FONT_FAMILY)
                ]), alignment=ft.alignment.top_left, margin=ft.margin.only(left=10)),

                ft.Container(content=ft.Column(controls=[
                    ft.Text(value="¿Buscas un coche de segunda mano?",size=30 if self.page.width >
                            900 else 20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE, font_family=FONT_FAMILY,text_align=ft.TextAlign("center")),
                    self.contenido_header
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    alignment=ft.alignment.center, expand=True),
            ]
        )
        self.update()
        self.page.update()

    def open_modal(self, e):
        # Abrir la ventana emergente
        self.page.dialog = self.modal
        self.modal.open = True
        self.page.update()

    def close_modal(self, e):
        # Cerrar la ventana emergente
        self.modal.open = False
        self.page.update()


class CardContainer(ft.Container):  # Plantilla para los resultados de los coches
    def __init__(self, titulo, precio, imagen, ubicacion, id, domain, page, filters, alertacoches, is_favorite=False):
        super().__init__()
        self.page = page
        self.turquesa = "#007C7E"
        self.width = 200 if self.page.width > 900 else 200
        self.height = 700 if self.page.width > 900 else 400
        padding=ft.padding.only(left=20, right=20, top=5, bottom=5) if self.page.width > 900 else ft.padding.only(left=5, right=5, top=5, bottom=5)
        self.on_click = self.on_click_event
        self.id_coche = id
        self.filters = filters
        self.alertacoches = alertacoches
        global alerta_page
        alerta_page = alertacoches
        image_container = ft.Container(image_src=imagen, border_radius=10,
                                        content=ft.IconButton(
                                            icon=ft.icons.FAVORITE if is_favorite else ft.icons.FAVORITE_BORDER,
                                            on_click=self.toggle_favorite),
                                        image_fit=ft.ImageFit.FILL, height=300 if self.page.width > 900 else 200, width=300 if self.page.width > 900 else 200,
                                        alignment=ft.alignment.top_left)
        self.content = ft.Column(controls=[
            image_container,
            ft.Text(titulo, font_family=FONT_FAMILY,color=self.turquesa),
            ft.Row(controls=[
                ft.Text(f"{precio}€", color=ft.colors.RED,
                        size=24, font_family=FONT_FAMILY),
                ft.Container(border=ft.border.all(width=1, color=self.turquesa),
                            content=ft.Text(value=domain, color=self.turquesa, font_family=FONT_FAMILY), padding=padding)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row(controls=[
                ft.Icon(name=ft.icons.LOCATION_ON,color=self.turquesa),
                ft.Text(ubicacion,
                        width=self.width - 40,  # Resta espacio para el ícono
                        max_lines=2,  # Limita a 2 líneas si es necesario
                        overflow="visible",
                        font_family=FONT_FAMILY,
                        color=self.turquesa
                        )
            ])
        ])

    def toggle_favorite(self, e):
        if not self.page.auth_state.is_authenticated:
            self.page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text(
                        "Inicia sesión para añadir favoritos", font_family=FONT_FAMILY),
                    bgcolor=ft.colors.RED_100,
                    action="CERRAR",
                    action_color=ft.colors.RED_700
                )
            )
            return

        car_data = {
            "id": self.id_coche,
            "title": self.content.controls[1].value,  # Título
            # Precio
            "price": self.content.controls[2].controls[0].value.replace("€", ""),
            "images": [self.content.controls[0].image_src],  # Imagen
            # Ubicación
            "location": {"city_name": self.content.controls[3].controls[1].value},
            "link": "",  # Añadir si tienes el link disponible
        }

        is_favorite = e.control.icon == ft.icons.FAVORITE_BORDER
        e.control.icon = ft.icons.FAVORITE if is_favorite else ft.icons.FAVORITE_BORDER
        e.control.icon_color = ft.colors.RED if is_favorite else "black"

        if is_favorite:
            self.page.favorites_screen.add_car_to_favorites(car_data)
        else:
            self.page.favorites_screen.remove_from_favorites(self.id_coche)

        e.control.update()

    def on_click_event(self, e):
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
        anuncio_screen = navigationBarAnuncio(
            self.page, anuncio_content, self.alertacoches,favorito,self.id_coche)
        self.page.add(anuncio_screen)

        self.page.update()


class RangeSliderFilters(ft.RangeSlider):  # creamos clase con rangeslider
    def __init__(self, start_value, end_value, min, max, on_change, data):
        super().__init__(start_value=start_value, end_value=end_value)
        self.start_value = start_value
        self.end_value = end_value
        self.min = min
        self.max = max
        self.divisions = (self.max - self.min)

        self.label = "{value}"
        self.on_change = on_change
        self.data = data


class AuthState:
    def __init__(self):
        # Controla si el usuario está o no autenticado
        self.is_authenticated = False
