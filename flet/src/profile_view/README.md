# Documentación Técnica - Perfil de Usuario

## Índice

1. [Estructura del Perfil de Usuario](#estructura-del-perfil-de-usuario)
2. [Documentación técnica detallada](#documentación-técnica-detallada)
3. [Flujo de funcionamiento](#flujo-de-funcionamiento)
4. [Requisitos del sistema](#requisitos-del-sistema)
5. [Instalación y ejecución](#instalación-y-ejecución)

## Estructura del Perfil de Usuario

El proyecto está estructurado en varios archivos Python que utilizan el framework Flet para crear una interfaz de usuario.

Los archivos principales son:

1. `main.py`: Punto de entrada de la aplicación
2. `profile.py`: Maneja la pantalla principal del perfil
3. `components.py`: Contiene componentes reutilizables
4. `validators.py`: Contiene las funciones de validación

> [!TIP]
>
> ```bash
> profile_view/
> ├── assets/
> │   └── fonts/
> │       └── Comfortaa-Bold.ttf
> ├── images/
> │   ├── logo.png
> │   └── profileimg.png
> ├── main.py
> ├── profile.py
> ├── components.py
> ├── validators.py
> └── README.md
> ```

## Documentación técnica detallada

### main.py

Este archivo es el punto de entrada de la aplicación. Configura la página principal y carga la fuente que se usa en el proyecto.

**Funciones principales:**

- `main(page: ft.Page)`: Configura la página principal y carga las fuentes
- `handle_logout(e)`: Maneja el evento de cierre de sesión

### profile.py

Contiene la clase `ProfileScreen` que maneja la interfaz y lógica de la pantalla de perfil.

**Métodos principales:**

- `__init__`: Inicializa los componentes de la pantalla
- `build()`: Construye la interfaz de usuario
- `init_fields()`: Inicializa los campos del formulario
- `init_ui()`: Inicializa los componentes de la interfaz
- `validar_nombre(e)`: Valida el nombre
- `validar_email(e)`: Valida el email
- `validar_password(e)`: Valida la contraseña en tiempo real
- `validar_confirm_password(e)`: Valida la confirmación de contraseña
- `show_edit_datos(e)`: Muestra el modal de edición de datos
- `show_change_password(e)`: Muestra el modal de cambio de contraseña
- `handle_datos_change(e)`: Procesa los cambios en datos personales
- `handle_password_change(e)`: Procesa el cambio de contraseña

### components.py

Contiene funciones para crear componentes reutilizables de la interfaz y la constante FONT_FAMILY para poder reutilizarla.

**Funciones principales:**

- `crear_header()`: Crea el encabezado con el logo
- `crear_titulo()`: Crea títulos para cada sección
- `crear_perfil_imagen()`: Crea el contenedor de la imagen de perfil
- `crear_textfield()`: Crea campos de texto personalizados
- `crear_datos_item()`: Crea cada contenedor de datos personales
- `crear_seguridad_container()`: Crea el contenedor de seguridad
- `crear_bottom_sheet()`: Crea modales bottom sheet
- `crear_notificaciones_container()`: Crea el contenedor de notificaciones
- `crear_logout_button()`: Crea el botón de cerrar sesión
- `show_snackbar()`: Muestra notificaciones temporales

### validators.py

Contiene funciones de validación utilizadas en toda la aplicación.

**Funciones principales:**

- `validar_email(email)`: Valida el formato del email
- `validar_password(password)`: Valida requisitos de contraseña
- `validar_nombre(nombre)`: Valida el nombre completo
- `validar_password_igual(password, password2)`: Compara entre dos contraseñas

## Flujo de Funcionamiento

1. La aplicación se inicia en `main.py`
2. Se carga la pantalla de perfil (`ProfileScreen`)
3. El usuario puede:
   - Ver sus datos personales
   - Editar nombre y email
   - Cambiar contraseña
   - Configurar notificaciones
   - Cerrar sesión

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

1. Navegar a la carpeta del proyecto:

   ```bash
   cd flet/src/profile_view
   ```

2. Ejecutar el archivo main:

   ```bash
   python main.py
   ```

La aplicación se abrirá automáticamente en una ventana de escritorio.

### Ejecución en Android

1. **Instalar Flet en Android:**
   - Abrir Google Play Store
   - Buscar "Flet" e instalar la app

2. **Preparar el entorno:**
   - Asegurarse que el PC y el dispositivo Android están en la misma red WiFi

3. **Ejecutar la app:**

   ```bash
   flet run --android
   ```

4. **Conectar con el dispositivo:**
   - Abrir la aplicación Flet en el dispositivo Android
   - Introducir la URL que aparece en la terminal del PC o escanear el QR

> [!NOTE]
> Si no cargan las imágenes, en dispositivos móviles, puedes descomentar las URLs de las imágenes en el código:
>
> En `profile.py`:
>
> ```python
> # Cambiar:
> self.image_url = os.path.join("images", "profileimg.png")
> # Por:
> self.image_url = "https://alertacoches.es/assets/profile_edit.1953f6e3.svg"
> ```
>
> En `components.py`:
>
> ```python
> # Cambiar:
> src = os.path.join("images", "logo.png")
> # Por:
> src = "https://alertacoches.es/assets/ac-concept-logo-sqr50.58b55979.png"
> ```
>

### Ejecución con Docker

1. Crear enlace simbólico al archivo de configuración:

    ```bash
    mklink docker-compose.yaml devel.yaml
    ```

2. Construir la imagen del contenedor:

    ```bash
    docker-compose build
    ```

3. Iniciar el contenedor:

    ```bash
    docker-compose up
    ```

Esta configuración permite ejecutar la aplicación en un entorno containerizado, facilitando la portabilidad y consistencia del entorno de desarrollo.

> [!IMPORTANT]
> En el archivo `devel.yaml`, modificar la línea de comando para apuntar al directorio correcto:
>
> ```yaml
> # Cambiar:
> command: flet run --host * --port 8000 --web --verbose
> # Por:
> command: flet run profile_view/main.py --host * --port 8000 --web --verbose
> ```
