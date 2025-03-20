import datetime
import flet as ft

FONT_FAMILY = "Comforta"
class CirculoContainer(ft.Stack):
    def __init__(self):
        super().__init__()
        self.turquesa = "#007C7E"

        circulo_turquesa=ft.Container(border_radius=50,height=15,width=15,bgcolor=self.turquesa)
        circulo_gris=ft.Container(border_radius=50,height=20,width=20,bgcolor=ft.colors.GREY_400)

        self.controls=[circulo_gris,
                    circulo_turquesa]
        self.alignment=ft.alignment.center
class LineaContainer(ft.Container):
    def __init__(self,height):
        super().__init__()
        self.bgcolor=ft.colors.GREY_300
        self.width=2
        self.expand=True
        self.height=height
class LineaTemporal(ft.Container):
    def __init__(self,filters, page):
        super().__init__()
        tiempo=filters.get("date","Desconocido")
        self.alignment=ft.alignment.center

        if tiempo == "Desconocido":
            print("Fecha desconocida")
        else:
            # Asegúrate de que el valor es un datetime
            if isinstance(tiempo, datetime.datetime):
                fecha_obj = tiempo  # Si ya es un datetime, úsalo directamente
            elif isinstance(tiempo, str):  # Si es una cadena, conviértela
                fecha_obj = datetime.datetime.strptime(tiempo, "%Y-%m-%d %H:%M:%S.%f")
            else:
                raise ValueError("Formato de tiempo no reconocido")
        # Fecha actual para comparación
        fecha_actual = datetime.datetime.now()

        # Calcular la diferencia
        diferencia = fecha_actual - fecha_obj
        # Desglose en días, horas, minutos y segundos
        dias = diferencia.days
        horas, resto_segundos = divmod(diferencia.seconds, 3600)
        minutos, segundos = divmod(resto_segundos, 60)

        self.texto_tiempo=""
        if dias!=0:
            self.texto_tiempo=f"Hace {dias} días"
        elif horas!=0:
            self.texto_tiempo=f"Hace {horas} horas"
        else:
            self.texto_tiempo=f"Hace {minutos} mins"
        self.turquesa = "#007C7E"

        tiempo_punto=ft.Stack(controls=[
            LineaContainer(250),
            CirculoContainer()
        ],alignment=ft.alignment.center)

        fila=ft.Row(controls=[
            ft.Text(self.texto_tiempo,color=self.turquesa,font_family=FONT_FAMILY,width=60,overflow="visible",max_lines=2,text_align=ft.TextAlign("center")),
            tiempo_punto
        ],alignment=ft.MainAxisAlignment.CENTER,spacing=20 if page.width>900 else 0)

        self.content=ft.Row(controls=[
            fila,
            CardContainer(filters,page)
        ],spacing=20)

class CardContainer(ft.Card):
    def __init__(self,filters, page):
        super().__init__()
        self.page = page
        self.turquesa = "#007C7E"
        self.width = 500 if self.page.width > 900 else 270
        self.height = 200
        padding=ft.padding.only(left=20, right=20, top=30, bottom=30)
        self.border_radius=20
        self.bgcolor=ft.colors.GREY_50
        self.elevation=4
        self.filters=filters

        marca = filters.get("make") or "Cualquiera marca o modelo"
        modelo=filters.get("model") or ""

        text_marca_modelo=f'{marca} {modelo}'
        rango_precios=f'Entre {filters.get("minprice","0")}€ y {filters.get("maxprice","Desconocido")}€'
        rango_matricula=f'Matriculados entre el {filters.get("minyear","0")} y {filters.get("maxyear","Desconocido")}'
        rango_km=f'Entre el {filters.get("minmileage","0")} y {filters.get("maxmileage","Desconocido")}'
        geartype=filters.get("geartype","Desconocido")
        fueltype=filters.get("fueltype","Desconocido")

        self.content = ft.Container(content=ft.Column(controls=[
            ft.Text(text_marca_modelo, font_family=FONT_FAMILY,color=self.turquesa,weight="bold",size=12),
            ft.Text(rango_precios, font_family=FONT_FAMILY,color=self.turquesa,size=12),
            ft.Text(rango_matricula, font_family=FONT_FAMILY,color=self.turquesa,size=12),
            ft.Text(rango_km, font_family=FONT_FAMILY,color=self.turquesa,size=12),

        ],alignment=ft.MainAxisAlignment.CENTER,spacing=5),padding=padding,on_click=self.back_to_home)
        if geartype!="Desconocido":
            self.content.content.controls.append(ft.Text(geartype,font_family=FONT_FAMILY,color=self.turquesa,size=12))
        if fueltype!="Desconocido":
            self.content.content.controls.append(ft.Text(fueltype,font_family=FONT_FAMILY,color=self.turquesa,size=12))
    def back_to_home(self, e):
        """
        Regresa a la página principal.
        """
        from mainpage_menu.Utils import create_mainpage
        self.page.clean()
        self.page.update()
        create_mainpage(self.page,self.filters)
