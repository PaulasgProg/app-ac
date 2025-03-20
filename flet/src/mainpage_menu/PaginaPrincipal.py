import flet as ft

class MainPage(ft.UserControl): #pagina principal
    def __init__(self,alerta,page,header):
        super().__init__()
        self.page=page
        self.selected_index = 0
        self.alertacoches_app=alerta
        self.header=header
        self.page.favorites_screen = page.favorites_screen
        self.page.auth_state = page.auth_state
    def build(self):
        # Contenido principal
        self.main_content =ft.Container(content=ft.Column(
                controls=[
                    self.header,
                    self.alertacoches_app
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO,
                on_scroll=self.alertacoches_app.handle_scroll,
                
            ),expand=True,
            alignment=ft.alignment.center,
            height=self.page.height) 

        # Estructura principal usando Column
        return ft.Column(
            controls=[
                self.main_content,
            ],
            spacing=0,
        )
    