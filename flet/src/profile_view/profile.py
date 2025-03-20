import flet as ft
from profile_view.validators import validar_nombre, validar_email, validar_password, validar_password_igual
from profile_view.components import crear_perfil_imagen, crear_datos_item, crear_seguridad_container, crear_notificaciones_container, crear_logout_button, crear_bottom_sheet_datos, crear_textfield, crear_titulo, show_snackbar, crear_header, crear_bottom_sheet_password
import asyncio
import httpx


class ProfileScreen:
    """
    Clase que representa la pantalla de perfil de usuario.
    """

    def __init__(self, page: ft.Page, on_logout):
        """ Inicializa la pantalla de perfil.

        Args:
            page (ft.Page): Página en la que se mostrará el perfil.
            on_logout (callable): Función que se ejecutará al hacer clic en el botón de cerrar sesión.
        """

        self.page = page
        self.on_logout = on_logout
        self.current_user = self.page.auth_state.user

        # URL de la imagen de perfil
        # self.image_url = "https://alertacoches.es/assets/profile_edit.1953f6e3.svg"
        self.image_url = "/images/profileimg.png"

        # Inicializar campos y componentes de la pantalla
        self.init_fields()
        self.init_ui()

        # Cargar datos del usuario
        asyncio.create_task(self.load_user_data())

    def build(self):
        """ Construye la pantalla de perfil.

        Returns:
            ft.Container: Contenedor con la pantalla de perfil.
        """
        return ft.Container(
            content=ft.Column(
                [
                    self.header,
                    # Contenido scrolleable con ResponsiveRow
                    ft.Container(
                        content=ft.ResponsiveRow(
                            [
                                ft.Column(
                                    controls=[
                                        self.title,
                                        self.perfilImg,
                                        self.datos_title,
                                        self.datos_container,
                                        self.security_title,
                                        self.security_container,
                                        self.notifications_title,
                                        self.notifications_container,
                                        ft.Container(height=10),
                                        self.divider,
                                        self.logout_button
                                    ],
                                    scroll=ft.ScrollMode.AUTO,
                                    # Configuración responsive para diferentes tamaños de pantalla
                                    col={"sm": 12, "md": 10, "xl": 6}
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        padding=20,
                        expand=True
                    ),
                ],
                spacing=0,  # Elimina espacio entre header y contenido
            ),
            bgcolor=ft.colors.WHITE,
            width=self.page.width,
            height=self.page.height,
            margin=0

        )

    def init_fields(self):
        """ Inicializa los campos y componentes de la pantalla de perfil."""

        self.current_password = crear_textfield(
            "Contraseña actual", password=True)
        self.current_password.on_change = self.validar_current_password

        # Campos para cambiar la contraseña
        self.new_password = crear_textfield("Nueva contraseña", password=True)
        self.new_password.on_change = self.validar_password

        self.confirm_password = crear_textfield(
            "Confirmar contraseña", password=True)
        self.confirm_password.on_change = self.validar_confirm_password

        # Campos de datos personales
        self.name = crear_textfield("Nombre completo")
        self.name.on_blur = self.validar_nombre
        self.name.value = self.current_user.get("nombre", "")

        self.email = crear_textfield(
            "Correo electrónico", keyboard_type=ft.KeyboardType.EMAIL)
        # self.email.on_blur = self.validar_email
        self.email.read_only = True  # No se puede editar el email
        self.email.value = self.current_user.get("email", "")

    async def load_user_data(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"http://backend:8000/api/user/{self.current_user['email']}")
                if response.status_code == 200:
                    user_data = response.json()
                    self.name.value = user_data["nombre"]
                    self.email.value = user_data["email"]
                    self.update_ui_user_data()
                    self.page.update()
        except Exception as e:
            print(f"Error cargando datos: {e}")
            show_snackbar(self.page, "Error cargando datos del usuario")

    def init_ui(self):
        """ Inicializa los componentes de la interfaz de usuario."""
        self.header = crear_header(self.page)
        self.title = crear_titulo("Perfil")
        self.perfilImg = crear_perfil_imagen(self.image_url, self.page)

        # Sección de datos personales
        self.datos_title = crear_titulo("DATOS PERSONALES")
        self.datos_container = ft.Container(
            content=ft.Column([
                crear_datos_item(
                    ft.icons.PERSON, self.name.value, self.show_edit_datos),
                crear_datos_item(
                    ft.icons.MAIL, self.email.value, self.show_edit_datos)
            ]),
            margin=ft.margin.only(top=10, bottom=25)
        )

        # Sección de seguridad
        self.security_title = crear_titulo("SEGURIDAD")
        self.security_container = crear_seguridad_container(
            self.show_change_password)

        # Sección de notificaciones
        self.notifications_title = crear_titulo(
            "CONFIGURACIÓN DE NOTIFICACIONES")
        self.notifications_container = crear_notificaciones_container()

        # Divider y botón de cerrar sesión
        self.divider = ft.Divider(1, color=ft.colors.GREY_300)
        self.logout_button = crear_logout_button(self.on_logout)

    def validar_nombre(self, e):
        """Valida el campo de nombre cuando cambia."""
        self.name.error_text = validar_nombre(self.name.value)
        self.page.update()

    def validar_email(self, e):
        """Valida el campo de email cuando cambia."""
        self.email.error_text = validar_email(self.email.value)
        self.page.update()

    def validar_password(self, e):
        """
        Valida la nueva contraseña y, si existe confirmación,
        verifica que ambas coincidan.
        """
        if self.new_password.error_text:  # Solo validar si es el campo de nueva contraseña
            self.new_password.error_text = validar_password(
                self.new_password.value)
            # Solo validar confirmación si ya tiene valor
            if self.confirm_password.value:
                self.confirm_password.error_text = validar_password_igual(
                    self.new_password.value, self.confirm_password.value)

    def validar_confirm_password(self, e):
        """Valida que la confirmación de contraseña coincida con la nueva contraseña."""
        self.confirm_password.error_text = validar_password_igual(
            self.new_password.value, self.confirm_password.value)
        self.page.update()

    def validar_current_password(self, e):
        """Valida solo la contraseña actual"""
        if not self.current_password.value:
            self.current_password.error_text = "La contraseña actual es obligatoria"
        else:
            self.current_password.error_text = None
        self.page.update()

    def show_edit_datos(self, e):
        """Muestra el bottom sheet para editar los datos personales."""
        self.bottom_sheet = crear_bottom_sheet_datos(
            self.page,
            "Cambia tus datos personales",
            self.name,
            self.email,
            self.handle_datos_change,
            self.close_datos
        )

    def show_change_password(self, e):
        """Muestra el bottom sheet para cambiar la contraseña."""
        self.bottom_sheet = crear_bottom_sheet_password(
            self.page,
            "Cambia tu contraseña",
            self.current_password,
            self.new_password,
            self.confirm_password,
            self.handle_password_change,
            self.close_password

        )

    def update_ui_user_data(self):
        """Actualiza la UI con los datos del usuario"""
        nombre_text = self.datos_container.content.controls[0].content.controls[1]
        email_text = self.datos_container.content.controls[1].content.controls[1]
        nombre_text.value = self.name.value
        email_text.value = self.email.value
        self.page.update()

    def close_bottom_sheet(self, e, sheet_type="datos"):
        """Cierra el bottom sheet y actualiza los valores si es necesario.

        Args:
            sheet_type (str, optional): Tipo de bottom sheet. Defaults to "datos".
        """
        if self.bottom_sheet:  # Solo si el bottom sheet está  activo
            if sheet_type == "datos":
                # Restaura los valores originales de los campos
                # Estructura de acceso a los valores:
                # self.datos_container -> El contenedor principal
                #   .content -> Accede al Column dentro del contenedor
                #   .controls[0] -> Primer item (nombre)
                #   .content -> Accede al Row dentro del item
                #   .controls[1] -> Segundo elemento del Row (el Text, siendo el primero el icono)
                self.name.value = self.datos_container.content.controls[0].content.controls[1].value
                self.email.value = self.datos_container.content.controls[1].content.controls[1].value
                self.name.error_text = None
                self.email.error_text = None
            else:  # password
                self.current_password.value = ""
                self.new_password.value = ""
                self.confirm_password.value = ""
                self.current_password.error_text = None
                self.new_password.error_text = None
                self.confirm_password.error_text = None

            self.bottom_sheet.open = False
            self.page.update()

    def close_datos(self, e):
        """Maneja el cierre del bottom sheet de datos personales."""
        self.close_bottom_sheet(e, "datos")

    def close_password(self, e):
        """Maneja el cierre del bottom sheet de cambio de contraseña."""
        self.close_bottom_sheet(e, "password")

    async def handle_datos_change(self, e):
        """
        Maneja el guardado de cambios en datos personales.
        Valida los campos y actualiza la UI si todo es correcto.
        """
        # Comprueba si hay errores existentes
        if self.name.error_text:
            self.bottom_sheet.update()
            return

        try:
            async with httpx.AsyncClient() as client:
                response = await client.put(
                    "http://backend:8000/api/user/update",
                    json={
                        "email": self.email.value,
                        "nombre": self.name.value
                    }
                )

            if response.status_code == 200:
                data = response.json()
                self.current_user = data["user"]
                self.update_ui_user_data()
                show_snackbar(
                    self.page, "Datos actualizados correctamente", "success")
                self.close_bottom_sheet(e, "datos")
            elif response.status_code == 400:
                error_msg = response.json().get("detail", "Error actualizando datos")
                show_snackbar(self.page, error_msg)
            else:
                show_snackbar(self.page, "Error actualizando datos")

        except Exception as e:
            print(f"Error actualizando datos: {e}")
            show_snackbar(self.page, "Error de conexión")

        self.page.update()

    async def handle_password_change(self, e):
        """Maneja el cambio de contraseña."""
        if (self.current_password.error_text or
            self.new_password.error_text or
            self.confirm_password.error_text or
                not self.current_password.value):

            # Forzar validación si está vacía
            if not self.current_password.value:
                self.current_password.error_text = "La contraseña actual es obligatoria"

            self.bottom_sheet.update()
            return

        try:
            async with httpx.AsyncClient() as client:
                response = await client.put(
                    "http://backend:8000/api/user/change-password",
                    json={
                        "email": self.current_user["email"],
                        "old_password": self.current_password.value,
                        "new_password": self.new_password.value
                    }
                )

                if response.status_code == 200:
                    show_snackbar(
                        self.page, "Contraseña cambiada correctamente", "success")
                    self.close_bottom_sheet(e, "password")
                else:
                    error_msg = response.json().get("detail", "Error cambiando contraseña")
                    show_snackbar(self.page, error_msg)

        except Exception as e:
            print(f"Error cambiando contraseña: {e}")
            show_snackbar(self.page, "Error de conexión")
