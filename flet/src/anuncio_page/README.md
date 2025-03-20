# Documentación Técnica – Pagina Anuncio

## Índice

1. Introducción
2. Requisitos y dependencias
3. Estructura proyecto
4. Documentación detallada de clases y funciones
5. Instalación y ejecución

## 1. Introducción

La app crea una página de anuncio interactiva para mostrar información detallada de un automóvil seleccionado, usando datos de una API externa. Se incluye una barra de navegación, un área de presentación de imágenes y detalles del coche, y una sección de anuncios de coches similares.

## 2. Requisitos y dependencias

- **Flet**: Framework de desarrollo de UI que permite construir aplicaciones interactivas.
- **Requests**: Librería de Python para realizar solicitudes HTTP y obtener datos de la API.
- **tldextract**: Librería para extraer componentes de URLs y obtener el dominio del anuncio.
- **re**: Para expresiones regulares, en este caso, para extraer fechas de publicación.

## 3. Estructura proyecto

1. `PaginaAnuncio.py`: se encuentra la clase principal que genera la interfaz de anuncio
2. `main.py`: modulo donde se ejecuta la clase principal.
3. `Utils.py`: donde se almacenan los componentes y funciones que se usan en la aplicación.

## 4. Componentes y funciones

1. **PaginaAnuncio.py**
    - `PaginaAnuncio`:Clase que define la interfaz principal del anuncio, mostrando imágenes y detalles del coche, botones interactivos y coches similares.
    - `handle_on_hover`: Función que cambia el estilo visual del botón del encabezado al pasar el ratón por encima.
    - `open_website`: Abre el sitio web de origen del anuncio al hacer clic en el botón.
    - `back_to_home`: Navega a la página principal.

    **Atributos principales**:

    - ``page``: Contexto de la página principal.
    - ``car_id``: ID del coche seleccionado.
    - ``car_information``: Información del coche extraída usando el ID.
    - ``car_instance``: Instancia de Car que contiene la información del coche.
2. **Utils.py**
    - ``navigationBar``:Representa la barra de navegación, incluye un icono de búsqueda y un icono de favoritos.
    - ``Icon_buttons``:Genera un botón que contiene un icono y texto. Esto se usa en la sección de detalles del coche.
    - ``CardContainer``: Plantilla de visualización para cada coche en la sección de "Coches Similares". Incluye imagen, título, precio y ubicación del coche.
    - ``Car``:Clase para almacenar la información del coche, extrayendo detalles específicos del anuncio.
    - ``load_car_information(id)``:Realiza una solicitud GET para obtener información del coche.
    - ``load_filtered_results(filters, page)``:Solicita anuncios filtrados desde la API y los muestra en pantalla.
    - ``display_results(page, data)``:Carga anuncios de coches similares y los muestra en una GridView.
    - `add_favoritos(e,id,page,lista_favoritos)`: Cuando se hace click en el botón se añade a la lista de favoritos del usuario el coche del anuncio.

## 5. Instalación y ejecución

1. Instalar Docker Desktop
2. Abrir Docker Desktop
3. Clonar el repositorio:

   ```bash
   git clone [URL_DEL_REPOSITORIO]
   ```

4. Crear enlace simbólico:

   ```bash
   mklink docker-compose.yaml devel.yaml
   ```

5. Construir el contenedor:

   ```bash
   docker-compose build
   ```

6. Ejecutar el contenedor:

   ```bash
   docker-compose up
   ```

7. En la aplicación de escritorio de Docker podemos ver como está corriendo nuestro contenedor,
desde ahi podemos entrar en la app de flet y en el wbd.
