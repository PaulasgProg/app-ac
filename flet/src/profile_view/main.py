import flet as ft
from profile_view.profile import ProfileScreen
import os


def main(page: ft.Page):
    page.title = "Perfil del usuario"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.colors.WHITE
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    page.fonts = {
        "Comfortaa-Bold": os.path.join(current_dir, "assets","fonts", "Comfortaa-Bold.ttf")
    }

    def handle_logout(e):
        print("Logout clicked")
        # Aquí iría la lógica de logout

    main_content = ft.Container(
        content=ProfileScreen(page, handle_logout).build(),
        expand=True
    )

    page.add(main_content)
    


ft.app(target=main)