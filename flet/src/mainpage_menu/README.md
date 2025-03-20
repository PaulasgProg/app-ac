# Documentación Técnica – AlertaCoches

## Índice

1. Introducción
2. Clases y Archivos
   - Filtro_Contenido.py
     - Clase AlertaCochesApp
   - PaginaPrincipal.py
     - Clase MainPage
   - main.py
     - Función main
   - Utils.py
     - Clase RangeSliderFilters
     - Clase CardContainer
     - Clase Header
     - navigationBar
3. Flujo de Funcionamiento
4. Instalación y ejecución

## 1. Introducción

AlertaCoches es una aplicación diseñada para facilitar la búsqueda y filtrado avanzado de anuncios de coches. Utilizando una interfaz intuitiva y modular, permite a los usuarios seleccionar y ajustar parámetros como marca, modelo, rango de precio, kilometraje, tipo de combustible, y muchos otros filtros para encontrar el coche ideal de acuerdo con sus preferencias.

La aplicación ha sido desarrollada en Python y utiliza la biblioteca Flet para construir una interfaz de usuario dinámica y responsiva. La interacción con una API permite a la aplicación cargar datos en tiempo real sobre marcas, modelos y otros parámetros, manteniendo la información actualizada para los usuarios.

## 2. Clases y archivos

### Filtro_Contenido.py

Este código en Python construye una interfaz para el filtrado de anuncios de coches mediante la biblioteca flet. Incluye componentes interactivos como Dropdown, RangeSlider, y ventanas modales para aplicar filtros avanzados. A continuación, se describe detalladamente la implementación de las clases y métodos, sus funciones y cómo interactúan entre sí.

#### Clase AlertaCochesApp

Es la clase principal que organiza y administra la interfaz. Incluye filtros, manejo de eventos, carga de datos de la API, y visualización de los resultados.

**Atributos:**

- Variables de filtros (marcas_id, modelo_id, etc.) para almacenar los ID de cada opción de filtro
- Componentes de filtro como Dropdown, RangeSliderFliters y CupertinoFilledButton
- Ventana modal (self.modal) para filtros avanzados
- Parámetros de filtrado (min_price, max_year, min_mileage, etc.) para definir el rango de valores permitidos

**Métodos:**

- `update_controls()`: ajusta el diseño según el ancho de la pantalla
- `load_coches()`: carga el número de coches disponibles según los filtros seleccionados
- `load_filters_modelo()`: carga los modelos según la marca seleccionada
- `load_filters_marca()`: carga las opciones de marca desde la API
- `getFilters()`: construye un diccionario con todos los filtros aplicados
- `getIdMarca()`, `getIdModelo()`: obtienen el ID de la marca y el modelo
- `fetch_data(self, endpoint, filters=None, dropdown=None, options_dict=None, update_button_text=False, display_results=False, reset_dropdown=False)`: Función genérica para hacer solicitudes a la API, que puede cargar opciones en dropdowns, contar coches o cargar resultados.
- `load_filtered_results()`: carga y muestra los resultados filtrados
- `display_results(data)`: muestra en pantalla los coches obtenidos
- `open_modal(e)`: abre la ventana modal de filtros avanzados
- `close_modal(e)`: cierra la ventana modal de filtros
- `handle_scroll`: carga automática de elementos con el scroll de la página
- `slider_is_changing(e)`: actualiza los TextField cuando se mueve el RangeSlider
- `text_is_changing(e)`: actualiza el RangeSlider cuando se modifica el TextField
- `get_shared_controls(self`: se usa para compartir los elementos de la clase con otra
- `create_card(self, car)`: crea un CardContainer

**Funcionalidad Principal:**

1. Filtrado de Datos: Selección de opciones en menús desplegables y ajuste de rangos
2. Ventana Modal para Filtros Avanzados: Opciones avanzadas con TextField y RangeSlider sincronizados
3. Interacción con la API: Carga de datos y actualización de resultados
4. Resultados en Pantalla: Presentación de resultados en formato de tarjetas en GridView

### PaginaPrincipal.py

#### Clase MainPage

La clase MainPage representa la página principal de la aplicación.

**Atributos:**

