import flet as ft
from mainpage_menu.Utils import navigationBar, AuthState
from mainpage_menu.Filtro_Contenido import AlertaCochesApp
from favoritos.favoritos import FavoritesScreen
from recientes_page.pagina_recientes import PaginaRecientes




def main(page: ft.Page):
    # Configuración de la página
    page.title = "Alertacoches"
    page.padding = 0
    page.spacing = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor=ft.colors.GREY_100

    page.fonts={
        "Comforta":"/fonts/Comfortaa-Bold.ttf",
    }

    page.auth_state = AuthState()
    # creamos instancia de alertacoches
    alertacoches_app = AlertaCochesApp(page)
    page.favorites_screen = FavoritesScreen(page,alertacoches_app)
    page.recientes_page = PaginaRecientes(page)


    nav_bar = navigationBar(page,alertacoches_app)



ft.app(target=main,assets_dir="assets")
