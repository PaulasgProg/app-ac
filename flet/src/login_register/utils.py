import flet as ft
import re

# Constante para la fuente que se usa en toda la app
FONT_FAMILY = "Comforta"

# Método para validar el email retorna un mensaje de error si no es válido
def validar_email(email):
    if not email:
        return "El email es obligatorio"
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        return "Email no válido"
    return None


# Método para validar que la contraseña sea válida
def validar_password(password):
    if not password:
        return "La contraseña es obligatoria"
    if len(password) < 6:
        return "La contraseña debe tener al menos 6 caracteres"
    return None


# Método para validar que el nombre tenga al menos un nombre y un apellido
def validar_nombre(nombre):
    if not nombre:
        return "El nombre es obligatorio"
    # Verifica que haya al menos dos palabras (nombre y apellido)
    if len(nombre.split()) < 2:
        return "Introduce nombre y apellidos"
    return None


# Método para validar que las contraseñas sean iguales
def validar_password_igual(password, password2):
    if not password2:
        return "Repite la contraseña"
    if password != password2:
        return "Las contraseñas no coinciden"
    return None


# Método para crear un título en Login y Register
def crear_titulo(titulo, alineacion=ft.alignment.center_left):
    return ft.Container(
        content=ft.Text(
            titulo,
            size=24,
            weight=ft.FontWeight.NORMAL,
            color=ft.colors.GREY_600,
            font_family=FONT_FAMILY
        ),
        alignment=alineacion,
        expand=True
    )


# Método para crear los textfields personalizados en Login y Register
def crear_textfield(label, error_text="", password=False, keyboard_type=ft.KeyboardType.TEXT):
    return ft.TextField(
        label=label,
        password=password,
        can_reveal_password=password,  # Para mostrar la contraseña si existe
        error_text=error_text,  # Mensaje de error
        error_style=ft.TextStyle(font_family=FONT_FAMILY, color=ft.colors.RED_600),
        border_radius=10,
        bgcolor=ft.colors.WHITE,
        text_size=16,
        keyboard_type=keyboard_type,  # Tipo de teclado
        border_color=ft.colors.GREY_300,
        # Color del borde cuando está seleccionado
        focused_border_color=ft.colors.TEAL_700,
        cursor_color=ft.colors.TEAL_700,
        focused_bgcolor=ft.colors.GREY_50,  # Color de fondo cuando está seleccionado
        label_style=ft.TextStyle(color=ft.colors.GREY_600, font_family=FONT_FAMILY),
        text_style=ft.TextStyle(color=ft.colors.GREY_900, font_family=FONT_FAMILY),
        content_padding=ft.padding.symmetric(
            horizontal=15, vertical=20),  # Padding del contenido del textfield
        expand=True)


# Método para crear los botones en Login y Register
def crear_button(text, is_principal=True, on_click=None):
    return ft.ElevatedButton(
        text=text,
        on_click=on_click,
        style=ft.ButtonStyle(
            color=ft.colors.WHITE if is_principal else ft.colors.GREY_600,
            bgcolor={
                ft.ControlState.DEFAULT: ft.colors.TEAL_700 if is_principal else ft.colors.GREY_200,
                ft.ControlState.HOVERED: ft.colors.TEAL_800 if is_principal else ft.colors.GREY_100,
                ft.ControlState.PRESSED: ft.colors.TEAL_900 if is_principal else ft.colors.GREY_200,
            },
            text_style=ft.TextStyle(font_family=FONT_FAMILY),
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=ft.padding.symmetric(vertical=20, horizontal=10),
            side=None if is_principal else ft.BorderSide(1, ft.colors.GREY_300)
        ),
        expand=True
    )


# Método para crear los botones "Ya tengo cuenta" y "Has olvidado la contraseña"
def crear_textButton(text):
    return ft.TextButton(
        content=ft.Text(
            text,
            weight=ft.FontWeight.W_400,
            color=ft.colors.GREY_700,
            font_family=FONT_FAMILY,
            style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE)
        )
    )


# Método para crear un checkbox personalizado en Register
# Retorna una fila con el checkbox y el texto y también el checkbox para poder acceder a su estado
def crear_checkbox(label, value=False):
    checkbox = ft.Checkbox(
        value=value,
        fill_color={
            ft.ControlState.DEFAULT: ft.colors.WHITE,
            ft.ControlState.SELECTED: ft.colors.TEAL_700
        },
        check_color=ft.colors.WHITE
    )

    row = ft.Row(
        controls=[
            checkbox,
            ft.Text(
                label,
                size=12,
                color=ft.colors.GREY_800,
                max_lines=None,
                overflow=ft.TextOverflow.VISIBLE,
                width=300,
                expand=True,
                font_family=FONT_FAMILY
            )
        ],
        spacing=10,
        expand=True
    )
    return row, checkbox


# Método para mostrar un mensaje en la parte inferior de la pantalla
def show_snackbar(page: ft.Page, mensaje, tipo="error"):
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
        content=ft.Text(mensaje, color=color_texto, font_family=FONT_FAMILY),
        action="CERRAR",
        action_color=color_accion,
        bgcolor=color_fondo,
        duration=3000,  # Duración de 3 segundos
    )

    # Mostrar snackbar en la parte inferior de la pantalla
    page.overlay.append(snack)
    snack.open = True
    page.update()