- `page`: Objeto de la página actual
- `selected_index`: Índice de navegación (0 inicial)
- `alertacoches_app`: Instancia de AlertaCoches
- `header`: Instancia de Header

**Métodos:**

- `__init__(self, alerta, page)`: Constructor de la página principal
- `build(self)`: Construye el contenido principal

### Utils.py

#### Clase Header

La clase Header se encarga de crear y gestionar el encabezado de la aplicación. Incluye funcionalidades para filtrar coches y mostrar un modal con opciones de búsqueda avanzada.

**Atributos:**

- `page`: Objeto que representa la página actual
- `border_radius`: Radio de borde para el contenedor del encabezado (20)
- `image_src`: Ruta de la imagen del encabezado
- `image_fit`: Ajuste de imagen (COVER)
- `width`: Ancho del contenedor (1300)
- `height`: Altura del encabezado (250)
- `margin`: Margen inferior (10)
- `marcas_id`: Diccionario para IDs de marcas
- `modelo_id`: Diccionario para IDs de modelos
- `alertacoches`: Instancia de AlertaCoches
- Controles UI varios (dropdown_marca, dropdown_modelo, etc.)

#### Función navigationBar

Crea una barra de navegación para cambiar entre vistas.

**Parámetros:**

- `page (ft.Page)`: Objeto de la página

**Descripción:**

- Cinco destinos de navegación:
  - Inicio
  - Favoritos
  - Recientes
  - Conéctate
  - Notificaciones
- Manejo de navegación mediante `handle_navigation_change`

**Métodos:**

- `__init__(self, page, alerta)`: Inicializa el encabezado
- `execute_load_filtered_results(self, e)`: Carga resultados filtrados
- `update_controls(self)`: Ajusta controles según tamaño de pantalla
- `open_modal(self, e)`: Abre modal de filtros
- `close_modal(self, e)`: Cierra modal de filtros

#### Clase RangeSliderFliters

Esta clase personalizada hereda de ft.RangeSlider para crear controles de rango que permiten seleccionar valores mínimos y máximos. Los controles de RangeSlider son útiles para el filtrado de datos numéricos como precios, kilometraje y potencia.

**Atributos:**

- `start_value` y `end_value`: valores iniciales y finales del rango
- `min` y `max`: definen los límites del rango permitido
- `divisions`: segmenta el control de rango
- `on_change`: método de manejo de eventos para actualizar el valor mostrado según el rango seleccionado
- `data`: tipo de filtro (por ejemplo, "precio" o "km")

#### Clase CardContainer

CardContainer se encarga de mostrar cada coche en una "tarjeta" visual con imagen, precio y ubicación.

**Atributos:**

- `titulo`: título del coche
- `precio`: precio del coche
- `imagen`: URL de la imagen del coche
- `ubicacion`: ubicación geográfica del coche

**Métodos:**

- Configura la visualización de la tarjeta con los datos anteriores y muestra los controles de ft.Container con iconos y texto relevante

### main.py

#### Función main

Punto de entrada de la aplicación.

**Parámetros:**

- `page (ft.Page)`: Objeto de la página

**Descripción:**

- Configura propiedades de la página
- Crea barra de navegación
- Inicializa AlertaCochesApp
- Maneja eventos de redimensionamiento

## 3. Flujo de Funcionamiento

1. **Inicialización de la Aplicación**
   - Inicio en main.py
   - Configuración de página principal
   - Creación de barra de navegación
   - Manejo de navegación

2. **Configuración de la Página Principal**
   - Creación de instancias (Header, AlertaCochesApp)
   - Construcción de contenido principal

3. **Componentes del Encabezado**
   - Configuración de controles de filtrado
   - Gestión de modal de filtros avanzados
   - Manejo de eventos de filtrado

4. **Interacción con la API y Filtrado de Datos**
   - Carga de datos (cambios, combustibles, provincias)
   - Gestión de selección de marca/modelo
   - Sincronización de controles de rango

5. **Visualización de Resultados**
   - Presentación en tarjetas
   - Actualización de contadores
   - Gestión de visualización

6. **Manejo de Cambios de Tamaño de Pantalla**
   - Ajuste de controles
   - Adaptación responsiva

## 4. Instalación y ejecución

### Opción Docker

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
