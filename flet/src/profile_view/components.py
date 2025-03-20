import flet as ft
import os

# Constante para la fuente que se usa en toda la app
FONT_FAMILY = "Comforta"


def crear_header(page: ft.Page) -> ft.Container:
    """Crea el header de la aplicación con el logo de alertacoches

    Args:
        page (ft.Page): Página de la aplicación

    Returns:
        ft.Container: Contenedor con el header
    """
    logo_size = min(40, page.width *
                    0.1)  # Calcula el tamaño del logo de forma responsiva

    # image_url = "https://alertacoches.es/assets/ac-concept-logo-sqr50.58b55979.png"
    return ft.Container(
        content=ft.Row(
            [
                ft.Container(
                    content=ft.Image(
                        src=os.path.join("images", "logo.png"),
                        # src=image_url,
                        # CONTAIN mantiene la proporción de la imagen ajustándola al contenedor
                        fit=ft.ImageFit.CONTAIN,
                    ),
                    border_radius=8,
                    width=logo_size,
                    height=logo_size
                ),
                ft.Text(
                    "alertacoches",
                    color=ft.colors.TEAL_500,
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    font_family=FONT_FAMILY,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,  # Espacio entre los elementos del Row
            vertical_alignment=ft.VerticalAlignment.CENTER
        ),
        padding=ft.padding.only(top=30,bottom=10,left=20,right=20),  # Padding del contenedor
        border=ft.Border(  # Crea un borde abajo del header con un color gris
            bottom=ft.BorderSide(1, ft.colors.GREY_200)
        ),
        shadow=ft.BoxShadow(color="grey",blur_radius=4,spread_radius=1),
        bgcolor="white",
        margin=0
    )


def crear_titulo(titulo):
    """Crea un título con el texto pasado como argumento.

    Args:
        titulo (str): Texto del título

    Returns:
        ft.Container: Contenedor con el título
    """
    return ft.Container(
        content=ft.Text(
            titulo,
            size=18,
            weight=ft.FontWeight.BOLD,
            color=ft.colors.GREY_700,
            font_family=FONT_FAMILY,
        ),
        alignment=ft.alignment.center_left,
        expand=True
    )


def crear_perfil_imagen(image_url: str, page: ft.Page) -> ft.Container:
    """Crea un contenedor con la imagen de perfil del usuario.

    Args:
        image_url (str): URL de la imagen de perfil
        page (ft.Page): Página de la aplicación

    Returns:
        ft.Container: Contenedor con la imagen de perfil
    """
    return ft.Container(
        content=ft.Row(
            [ft.Container(
                content=ft.Image(
                    image_url,
                    fit=ft.ImageFit.CONTAIN,
                    error_content=ft.Icon(
                        ft.icons.PERSON,
                        size=50,
                        color=ft.colors.GREY_400
                    )
                ),
                bgcolor=ft.colors.GREY_50,
                border_radius=15,
                padding=15,
                height=min(300, page.height * 0.3),
                width=min(300, page.width * 0.8),
                alignment=ft.alignment.center,
            )],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        margin=ft.margin.only(bottom=15, top=15),
    )


def crear_textfield(label, error_text="", password=False, keyboard_type=ft.KeyboardType.TEXT):
    """ Crea un textfield con los parámetros pasados como argumentos.

    Args:
        label (str): Texto del label del textfield
        error_text (str, optional): Texto de error a mostrar. Defaults to "".
        password (bool, optional): Si el campo es para contraseña será True. Defaults to False.
        keyboard_type (ft.KeyboardType, optional): Tipo de teclado a mostrar. Defaults to ft.KeyboardType.TEXT.

    Returns:
        ft.TextField: Textfield creado
    """
    return ft.TextField(
        label=label,
        password=password,
        can_reveal_password=password,  # Para mostrar la contraseña si existe
        error_text=error_text,  # Mensaje de error
        border_radius=10,
        bgcolor=ft.colors.WHITE,
        text_size=14,
        keyboard_type=keyboard_type,  # Tipo de teclado
        border_color=ft.colors.GREY_300,
        # Color del borde cuando está seleccionado
        focused_border_color=ft.colors.TEAL_700,
        cursor_color=ft.colors.TEAL_700,
        focused_bgcolor=ft.colors.GREY_50,  # Color de fondo cuando está seleccionado
        label_style=ft.TextStyle(
            color=ft.colors.GREY_600, font_family=FONT_FAMILY),
        text_style=ft.TextStyle(color=ft.colors.GREY_900,
                                font_family=FONT_FAMILY),
        error_style=ft.TextStyle(
            color=ft.colors.RED_700, font_family=FONT_FAMILY),
        content_padding=ft.padding.symmetric(
            horizontal=15, vertical=20),  # Padding del contenido del textfield
        expand=True)


def crear_datos_item(icon: str, texto: str, on_click=None) -> ft.Container:
    """Crea un contenedor con un icono y un texto.

    Args:
        icon (str): Icono a mostrar
        texto (str): Texto a mostrar
        on_click (callable, optional): Función a ejecutar al hacer clic. Defaults to None.

    Returns:
        ft.Container: Contenedor con el icono y el texto
    """
    return ft.Container(
        content=ft.Row([
            ft.Icon(icon, color=ft.colors.TEAL_800),
            ft.Text(
                texto,
                color=ft.colors.TEAL_800,
                weight=ft.FontWeight.W_400,
                font_family=FONT_FAMILY,
                size=16
            )
        ], spacing=10),
        bgcolor=ft.colors.GREY_100,
        border_radius=15,
        padding=20,
        margin=ft.margin.only(bottom=10),
        on_click=on_click
    )


def crear_seguridad_container(on_change_password) -> ft.Container:
    """Crea el contenedor de seguridad con el botón para cambiar la contraseña.

    Args:
        on_change_password (callable): Función para manejar el cambio de contraseña

    Returns:
        ft.Container: Contenedor de seguridad
    """
    return ft.Container(
        content=ft.Row([
            ft.Icon(ft.icons.SECURITY, color=ft.colors.TEAL_800),
            ft.Text(
                "Contraseña",
                color=ft.colors.TEAL_800,
                weight=ft.FontWeight.W_400,
                expand=True,
                font_family=FONT_FAMILY,
                size=16
            ),
            ft.Container(
                content=ft.ElevatedButton(
                    content=ft.Text(
                        "CAMBIAR",
                        weight=ft.FontWeight.W_500,
                        font_family=FONT_FAMILY
                    ),
                    style=ft.ButtonStyle(
                        color=ft.colors.TEAL_800,
                        bgcolor=ft.colors.TEAL_100,
                        padding=ft.padding.symmetric(
                            horizontal=20, vertical=15),
                        shape=ft.RoundedRectangleBorder(radius=10)
                    ),
                    on_click=on_change_password
                ),
            )
        ], spacing=10),
        padding=ft.padding.symmetric(horizontal=20, vertical=10),
        bgcolor=ft.colors.GREY_100,
        border_radius=15,
        margin=ft.margin.only(top=10, bottom=25)
    )


def crear_bottom_sheet_datos(page: ft.Page, title: str, field1: ft.TextField, field2: ft.TextField, on_save, on_close):
    """Crea un bottom sheet con los campos y botones pasados como argumentos.

    Args:
        page (ft.Page): Página de la aplicación
        title (str): Título del bottom sheet
        field1 (ft.TextField): Primer campo del bottom sheet
        field2 (ft.TextField): Segundo campo del bottom sheet
        on_save (callable): Función para guardar los datos
        on_close (callable): Función para cerrar el bottom sheet

    Returns:
        ft.BottomSheet: Modal bottom sheet creado
    """
    bottom_sheet = ft.BottomSheet(
        content=ft.Container(
            content=ft.Column(
                [
                    # Encabezado con el título y botón de cerrar
                    ft.Row(
                        [
                            ft.Text(  # Título del bottom sheet
                                title,
                                size=18,
                                weight=ft.FontWeight.W_700,
                                color=ft.colors.GREY_900,
                                font_family=FONT_FAMILY
                            ),
                            ft.IconButton(  # Botón de cerrar(X)
                                icon=ft.icons.CLOSE,
                                icon_color=ft.colors.GREY_800,
                                on_click=on_close,
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    # Campos de texto pasado como argumento
                    field1,
                    field2,

                    # Contenedor con los botones de guardar y cancelar
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.TextButton(  # Botón de cancelar
                                    content=ft.Text(
                                        "Cancelar", color=ft.colors.GREY_900, font_family=FONT_FAMILY),
                                    style=ft.ButtonStyle(
                                        color=ft.colors.GREY_800,
                                        padding=ft.padding.symmetric(
                                            vertical=20, horizontal=30),

                                    ),
                                    on_click=on_close,

                                ),
                                ft.ElevatedButton(  # Botón de guardar
                                    "Guardar",
                                    icon=ft.icons.SAVE,
                                    icon_color=ft.colors.WHITE,
                                    style=ft.ButtonStyle(
                                        color=ft.colors.WHITE,
                                        bgcolor=ft.colors.TEAL_700,
                                        shape=ft.RoundedRectangleBorder(
                                            radius=20),
                                        padding=ft.padding.symmetric(
                                            vertical=15, horizontal=20),
                                        text_style=ft.TextStyle(
                                            font_family=FONT_FAMILY)
                                    ),
                                    on_click=on_save,

                                ),
                            ],
                            # Alineación de los botones a la derecha
                            alignment=ft.MainAxisAlignment.END,
                            spacing=10,
                        ),
                        margin=ft.margin.only(top=20),
                    ),
                ],
                spacing=20,
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=20,
            bgcolor=ft.colors.WHITE,
            border_radius=10
        )
    )
    page.overlay.append(bottom_sheet)
    bottom_sheet.open = True
    page.update()
    return bottom_sheet


# Para cambio de contraseña (3 campos)
def crear_bottom_sheet_password(page: ft.Page,
                                title: str,
                                current_password: ft.TextField,
                                new_password: ft.TextField,
                                confirm_password: ft.TextField,
                                on_save, on_close):
    bottom_sheet = ft.BottomSheet(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(
                                title,
                                size=18,
                                weight=ft.FontWeight.W_700,
                                color=ft.colors.GREY_900,
                                font_family=FONT_FAMILY
                            ),
                            ft.IconButton(
                                icon=ft.icons.CLOSE,
                                icon_color=ft.colors.GREY_800,
                                on_click=on_close,
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    current_password,
                    new_password,
                    confirm_password,
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.TextButton(
                                    content=ft.Text(
                                        "Cancelar", color=ft.colors.GREY_900, font_family=FONT_FAMILY),
                                    style=ft.ButtonStyle(
                                        color=ft.colors.GREY_800,
                                        padding=ft.padding.symmetric(
                                            vertical=20, horizontal=30),
                                    ),
                                    on_click=on_close,
                                ),
                                ft.ElevatedButton(
                                    "Guardar",
                                    icon=ft.icons.SAVE,
                                    icon_color=ft.colors.WHITE,
                                    style=ft.ButtonStyle(
                                        color=ft.colors.WHITE,
                                        bgcolor=ft.colors.TEAL_700,
                                        shape=ft.RoundedRectangleBorder(
                                            radius=20),
                                        padding=ft.padding.symmetric(
                                            vertical=15, horizontal=20),
                                        text_style=ft.TextStyle(
                                            font_family=FONT_FAMILY)
                                    ),
                                    on_click=on_save,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.END,
                            spacing=10,
                        ),
                        margin=ft.margin.only(top=20),
                    ),
                ],
                spacing=20,
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=20,
            bgcolor=ft.colors.WHITE,
            border_radius=10
        )
    )
    page.overlay.append(bottom_sheet)
    bottom_sheet.open = True
    page.update()
    return bottom_sheet


def crear_notificaciones_container() -> ft.Container:
    """Crea el contenedor de notificaciones.

    Returns:
        ft.Container: Contenedor de notificaciones
    """
    return ft.Container(
        content=ft.Row([
            ft.Switch(
                value=True,
                active_color=ft.colors.WHITE,
                active_track_color=ft.colors.TEAL_700,
                inactive_track_color=ft.colors.GREY_600,
                inactive_thumb_color=ft.colors.GREY_100
            ),
            ft.Text(
                "Recibir comunicaciones comerciales y noticias",
                color=ft.colors.GREY_500,
                size=16,
                font_family=FONT_FAMILY,
                expand=True
            ),
        ],
            expand=True,
            spacing=10,
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.VerticalAlignment.CENTER),
        margin=ft.margin.only(top=10, bottom=25)
    )


def crear_logout_button(on_logout) -> ft.Row:
    """Crea un botón para cerrar sesión.

    Args:
        on_logout (callable): Función para cerrar sesión

    Returns:
        ft.Row: Botón de cerrar sesión con el texto "Cerrar sesión"
    """
    return ft.Row(
        controls=[
            ft.TextButton(
                content=ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.icons.LOGOUT, color=ft.colors.TEAL_700),
                        ft.Text(
                            "Cerrar sesión",
                            color=ft.colors.TEAL_700,
                            weight=ft.FontWeight.W_500,
                            font_family=FONT_FAMILY
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                    padding=ft.padding.symmetric(vertical=20, horizontal=20),
                    bgcolor=ft.colors.GREY_100,
                    border_radius=20
                ),
                on_click=on_logout,
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )


def show_snackbar(page: ft.Page, mensaje, tipo="error"):
    """Muestra un snackbar con el mensaje pasado como argumento.

    Args:
        page (ft.Page): Página de la aplicación
        mensaje (str): Mensaje a mostrar en el snackbar
        tipo (str, optional): Tipo de mensaje. Defaults to "error".
    """
    if tipo == "error":
        color_texto = ft.colors.RED_900
        color_accion = ft.colors.RED_700
        color_fondo = ft.colors.RED_100
    else:
        color_texto = ft.colors.GREEN_900
        color_accion = ft.colors.GREEN_700
        color_fondo = ft.colors.GREEN_100

    # Crear el snackbar con el mensaje y los colores correspondientes
    snack = ft.SnackBar(
        content=ft.Text(mensaje, color=color_texto,
                        font_family=FONT_FAMILY, weight=ft.FontWeight.BOLD),
        action="CERRAR",
        action_color=color_accion,
        bgcolor=color_fondo,
        duration=3000,  # Duración de 3 segundos
    )

    # Mostrar snackbar en la parte inferior de la pantalla
    page.overlay.append(snack)
    snack.open = True
    page.update()
