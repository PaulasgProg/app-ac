import asyncio
from datetime import datetime
import json
import os
import flet as ft
import httpx
import requests
import tldextract
from mainpage_menu.Utils import RangeSliderFilters, CardContainer

# Constante para la fuente que se usa en toda la app
FONT_FAMILY = "Comforta"


class AlertaCochesApp(ft.Column):  # Filtro y contenido generado por los filtros
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.marcas_id = {}
        self.modelo_id = {}
        self.provincias = {}
        self.combustible = {}
        self.orden = {}
        self.cambio = {}
        self.is_loading = False  # Bandera para evitar cargar múltiples veces
        self.onlyone = True
        self.expand = True
        turquoise_color = "#007C7E"
        self.filename = "recientes.json"
        async def setup():
            await self.get_searchs()

        asyncio.run(setup())

        self.dropdown_marca = ft.Dropdown(
            label="Marca",
            hint_text="Marca",
            width=180, border_radius=10,
            data="Marca",
            on_change=self.load_filters_modelo,
            elevation=10, content_padding=ft.padding.only(bottom=25, top=25, left=20, right=10),
            text_style=ft.TextStyle(
                font_family=FONT_FAMILY, color=ft.colors.GREY_800),
            label_style=ft.TextStyle(font_family=FONT_FAMILY)

        )
        self.dropdown_modelo = ft.Dropdown(
            label="Modelo",
            hint_text="Modelo",
            border_radius=10, width=160, data="Modelo",
            disabled=True,
            on_change=self.load_coches,
            text_style=ft.TextStyle(
                font_family=FONT_FAMILY, color=ft.colors.GREY_800),
            label_style=ft.TextStyle(font_family=FONT_FAMILY),
            elevation=10, content_padding=ft.padding.only(bottom=25, top=25, left=20, right=10))

        self.dropdown_provincias = ft.Dropdown(label="Provincia", text_style=ft.TextStyle(
            font_family=FONT_FAMILY, color=ft.colors.GREY_800), label_style=ft.TextStyle(font_family=FONT_FAMILY),data="province",on_change=self.drop_changing)

        self.dropdown_combustible = ft.Dropdown(
            label="Combustible", text_style=ft.TextStyle(
                font_family=FONT_FAMILY, color=ft.colors.GREY_800), label_style=ft.TextStyle(font_family=FONT_FAMILY),data="fuel",on_change=self.drop_changing)

        self.dropdown_cambio = ft.Dropdown(label="Cambio", text_style=ft.TextStyle(
                        font_family=FONT_FAMILY, color=ft.colors.GREY_800), label_style=ft.TextStyle(font_family=FONT_FAMILY),data="gear",on_change=self.drop_changing)

        self.dropdown_ordenar=ft.Dropdown(value="Precios más bajos",border=None,border_color=ft.colors.TRANSPARENT,filled=True,bgcolor=ft.colors.GREY_100,content_padding=0,color="grey",text_size=12,
                                        text_style=ft.TextStyle(font_family=FONT_FAMILY, color=ft.colors.GREY_800),data="orden",on_change=self.drop_changing,width=180)


        self.recientes = ft.FilledButton(
            text="Publicados hace",
            icon=ft.icons.TIMER_OUTLINED,
            style=ft.ButtonStyle(
                bgcolor=ft.colors.GREY_100,
                shadow_color=ft.colors.GREY,
                color="black",
                elevation=4,
                # Reduced border radius for less rounded corners
                shape=ft.RoundedRectangleBorder(10),
                padding=ft.padding.only(
                    top=18, bottom=18, left=15, right=20),  # Increases height
                text_style=ft.TextStyle(font_family=FONT_FAMILY)
            ), height=70
        )
        self.open_modal_button = ft.FilledButton(text="Más filtros",
                                                 icon=ft.icons.SETTINGS,
                                                 on_click=self.open_modal,
                                                 style=ft.ButtonStyle(bgcolor=ft.colors.GREY_100,
                                                                      shadow_color=ft.colors.GREY,
                                                                      color="black",
                                                                      elevation=4,
                                                                      # Reduced border radius for less rounded corners
                                                                      shape=ft.RoundedRectangleBorder(
                                                                          10),
                                                                      padding=ft.padding.only(top=18, bottom=18, left=15, right=15), text_style=ft.TextStyle(font_family=FONT_FAMILY)
                                                                      ), height=70)

        # SLIDER DE RANGO,creado en COMPONENTES,se especifica el inicio y el fin, y el min y el max.Creamos uno para cada caracterisitca
        self.rango_matriculacion = RangeSliderFilters(
            1970, 2024, 1900, 2024, self.slider_is_changing, "matricula")
        self.rango_precios = RangeSliderFilters(
            750, 200000, 750, 200000, self.slider_is_changing, "precio")
        self.rango_km = RangeSliderFilters(
            1, 950000, 1, 950000, self.slider_is_changing, "km")
        self.rango_potencia = RangeSliderFilters(
            1, 1200, 1, 1200, self.slider_is_changing, "potencia")

        # textfields para la ventana modal, con cada cambio de numero se modifica tanto en el campo de texto como en el slider
        self.text_field_min = ft.TextField(label="Año desde", text_style=ft.TextStyle(font_family=FONT_FAMILY), label_style=ft.TextStyle(
            font_family=FONT_FAMILY), expand=True, value=str(self.rango_matriculacion.start_value), on_change=self.text_is_changing, data="matricula_min")

        self.text_field_max = ft.TextField(label="Año hasta", text_style=ft.TextStyle(font_family=FONT_FAMILY), label_style=ft.TextStyle(
            font_family=FONT_FAMILY), expand=True, value=str(
            self.rango_matriculacion.end_value), on_change=self.text_is_changing, data="matricula_max")

        self.text_field_min_precio = ft.TextField(label="Precio desde", text_style=ft.TextStyle(font_family=FONT_FAMILY), label_style=ft.TextStyle(
            font_family=FONT_FAMILY), expand=True, value=str(
            self.rango_precios.start_value), on_change=self.text_is_changing, data="precio_min")

        self.text_field_max_precio = ft.TextField(label="Precio hasta", text_style=ft.TextStyle(font_family=FONT_FAMILY), label_style=ft.TextStyle(
            font_family=FONT_FAMILY), expand=True, value=str(
            self.rango_precios.end_value), on_change=self.text_is_changing, data="precio_max")

        self.text_field_min_km = ft.TextField(label="Desde", text_style=ft.TextStyle(font_family=FONT_FAMILY), label_style=ft.TextStyle(
            font_family=FONT_FAMILY), expand=True, value=str(
            self.rango_km.start_value), on_change=self.text_is_changing, data="km_min")

        self.text_field_max_km = ft.TextField(label="Hasta", text_style=ft.TextStyle(font_family=FONT_FAMILY), label_style=ft.TextStyle(
            font_family=FONT_FAMILY), expand=True, value=str(
            self.rango_km.end_value), on_change=self.text_is_changing, data="km_max")

        self.text_field_min_pot = ft.TextField(label="Desde", text_style=ft.TextStyle(font_family=FONT_FAMILY), label_style=ft.TextStyle(
            font_family=FONT_FAMILY), expand=True, value=str(
            self.rango_potencia.start_value), on_change=self.text_is_changing, data="potencia_min")

        self.text_field_max_pot = ft.TextField(label="Hasta", text_style=ft.TextStyle(font_family=FONT_FAMILY), label_style=ft.TextStyle(
            font_family=FONT_FAMILY), expand=True, value=str(
            self.rango_potencia.end_value), on_change=self.text_is_changing, data="potencia_max")

        self.boton_modal = ft.FilledButton(
            data="button",
            text="Ver todo",
            icon="search",
            on_click=self.load_filtered_results,
            style=ft.ButtonStyle(
                bgcolor=turquoise_color,
                elevation=4,
                text_style=ft.TextStyle(font_family=FONT_FAMILY),
                shape=ft.RoundedRectangleBorder(5)), height=70)
        # VENTANA MODAL DE MAS  FILTROS
        self.modal = ft.AlertDialog(
            title=ft.Text("Filtros avanzados", font_family=FONT_FAMILY),
            content=ft.Column(
                [
                    ft.Text("Fecha de matriculación", font_family=FONT_FAMILY),
                    self.rango_matriculacion,
                    ft.Row(controls=[self.text_field_min,
                           self.text_field_max], expand=True),
                    ft.Divider(),
                    ft.Text("Rango de precios", font_family=FONT_FAMILY),
                    self.rango_precios,
                    ft.Row(controls=[self.text_field_min_precio,
                           self.text_field_max_precio], expand=True),
                    ft.Divider(),
                    self.dropdown_provincias,
                    ft.Divider(),
                    ft.Text("Rango kilometraje", font_family=FONT_FAMILY),
                    self.rango_km,
                    ft.Row(controls=[self.text_field_min_km,
                           self.text_field_max_km], expand=True),
                    ft.Divider(),
                    ft.Text("Potencia", font_family=FONT_FAMILY),
                    self.rango_potencia,
                    ft.Row(controls=[self.text_field_min_pot,
                           self.text_field_max_pot], expand=True),
                    ft.Divider(),
                    self.dropdown_combustible,
                    self.dropdown_cambio,
                ], scroll=ft.ScrollMode.AUTO, expand=True, width=800
            ),
            actions=[
                ft.ElevatedButton(
                    "Cerrar", on_click=self.close_modal), self.boton_modal

            ]
        )

        # Inicialización de los filtros
        self.min_price = f"{self.rango_precios.start_value}"
        self.max_price = f"{self.rango_precios.end_value}"
        self.min_year = f"{self.rango_matriculacion.start_value}"
        self.max_year = f"{self.rango_matriculacion.end_value}"
        self.min_mileage = f"{self.rango_km.start_value}"
        self.max_mileage = f"{self.rango_km.end_value}"
        self.min_power = f"{self.rango_potencia.start_value}"
        self.max_power = f"{self.rango_potencia.end_value}"
        self.geartype=None
        self.fueltype=None
        self.province=None
        self.orderby=34
        self.page_input = 1
        self.per_page = 20

        self.filters = self.getFilters()  # obtenemos filtros

        # CARGAMOS DE LA API LOS DATOS DE MARCA, PROVINCIAS, CAMBIO Y COMBUSTIBLE
        self.load_filters_marca()
        # Para cargar las opciones de cambio
        self.fetch_data("https://api.alertacoches.es/api/filter/14", filters=self.getFilters(),
                        dropdown=self.dropdown_cambio, options_dict=self.cambio)
        # Para cargar las opciones de combustible
        self.fetch_data("https://api.alertacoches.es/api/filter/15", filters=self.getFilters(),
                        dropdown=self.dropdown_combustible, options_dict=self.combustible)
        # Para cargar las opciones de provincias
        self.fetch_data("https://api.alertacoches.es/api/filter/13", filters=self.getFilters(),
                        dropdown=self.dropdown_provincias, options_dict=self.provincias)
        # Para cargar las opciones de orden
        self.fetch_data("https://api.alertacoches.es/api/filter/3", filters=self.getFilters(),
                        dropdown=self.dropdown_ordenar, options_dict=self.orden)

        # Botón de búsqueda y contenedor de resultados
        self.search_button = ft.FilledButton(
            data="button",
            text="Ver todo",
            icon="search",
            on_click=self.load_filtered_results,
            style=ft.ButtonStyle(
                bgcolor=turquoise_color,
                elevation=4,
                text_style=ft.TextStyle(font_family=FONT_FAMILY, size=14),
                shape=ft.RoundedRectangleBorder(5)), height=70)
        self.results_container = ft.Column(expand=True)
        #self.width = 1300

        # plantilla para los resultados
        self.images = ft.GridView(
            expand=1,
            runs_count=2 if self.page.width<900 else 4,
            child_aspect_ratio=0.65 if self.page.width > 900 else 0.55,
            spacing=5,
            run_spacing=30,
            max_extent=300 if self.page.width>900 else self.page.width // 2 - 20,
        )

        # elementos de filtros
        self.container_filtro = ft.Row(controls=[
            ft.Column(controls=[
                ft.Row([self.dropdown_marca, self.dropdown_modelo, self.recientes, self.open_modal_button])]),
            ft.Column(controls=[
                ft.Row(controls=[self.search_button])])
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        self.controls=[ft.Container(ft.Column(expand=True),margin=ft.margin.only(left=600,right=300),expand=True)]
    # si la pantalla es mayor que 900 se añade la fila de filtros, si no no
    def update_controls(self):
        if self.page.width > 1600:

            self.controls[0].margin=ft.margin.only(left=300,right=300)
            self.controls[0].content.controls =[
                self.container_filtro,
                ft.Container(height=10),
                ft.Row(controls=[ft.Column([
                    ft.Container(content=ft.Text("Ordenar",font_family=FONT_FAMILY)),
                    self.dropdown_ordenar],
                    spacing=0)],
                    alignment=ft.MainAxisAlignment.END),
                ft.Text("LO QUE HEMOS ENCONTRADO PARA TI",
                        weight=ft.FontWeight.BOLD, size=22),
                ft.Container(height=10),
                self.results_container
            ]
        elif self.page.width <1600 and self.page.width>900:
            self.controls[0].margin=ft.margin.only(left=200,right=200)
            self.controls[0].content.controls =[
                self.container_filtro,
                ft.Container(height=10),
                ft.Row(controls=[ft.Column([
                    ft.Container(content=ft.Text("Ordenar",font_family=FONT_FAMILY)),
                    self.dropdown_ordenar],
                    spacing=0)],
                    alignment=ft.MainAxisAlignment.END),
                ft.Text("LO QUE HEMOS ENCONTRADO PARA TI",
                        weight=ft.FontWeight.BOLD, size=22),
                ft.Container(height=10),
                self.results_container
            ]
        else:
            self.controls[0].margin=2
            self.controls[0].content.controls = [
                ft.Container(height=5),
                ft.Text("COCHES DE OCASIÓN RECIENTES",
                        weight=ft.FontWeight.BOLD, size=18, font_family=FONT_FAMILY),
                ft.Container(height=5),
                ft.Text("Los últimos anuncios que hemos encontrado",
                        weight=ft.FontWeight.BOLD, size=12, font_family=FONT_FAMILY),
                ft.Container(height=5),
                self.results_container]
        self.update()
        self.page.update()

    def update_filters(self, e=None):
        """
        Configura los filtros y actualiza el estado de los rangos seleccionados.
        """
        if e and e.control.data == "button":
            self.page_input = 1
        if self.is_loading:
            return
        self.is_loading = True

        if self.modal.open:
            self.min_price = int(self.rango_precios.start_value)
            self.max_price = int(self.rango_precios.end_value)
            self.min_year = int(self.rango_matriculacion.start_value)
            self.max_year = int(self.rango_matriculacion.end_value)
            self.min_mileage = int(self.rango_km.start_value)
            self.max_mileage = int(self.rango_km.end_value)
            self.min_power = int(self.rango_potencia.start_value)
            self.max_power = int(self.rango_potencia.end_value)
            self.page_input = 1
            self.per_page = 20

            self.modal.open = False
            self.page.update()
        # Cierra el modal y actualiza el estado en la interfaz
        self.close_modal(e)

    def getFilters(self):  # creamos los filtros de busqueda
        filters = {
            'make': self.getIdMarca(),
            'model': self.getIdModelo(),
            "minprice": self.min_price,
            "maxprice": self.max_price,
            "minyear": self.min_year,
            "maxyear": self.max_year,
            "minmileage": self.min_mileage,
            "maxmileage": self.max_mileage,
            "minpower": self.min_power,
            "maxpower": self.max_power,
            "geartype": self.geartype,
            "fueltype": self.fueltype,
            "province":self.province,
            "orderby":self.orderby,
            "page": self.page_input,
            "perpage": self.per_page
        }
        return filters
    def getFiltersRecientes(self):  # creamos los filtros de busqueda
        filters = {
            'make': self.dropdown_marca.value,
            'model': self.dropdown_modelo.value,
            "minprice": self.min_price,
            "maxprice": self.max_price,
            "minyear": self.min_year,
            "maxyear": self.max_year,
            "minmileage": self.min_mileage,
            "maxmileage": self.max_mileage,
            "minpower": self.min_power,
            "maxpower": self.max_power,
            "geartype": self.dropdown_cambio.value,
            "fueltype": self.dropdown_combustible.value,
            "province":self.dropdown_provincias.value,
            "orderby":self.orderby,
            "page": self.page_input,
            "perpage": self.per_page
        }
        return filters

    def getIdMarca(self):  # obtenemos el id de la marca
        if self.dropdown_marca.value:
            marca_dropdown = self.dropdown_marca.value
            id_marca = self.marcas_id[f"{marca_dropdown}"]
        else:
            id_marca = None
        return id_marca

    def getIdModelo(self):  # obtenemos el id del modelo
        if self.dropdown_modelo.value:
            modelo_dropdown = self.dropdown_modelo.value
            id_modelo = self.modelo_id[f"{modelo_dropdown}"]
        else:
            id_modelo = None
        return id_modelo

    def fetch_data(self, endpoint, filters=None, dropdown=None, options_dict=None, update_button_text=False, display_results=False, reset_dropdown=False):
        """
        Función genérica para hacer solicitudes a la API, que puede cargar opciones en dropdowns, contar coches o cargar resultados.

        Args:
        - endpoint (str): URL del endpoint para la solicitud.
        - filters (dict, opcional): Parámetros de filtro para la solicitud.
        - dropdown (Dropdown, opcional): Componente dropdown al que añadir las opciones.
        - options_dict (dict, opcional): Diccionario para almacenar las opciones.
        - update_button_text (bool, opcional): Si es True, actualizará el texto del botón con el conteo de coches.
        - display_results (bool, opcional): Si es True, mostrará los resultados en pantalla.
        - reset_dropdown (bool, opcional): Si es True, vacía el dropdown antes de cargar opciones.
        """
        try:
            response = requests.get(endpoint, params=filters)
            response.raise_for_status()
            data = response.json()
            print("Datos de la API:", data)

            # Si es un dropdown, cargar opciones
            if dropdown and options_dict is not None:
                if reset_dropdown:
                    # Reseteamos el diccionario cada vez que cambia de opcion el dropdown de marcas
                    options_dict.clear()
                    dropdown.options.clear()  # Limpia el dropdown si es necesario
                    dropdown.disabled = False
                for item in data:
                    dropdown.options.append(ft.dropdown.Option(
                        item.get("short_desc", "Desconocido")))
                    options_dict[item.get("short_desc")] = item.get("value_id")
                self.page.update()

            # Si es para contar coches
            elif update_button_text:
                count = data.get("count", 0)
                self.boton_modal.text = f"Ver {count} coches"
                self.search_button.text = f"Ver {count} coches"
                return count  # Devuelve el conteo

            # Si es para mostrar los resultados en pantalla
            elif display_results:
                self.display_results(data)

        except requests.RequestException as error:
            print("Error al cargar datos:", error)
        finally:
            self.is_loading = False

    # cuenta el numero de coches disponibles para los filtros correspondientes
    def load_coches(self, e):
        # Para contar los coches con filtros aplicados
        self.fetch_data("https://api.alertacoches.es/api/search/count",
                        filters=self.getFilters(), update_button_text=True)
        self.update()
        self.page.update()

    def load_filters_modelo(self, e):
        """
        Carga los modelos disponibles según la marca seleccionada.
        """
        self.dropdown_modelo.value = None
        self.update_filters(e)  # Prepara los filtros y el estado inicial
        # Resetea el dropdown de modelos y actualiza el conteo de coches
        self.fetch_data("https://api.alertacoches.es/api/search/count",
                        filters=self.getFilters(), update_button_text=True)

        # Carga los modelos según la marca seleccionada
        filters = {"parentValueId": self.getIdMarca()}
        self.fetch_data(
            "https://api.alertacoches.es/api/filter/2/",
            filters=filters,
            dropdown=self.dropdown_modelo,
            options_dict=self.modelo_id,
            reset_dropdown=True
        )
        self.update()

    def load_filters_marca(self):  # carga las marcas de coche
        """
        Carga las marcas de coches y las agrega al dropdown correspondiente.
        """
        self.fetch_data(
            "https://api.alertacoches.es/api/filter/1",
            filters=self.getFilters(),
            dropdown=self.dropdown_marca,
            options_dict=self.marcas_id,
            reset_dropdown=True
        )

    def load_filtered_results(self, e=None):
        """
        Carga los coches disponibles con los filtros seleccionados y muestra los resultados en pantalla.
        """
        if e is not None:
            self.close_modal(e)
            if e.control.data == "button":  # ponemos el input page de los filtros a uno para primeras busquedas
                self.page_input = 1
        if self.is_loading:  # Previene múltiples cargas al mismo tiempo al hacer scroll
            return
        self.is_loading = True
        self.update_filters(e)  # Prepara los filtros y el estado inicial
        filters = self.getFilters()

        # Cuenta los coches con filtros aplicados
        self.fetch_data("https://api.alertacoches.es/api/search/count",
                        filters=filters, update_button_text=True)

        # Carga y muestra los resultados filtrados en pantalla
        self.fetch_data("https://api.alertacoches.es/api/search",
                        filters=filters, display_results=True)

        print(filters)
        if self.page.auth_state.is_authenticated:
            async def setup():
                await self.save_search(self.getFiltersRecientes())
                await self.page.recientes_page.init_async()

            asyncio.run(setup())

    def display_results(self, data):  # muestra en pantalla los resultados
        # Limpiar resultados anteriores y mostrar nuevos resultados
        if self.page_input == 1:  # QUE SOLO SE LIMPIE SI SON LOS PRIMEROS DATOS DE LA BUSQUEDA
            self.results_container.controls.clear()
            self.images.controls.clear()

        for car in data.get("data", []):  # recorremos el diccionario que devuelve la api
            location = car.get("location", "Desconocido")
            city = location["city_name"]
            images = car.get("images", [])
            # Obtiene la primera imagen si la lista existe y tiene elementos
            # image_url = car.get("images",[])[0] if car.get("images") and len(car.get("images")) > 0 else None

            self.images.controls.append(  # añadimos cada carta con los datos de los coches a la gridview
                self.create_card(car=car)
            )
            # Añadir `self.images` a `results_container` si no está ya añadido
        if self.images not in self.results_container.controls:
            self.results_container.controls.append(self.images)
        if self.results_container in self.controls[0].content.controls:
            self.images.update()
            self.results_container.update()
            self.update()
        self.is_loading = False
        self.onlyone = True

    def open_modal(self, e):
        # Abrir la ventana emergente
        self.page.dialog = self.modal
        self.modal.open = True
        self.page.update()

    def close_modal(self, e):

        self.modal.open = False
        self.page.update()

    # cuando cambia el slider se modifica el textfield correspondiente
    def slider_is_changing(self, e):
        if e.control.data == "matricula":
            self.text_field_min.value = str(int(e.control.start_value))
            self.text_field_max.value = str(int(e.control.end_value))
        elif e.control.data == "km":
            self.text_field_min_km.value = str(int(e.control.start_value))
            self.text_field_max_km.value = str(int(e.control.end_value))
        elif e.control.data == "potencia":
            self.text_field_min_pot.value = str(int(e.control.start_value))
            self.text_field_max_pot.value = str(int(e.control.end_value))
        elif e.control.data == "precio":
            self.text_field_min_precio.value = str(int(e.control.start_value))
            self.text_field_max_precio.value = str(int(e.control.end_value))
        # Inicialización de los filtros
        self.min_price = int(self.rango_precios.start_value)
        self.max_price = int(self.rango_precios.end_value)
        self.min_year = int(self.rango_matriculacion.start_value)
        self.max_year = int(self.rango_matriculacion.end_value)
        self.min_mileage = int(self.rango_km.start_value)
        self.max_mileage = int(self.rango_km.end_value)
        self.min_power = int(self.rango_potencia.start_value)
        self.max_power = int(self.rango_potencia.end_value)
        self.page_input = 1
        self.per_page = 20
        self.modal.update()
        self.load_coches(None)
        self.page.update()

    # cuando cambia el textfield se  modifica el slider correspondiente
    def text_is_changing(self, e):
        if e.control.data == "matricula_min":
            self.rango_matriculacion.start_value = int(e.control.value)
        elif e.control.data == "matricula_max":
            self.rango_matriculacion.end_value = int(e.control.value)
        elif e.control.data == "km_min":
            self.rango_km.start_value = int(e.control.value)
        elif e.control.data == "km_max":
            self.rango_km.end_value = int(e.control.value)
        elif e.control.data == "potencia_min":
            self.rango_potencia.start_value = int(e.control.value)
        elif e.control.data == "potencia_max":
            self.rango_potencia.end_value = int(e.control.value)
        elif e.control.data == "precio_min":
            self.rango_precios.start_value = int(e.control.value)
        elif e.control.data == "precio_max":
            self.rango_precios.end_value = int(e.control.value)

        # Inicialización de los filtros
        self.min_price = int(self.rango_precios.start_value)
        self.max_price = int(self.rango_precios.end_value)
        self.min_year = int(self.rango_matriculacion.start_value)
        self.max_year = int(self.rango_matriculacion.end_value)
        self.min_mileage = int(self.rango_km.start_value)
        self.max_mileage = int(self.rango_km.end_value)
        self.min_power = int(self.rango_potencia.start_value)
        self.max_power = int(self.rango_potencia.end_value)
        self.page_input = 1
        self.per_page = 20
        self.load_coches(None)
        self.modal.update()
        self.page.update()

    def drop_changing(self,e):
        if e.control.data=="gear":
            if e.control.value=="Manual":
                self.geartype= int(738)
            elif e.control.value=="Automático":
                self.geartype=int(737)
        elif e.control.data=="fuel":
            if e.control.value=="Eléctrico/Híbrido":
                self.fueltype=int(743)
            elif e.control.value=="Diesel":
                self.fueltype=int(740)
            elif e.control.value=="Gasolina":
                self.fueltype=int(739)
        elif e.control.data=="orden":
            if self.dropdown_ordenar.value:
                orden_dropdown = self.dropdown_ordenar.value
                id_orden = self.orden[f"{orden_dropdown}"]
                self.orderby=int(id_orden)
            else:
                id_orden = None
        elif e.control.data=="province":
            if self.dropdown_provincias.value:
                provincia_dropdown = self.dropdown_provincias.value
                id_provincia = self.provincias[f"{provincia_dropdown}"]
                self.province=int(id_provincia)
            else:
                id_provincia = None
        self.load_coches(None)
        self.page.update()


    def handle_scroll(self, e):  # FUNCION PARA QUE CARGUEN LOS DATOS A MEDIDA QUE HACEMOS SCROLL
        # Verificamos si estamos cerca del final de la columna para cargar más datos
        if not self.is_loading and e.pixels >= e.max_scroll_extent - 200 and self.onlyone:
            self.page_input += 1
            self.onlyone = False
            print(self.page_input)
            self.load_filtered_results(None)

    def get_shared_controls(self):

        return {
            "dropdown_marca": self.dropdown_marca,
            "dropdown_modelo": self.dropdown_modelo,
            "open_modal_button": self.open_modal_button,
            "boton_modal": self.boton_modal,
            "recientes": self.recientes
        }

    def create_card(self, car):
        link = car.get("link", "Desconocido")
        # Extraer componentes de la URL
        extracted = tldextract.extract(link)
        filters = self.getFilters()

        # Verificar si el coche está en favoritos
        car_id = car.get("id", "Desconocido")
        is_favorite = False
        if hasattr(self.page, 'favorites_screen'):
            is_favorite = any(
                fav["id"] == car_id for fav in self.page.favorites_screen.favorites)

        # Combinar el subdominio, el dominio y el TLD para obtener el nombre completo
        domain_name = f"{extracted.domain}.{extracted.suffix}"
        return CardContainer(
            car.get("title", "Desconocido"),
            car.get("price", "Desconocido"),
            car.get("images", [])[0] if car.get("images") else None,
            car.get("location", "Desconocido").get("city_name", "Desconocido"),
            car.get("id", "Desconocido"),
            domain_name,
            self.page,
            filters,
            self,
            is_favorite=is_favorite
        )
    async def get_searchs(self):
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if self.page.auth_state.is_authenticated:
                        user_email = self.page.auth_state.user['email']
                        return data.get(user_email, [])
            return []
        except Exception as e:
            print(f"Error loading recientes: {e}")
            return []
    async def save_search(self,lista_filtros):
        lista_filtros["date"]=str(datetime.now())
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"http://backend:8000/api/recientes/{self.page.auth_state.user['email']}",
                    json=lista_filtros
                )

                if response.status_code == 200:
                    print("Busqueda guardada")

                else:
                    error_msg = response.json().get("detail", "Error en el registro")
                    print("No se pudo guardar la búsqueda")

        except Exception as e:
            print(f"Error en registro: {e}")

