import flet as ft
from login_register.utils import crear_titulo, crear_textfield, crear_button, crear_textButton, validar_email, show_snackbar
from profile_view.components import crear_header


class RecoverPasswordScreen:
    def __init__(self, page: ft.Page, switch_to_login):
        self.page = page
        self.switch_to_login = switch_to_login

        # Crear título de la pantalla
        self.titulo = crear_titulo("Reestablecer contraseña")

        # Campo de email con validación
        self.email = crear_textfield("Correo electrónico")
        self.email.on_blur = self.validar_email

        # Botón principal de envío
        self.recover_button = crear_button("Enviar enlace de recuperación")
        self.recover_button.on_click = self.recover_click

        # Botón para volver al login
        self.back_button = crear_textButton("¡Ya me acuerdo!")
        self.back_button.on_click = self.switch_to_login

        self.header = crear_header(self.page)

    # Método para construir la pantalla de recuperación de contraseña
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
                                        ft.Row([self.recover_button],
                                               expand=True),
                                        self.back_button,
                                        ft.Container(height=10)
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=20,
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
                ], spacing=0
            ),
            margin=0
        )

    # Método para validar el email
    def validar_email(self, e):
        self.email.error_text = validar_email(self.email.value)
        self.page.update()

    # Método para enviar el email de recuperación
    def recover_click(self, e):
        # Validar email antes de procesar
        email_error = validar_email(self.email.value)

        if email_error:
            self.email.error_text = email_error
            self.page.update()
            return

        # Aquí iría la lógica real de envío del email de recuperación
        # Por ahora solo mostramos un mensaje de éxito
        show_snackbar(
            self.page,
            "Se ha enviado un enlace de recuperación a tu email",
            "success"
        )

        # Volver al login
        self.switch_to_login(None)
