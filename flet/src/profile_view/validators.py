import re  # Importa el módulo de expresiones regulares de Python


def validar_password(password):
    """Valida que la contraseña cumpla con los requisitos mínimos

    Args:
        password (str): Contraseña a validar

    Returns:
        str: Mensaje de error si la contraseña no cumple con los requisitos, None si es válida
    """
    if not password:
        return "La contraseña es obligatoria"
    if len(password) < 6:
        return "La contraseña debe tener al menos 6 caracteres"
    return None


def validar_password_igual(password, password2):
    """Comprueba que las contraseñas coincidan

    Args:
        password (str): Contraseña original
        password2 (str): Contraseña de confirmación

    Returns:
        str: Mensaje de error si las contraseñas no coinciden, None si son iguales
    """
    if not password2:
        return "Repite la contraseña"
    if password != password2:
        return "Las contraseñas no coinciden"
    return None


def validar_nombre(nombre):
    """Valida que el nombre tenga al menos dos palabras(nombre y apellido)

    Args:
        nombre (str): Nombre a validar

    Returns:
        str: Mensaje de error si el nombre no cumple con los requisitos, None si es válido
    """
    if not nombre:
        return "El nombre es obligatorio"
    # Verifica que haya al menos dos palabras (nombre y apellido)
    if len(nombre.split()) < 2:
        return "Introduce nombre y apellidos"
    return None


def validar_email(email):
    """Valida que el email sea válido

    Args:
        email (str): Email a validar

    Returns:
        str: Mensaje de error si el email no es válido, None si es válido
    """
    if not email:
        return "El email es obligatorio"
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        return "Email no válido"
    return None
