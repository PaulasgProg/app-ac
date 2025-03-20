# Documentación Técnica - Alerta Coches

## Sistema de autenticación

### Índice

1. [Estructura del Login/Register](#estructura-del-loginregister)
2. [Documentación técnica detallada](#documentación-técnica-detallada)
3. [Flujo de funcionamiento](#flujo-de-funcionamiento)
4. [Requisitos del sistema](#requisitos-del-sistema)
5. [Instalación y ejecución](#instalación-y-ejecución)

## Estructura del Login/Register

El proyecto está estructurado en varios archivos Python que utilizan el framework Flet para crear una interfaz de usuario.

Los archivos principales son:

1. `main.py`: Punto de entrada de la aplicación
2. `login.py`: Maneja la pantalla de inicio de sesión
3. `register.py`: Maneja la pantalla de registro
4. `recoverpass.py`: Maneja la pantalla de recuperación de contraseña
5. `utils.py`: Contiene funciones de utilidad compartidas

## Documentación técnica detallada

### main.py

Este archivo es el punto de entrada de la aplicación. Configura la página principal y maneja la navegación entre las diferentes pantallas.

**Funciones principales:**

- `main(page: ft.Page)`: Configura la página principal y define las funciones de navegación
- `switch_to_register(e)`: Cambia a la pantalla de registro
- `switch_to_login(e)`: Cambia a la pantalla de inicio de sesión
- `switch_to_recover(e)`: Cambia a la pantalla de recuperación de contraseña

### login.py

Contiene la clase `LoginScreen` que maneja la interfaz y lógica de la pantalla de inicio de sesión.

**Métodos principales:**

- `__init__`: Inicializa los componentes de la pantalla
- `build()`: Construye la interfaz de usuario
- `validar_email(e)`: Valida el email
- `validar_password(e)`: Valida la contraseña en tiempo real
- `login_click(e)`: Maneja el evento de clic en el botón de inicio de sesión

### register.py

Contiene la clase `RegisterScreen` que maneja la interfaz y lógica de la pantalla de registro.

**Métodos principales:**

- `__init__`: Inicializa los componentes de la pantalla
- `build()`: Construye la interfaz de usuario
- `validar_nombre(e)`: Valida el nombre
- `validar_email(e)`: Valida el email
- `validar_password(e)`: Valida la contraseña en tiempo real
- `validar_confirm_password(e)`: Valida la confirmación de contraseña en tiempo real
- `register_click(e)`: Maneja el evento de clic en el botón de registro

### recoverpass.py

Contiene la clase `RecoverPasswordScreen` que maneja la interfaz y lógica de la pantalla de recuperación de contraseña.

**Métodos principales:**

- `__init__`: Inicializa los componentes de la pantalla
- `build()`: Construye la interfaz de usuario
- `validar_email(e)`: Valida el email
- `recover_click(e)`: Maneja el evento de clic en el botón de recuperación

### utils.py

Contiene funciones de utilidad utilizadas en todo el proyecto.

**Funciones principales:**

- `validar_email(email)`: Valida el formato del email
- `validar_password(password)`: Valida que la contraseña tenga al menos seis caracteres
- `validar_nombre(nombre)`: Valida el nombre completo
- `validar_password_igual(password, password2)`: Compara dos contraseñas
- `crear_titulo(titulo, alineacion)`: Crea un título con estilo
- `crear_textfield(label, error_text, password, keyboard_type)`: Crea un campo de texto personalizado
- `crear_button(text, is_principal, on_click)`: Crea un botón personalizado
- `crear_textButton(text)`: Crea un botón de texto personalizado
- `crear_checkbox(label, value)`: Crea un checkbox personalizado
- `show_snackbar(page, mensaje, tipo)`: Muestra un mensaje de notificación

## Flujo de Funcionamiento

1. La aplicación se inicia ejecutando `main.py`
2. La pantalla inicial es la de inicio de sesión (LoginScreen)
3. Desde la pantalla de inicio de sesión, el usuario puede:
   - Intentar iniciar sesión
   - Navegar a la pantalla de registro
   - Navegar a la pantalla de recuperación de contraseña
4. En la pantalla de registro, el usuario puede:
   - Registrar una nueva cuenta
   - Volver a la pantalla de inicio de sesión
5. En la pantalla de recuperación de contraseña, el usuario puede:
   - Solicitar un enlace de recuperación
   - Volver a la pantalla de inicio de sesión

## Responsividad

La aplicación utiliza `ft.ResponsiveRow` y configuraciones de columnas para adaptarse a diferentes tamaños de pantalla:

- Pantallas pequeñas (sm): 12 columnas
- Pantallas medianas (md): 10 columnas
- Pantallas grandes (xl): 6 columnas

## Requisitos del Sistema

- Python 3.11.5
- Flet

## Instalación y Ejecución

### Instalación

1. Clonar el repositorio:

    ```bash
    git clone [URL_DEL_REPOSITORIO]
    ```

2. Instalar dependencias:

    ```bash
    pip install -r requirements.txt
    ```

### Ejecución en Escritorio

1. Moverse a la carpeta "login_register":

    ```bash
    cd flet/src/login_register
    ```

2. Ejecutar el archivo main:

    ```bash
    python main.py
    ```

La aplicación se abrirá automáticamente en una ventana de escritorio.

### Ejecución en Android

1. **Instalar Flet en Android:**
   - Abrir Google Play Store
   - Buscar "Flet" y instalar la app

2. **Preparar el entorno:**
   - Asegurarse que el PC y el dispositivo Android están en la misma red WiFi

3. **Ejecutar la app:**
   - En el PC, desde la carpeta del proyecto:

   ```bash
   flet run --android
   ```

4. **Conectar con el dispositivo:**
   - Abrir la aplicación Flet en el dispositivo Android
   - Introducir la URL que aparece en la terminal del PC o escanear el QR
