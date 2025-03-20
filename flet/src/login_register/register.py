import flet as ft
from login_register.utils import crear_textButton, crear_button, crear_textfield, show_snackbar, validar_email, validar_password, crear_titulo, validar_nombre, validar_password_igual, crear_checkbox
import httpx
from profile_view.components import crear_header

# Clase que maneja la pantalla de registro de usuarios
# Contiene todos los elementos del formulario y la lógica de validación


class RegisterScreen:
    def __init__(self, page: ft.Page, switch_to_login):
        self.page = page
        self.switch_to_login = switch_to_login

        # Creamos el título principal de la pantalla
        self.titulo = crear_titulo("¡Regístrate para potenciar tu búsqueda!")

        # Campo de nombre completo con su validación
        self.name = crear_textfield("Nombre completo")
        self.name.on_blur = self.validar_nombre

        # Campo de email con su validación
        self.email = crear_textfield("Correo electrónico")
        self.email.on_blur = self.validar_email

        # Campo de contraseña con su validación
        self.password = crear_textfield("Contraseña", password=True)
        self.password.on_change = self.validar_password

        # Campo de confirmación de contraseña
        self.confirm_password = crear_textfield(
            "Repite la contraseña", password=True)
        self.confirm_password.on_change = self.validar_confirm_password

        # Checkbox para aceptar términos y condiciones
        self.terms_row, self.terms_check = crear_checkbox(
            "He leído y acepto el Aviso Legal, la Política de Privacidad y la Política de Cookies")

        # Checkbox para aceptar marketing (por defecto marcado)
        self.marketing_row, self.marketing_check = crear_checkbox(
            "Sí, deseo recibir comunicaciones comerciales de AlertaCoches y empresas colaboradoras", True)

        # Botón principal de crear cuenta
        self.create_account_button = crear_button("Crear cuenta")
        self.create_account_button.on_click = self.register_click

        # Link para volver a la pantalla de login
        self.login_link = crear_textButton("Ya tengo cuenta")
        self.login_link.on_click = self.switch_to_login

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
                                        self.name,
                                        self.email,
                                        self.password,
                                        self.confirm_password,
                                        self.terms_row,
                                        self.marketing_row,
                                        ft.Row(
                                            [self.create_account_button], expand=True),
                                        self.login_link,
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
                ], spacing=0
            ),
            margin=0
        )

    # Método para validar el nombre en tiempo real
    def validar_nombre(self, e):
        self.name.error_text = validar_nombre(self.name.value)
        self.page.update()

    # Método para validar el email en tiempo real
    def validar_email(self, e):
        self.email.error_text = validar_email(self.email.value)
        self.page.update()

    # Método para validar la contraseña en tiempo real
    def validar_password(self, e):
        self.password.error_text = validar_password(self.password.value)
        self.page.update()

    # Método para validar que las contraseñas coincidan en tiempo real
    def validar_confirm_password(self, e):
        self.confirm_password.error_text = validar_password_igual(
            self.password.value, self.confirm_password.value)
        self.page.update()

    # Método para manejar el evento de clic en el botón de crear cuenta
    # Realiza todas las validaciones y muestra mensajes de error si es necesario
    async def register_click(self, e):
        # Validar nombre, email, contraseña y confirmación de contraseña
        self.name.error_text = validar_nombre(self.name.value)
        self.email.error_text = validar_email(self.email.value)
        self.password.error_text = validar_password(self.password.value)
        self.confirm_password.error_text = validar_password_igual(
            self.password.value, self.confirm_password.value)

        # Si hay errores en alguno de los campos se muestra un mensaje de error y se detiene el registro
        if self.name.error_text or self.email.error_text or self.password.error_text or self.confirm_password.error_text:
            show_snackbar(
                self.page, "Por favor, revisa los campos marcados en rojo")
            self.page.update()
            return

        # Si no se aceptan los términos y condiciones se muestra un mensaje de error y se detiene el registro
        if not self.terms_check.value:
            show_snackbar(
                self.page, "Debes aceptar los términos y condiciones")
            return

        try:
            # Llamada al endpoint de registro
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "http://backend:8000/api/register",
                    json={
                        "nombre": self.name.value,
                        "email": self.email.value,
                        "password": self.password.value
                    }
                )

                if response.status_code == 200:
                    show_snackbar(
                        self.page, "¡Cuenta creada con éxito!", "success")
                    # Volver a la pantalla de login
                    if self.switch_to_login:
                        self.switch_to_login(e)
                else:
                    error_msg = response.json().get("detail", "Error en el registro")
                    show_snackbar(self.page, error_msg)

        except Exception as e:
            print(f"Error en registro: {e}")
            show_snackbar(self.page, "Error de conexión")

        self.page.update()
