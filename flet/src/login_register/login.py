import flet as ft
from login_register.utils import crear_textButton, crear_button, crear_textfield, show_snackbar, validar_email, validar_password, crear_titulo
from profile_view.components import crear_header
import httpx


class LoginScreen:
    def __init__(self, page: ft.Page, switch_to_register, switch_to_recover, on__login_success):
        self.page = page  # Referencia a la página principal
        # Método para cambiar a la pantalla de registro
        self.switch_to_register = switch_to_register
        self.on_login_success = on__login_success
        self.switch_to_recover = switch_to_recover

        self.titulo = crear_titulo(
            "¡Inicia sesión y encuentra tu futuro coche!")

        # Crear los textfields con sus respectivas validaciones
        self.email = crear_textfield("Correo electrónico")
        self.email.on_blur = self.validar_email

        self.password = crear_textfield("Contraseña", password=True)
        self.password.on_change = self.validar_password

        # TextButton para cambiar a la pantalla de recuperar contraseña
        self.forgot_password = crear_textButton("¿Has olvidado la contraseña?")
        self.forgot_password.on_click = self.switch_to_recover

        # Línea divisoria entre los botones
        self.divider_btns = ft.Container(
            content=ft.Divider(height=1, color=ft.colors.GREY_200),
            expand=True
        )

        # Botones de inicio de sesión y registro con sus respectivos métodos
        self.login_button = crear_button(
            "Iniciar sesión", on_click=self.login_click)
        self.register_button = crear_button(
            "Crear Cuenta", is_principal=False, on_click=self.switch_to_register)
        
        self.header = crear_header(self.page)


    # Método para construir la pantalla de inicio de sesión con todos los elementos creados anteriormente
    # Retorna un contenedor con una fila que contiene una columna con todos los elementos
    # Configura el diseño responsive con col={"sm": 12, "md": 10, "xl": 6}
        # sm (móvil): usa 12 columnas (ancho completo)
        # md (tablet): usa 10 columnas (más estrecho)
        # xl (escritorio): usa 6 columnas (centrado)
    def build(self):
        return ft.Container(
            content=ft.Column(
                [
                    self.header,
                    ft.Container(
                        content=ft.ResponsiveRow(
                            [
                                ft.Column(
                                    controls=[
                                        ft.Container(height=20),
                                        self.titulo,
                                        self.email,
                                        self.password,
                                        ft.Row([self.login_button],
                                               expand=True),
                                        self.forgot_password,
                                        self.divider_btns,
                                        ft.Row([self.register_button],
                                               expand=True),
                                        ft.Container(height=10)
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=15,
                                    scroll=ft.ScrollMode.AUTO,
                                    col={"sm": 12, "md": 10, "xl": 6}
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        padding=15,
                        expand=True
                    )
                ],
                spacing=0
            ),
            margin=0

        )

    # Método para validar el email mientras el usuario escribe
    # La función validar_email se encuentra en utils.py
    def validar_email(self, e):
        self.email.error_text = validar_email(self.email.value)
        self.page.update()

    # Método para validar la contraseña mientras el usuario escribe
    def validar_password(self, e):
        self.password.error_text = validar_password(self.password.value)
        self.page.update()

    # Método para manejar el evento de clic en el botón de inicio de sesión
    # Usamos async para hacer una petición asíncrona al servidor
    # Asíncrona porque la petición puede tardar y no queremos bloquear la interfaz
    async def login_click(self, e):
        try:
            # Validar email y contraseña antes de iniciar sesión
            email_error = validar_email(self.email.value)
            password_error = validar_password(self.password.value)

            # Si hay errores los mostramos y se detiene el login
            if email_error or password_error:
                self.email.error_text = email_error
                self.password.error_text = password_error
                self.page.update()
                return

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "http://backend:8000/api/login",
                    json={
                        "email": self.email.value,
                        "password": self.password.value
                    }
                )

                if response.status_code == 200:
                    data = response.json()
                    # Asegurar que la página está lista
                    if self.page:
                        # Actualizar estado de autenticación
                        self.page.auth_state.user = data["user"]
                        self.page.auth_state.is_authenticated = True

                        # Actualizar UI
                        self.page.update()

                        if self.on_login_success:
                            self.on_login_success(e)
                        show_snackbar(
                            self.page, "Sesión iniciada correctamente", "success")
                else:
                    show_snackbar(
                        self.page, "Usuario o contraseña incorrectos")

        except Exception as e:
            print(f"Error en login: {e}")
            show_snackbar(self.page, "Error de conexión. Intenta de nuevo.")
            self.page.update()
