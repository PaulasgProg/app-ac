import os
import flet as ft
from anuncio_page.Utils import load_car_information,Car,Icon_Text,load_filtered_results,Image_Text,create_container


# Constante para la fuente que se usa en toda la app
FONT_FAMILY = "Comforta"

class PaginaAnuncio(ft.Column):
    def __init__(self,page,id_coche,filters,alertacoches):
        super().__init__()
        self.pg=page
        self.turquesa = "#007C7E"
        self.scroll=ft.ScrollMode.AUTO
        self.horizontal_alignment=ft.CrossAxisAlignment.CENTER
        self.height=self.pg.height
        self.width=self.pg.width
        self.expand=True
        self.car_id=id_coche
        self.car_information=load_car_information(self.car_id) #cargamos la información del coche con respecto a su id
        self.car_instance=Car(self.car_information,filters) #Creamos instancia del coche con la informacion correspondiente
        self.filters=filters
        self.alertacoches=alertacoches

        #Boton del header que abre la ppagina web de procedencia del anuncio
        button_header=ft.Container(border=ft.border.all(width=1,color=self.turquesa),
                    content=ft.Row([ft.Icon(ft.icons.OPEN_IN_BROWSER),ft.Text(value=f"ver en {self.car_instance.domain_name}".upper(),color=self.turquesa, font_family=FONT_FAMILY)])
                    ,shadow=ft.BoxShadow(color="grey",blur_radius=4,spread_radius=1),
                    on_hover=self.handle_on_hover,
                    bgcolor="white",
                    padding=ft.padding.only(left=10,right=10,top=5,bottom=5),
                    on_click=self.open_website 
                    )

        self.header=ft.Container(bgcolor="white",alignment=ft.alignment.center,padding=ft.padding.only(left=300,right=300,bottom=15,top=15),
            content=ft.Row(expand=True,controls=[
            ft.Column(controls=[ft.Row(controls=[
                ft.Container(image_src=os.path.join("images", "logo.png"),border_radius=10,image_fit=ft.ImageFit.CONTAIN,height=40,width=40,on_click=self.back_to_home),
                ft.Container(image_src="//alertacoches.png",height=50,width=200,image_fit=ft.ImageFit.FILL,on_click=self.back_to_home)
            ])]),
            ft.Column(controls=[button_header])
        ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN),shadow=ft.BoxShadow(color="grey",blur_radius=8,spread_radius=2),width=self.pg.width)

        self.imagen_principal=ft.Container(image_src=self.car_instance.images[0],image_fit=ft.ImageFit.CONTAIN,width=800,height=500)


        self.fila_imagenes=ft.Container(bgcolor=ft.colors.GREY_200,alignment=ft.alignment.center,
                                content=ft.Row(alignment=ft.MainAxisAlignment.CENTER,scroll=ft.ScrollMode.AUTO,
                                controls=[ft.Image(src=i,fit=ft.ImageFit.SCALE_DOWN,width=100,height=100) for i in self.car_instance.images]))

        fila_precio_iconos=ft.Container(
                                content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN,controls=[
                                    ft.Column(controls=[ft.Text(f"{self.car_instance.price}€",size=24,weight=ft.FontWeight.BOLD,color="red", font_family=FONT_FAMILY)]),
                                    ft.Column(controls=[
                                        ft.Row(
                                            controls=[
                                        ft.Container(content=ft.Image(src="/twitter.png",width=20,height=20,fit=ft.ImageFit.SCALE_DOWN),width=40,height=40,bgcolor="blue",border_radius=5),
                                        ft.Container(content=ft.Icon(ft.icons.FACEBOOK_OUTLINED),width=40,height=40,bgcolor="blue",border_radius=5),
                                        ft.Container(content=ft.Image(src="/wpp.png",fit=ft.ImageFit.FIT_WIDTH),width=40,height=40,bgcolor="green",border_radius=5,padding=10)
                                        ]),
                                    ])
                                ]))
        marca_coche=ft.Row(controls=[ft.Text(self.car_instance.title,color=self.turquesa,size=20, font_family=FONT_FAMILY)])
        texto_informacion=ft.Row(controls=[ft.Text("INFORMACIÓN DEL COCHE",size=20,weight=ft.FontWeight.BOLD,color=self.turquesa, font_family=FONT_FAMILY)])

        informacion_coche=ft.Column(controls=[
            ft.Row(controls=[
                Icon_Text(ft.icons.CALENDAR_TODAY,self.car_instance.year),
                Image_Text("/ruta.png",f"{self.car_instance.km}kms"),
                Image_Text("/gasolina.png",self.car_instance.fuel),
                Image_Text("/motor.png",f"{self.car_instance.cv}CV"),
                Image_Text("/cambio_marchas.png","Automático" if self.car_instance.gear_type=="at" else "Manual")
            ],alignment=ft.MainAxisAlignment.SPACE_EVENLY),
            ft.Divider(),
            ft.Row(controls=[
                ft.Icon(ft.icons.TIMER_OUTLINED),
                ft.Text(f"Publicado el {self.car_instance.date}", font_family=FONT_FAMILY)
            ],expand=True,alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(),
            ft.Row(controls=[
                ft.Icon(ft.icons.LOCATION_ON,color=self.turquesa),
                ft.Text(f"{self.car_instance.city_name} {self.car_instance.zip_code}, {self.car_instance.province}", font_family=FONT_FAMILY)
            ],expand=True,alignment=ft.MainAxisAlignment.CENTER)
        ],horizontal_alignment=ft.CrossAxisAlignment.CENTER,expand=True)

        mapa=ft.Column([ft.Container(expand=True,border_radius=20,width=600,height=300,image_src="/captura_maps.jpg",image_fit=ft.ImageFit.FIT_WIDTH)])
        fila_info_coche=ft.ResponsiveRow(controls=[
            ft.Column([informacion_coche],col={"sm":6}),
            ft.Column([mapa],col={"sm":6})
            ],expand=True)

        container_informe=create_container(titulo="INFORME DEL ESTADO DEL COCHE",
                        descripcion="¡Compra tu próximo coche con confianza! Descubre la historia completa del vehículo con el informe de Carfax. Evita sorpresas desagradables y toma decisiones informadas. ¡Obtén tu informe ahora para una compra segura y sin riesgos!",
                        color=ft.colors.GREY_900,texto_boton="VER EL HISTORIAL",icono="/carfax.png",page=self.pg)
        container_perito=create_container(titulo="REVÍSALO CON UN PERITO ESPECIALIZADO",
                        descripcion="Solicita una revisión detallada del estado real del vehículo antes de comprarlo. Compra con seguridad",
                        texto_boton="SOLICITAR PRESUPUESTO DE LA REVISIÓN",color=self.turquesa,icono="/revisamostucoche.png",page=self.pg)
        fila_containers=ft.ResponsiveRow(controls=[
            ft.Column([container_perito],col={"sm": 6}),
            ft.Column([container_informe],col={"sm": 6})
            ],expand=True)
        texto_coches_similares=ft.Row(controls=[ft.Text("COCHES SIMILARES A ESTE",size=20,weight=ft.FontWeight.BOLD,color=self.turquesa, font_family=FONT_FAMILY)])
         #plantilla para los resultados
        self.results_container = ft.Column(scroll="auto", expand=True) 
        self.images=ft.GridView(
                expand=1,
                runs_count=2 if self.pg.width<900 else 4,
                child_aspect_ratio=0.65 if self.pg.width > 900 else 0.55,
                spacing=5,
                run_spacing=30,
                max_extent=300 if self.pg.width>900 else self.pg.width // 2 - 20,  # Ajusta el tamaño de las celdas
            )


        self.container=ft.Container(content=ft.Column(
            [
                self.imagen_principal,
                self.fila_imagenes,
                fila_precio_iconos,
                marca_coche,
                texto_informacion,
                fila_info_coche,
                fila_containers,
                texto_coches_similares,
                self.results_container
            ],horizontal_alignment=ft.CrossAxisAlignment.CENTER,width=self.width,
        ),padding=ft.padding.only(left=300,right=300),alignment=ft.alignment.center,width=self.width,expand=True)

        self.controls=[self.header,self.container]
        load_filtered_results(self.filters,self)
        self.update_controls(None)
        self.pg.on_resize=self.update_controls

    def update_controls(self,e):
            if self.pg.width > 900:
                self.container.padding=ft.padding.only(left=300,right=300)
                self.imagen_principal.width=800
                self.imagen_principal.height=500
                self.fila_imagenes.width=None
                self.header.padding=ft.padding.only(left=300,right=300,bottom=15,top=15)
                self.header.content.controls[0].controls[0].controls=[
                    ft.Container(image_src=os.path.join("images", "logo.png"),border_radius=10,image_fit=ft.ImageFit.FIT_WIDTH,height=40,width=40,on_click=self.back_to_home),
                    ft.Container(image_src="//alertacoches.png",height=50,width=200,image_fit=ft.ImageFit.FILL,on_click=self.back_to_home)
                ]
            else:
                self.container.padding=ft.padding.all(5)
                self.imagen_principal.width=self.pg.width
                self.imagen_principal.height=300
                self.fila_imagenes.width=self.pg.width
                self.header.padding=ft.padding.only(left=15,right=10,bottom=15,top=30)
                # Añadir un nuevo control para que solo aparezca el logo
                self.header.content.controls[0].controls[0].controls = [ft.Container(image_src="//alertacoches_logo.jpeg",border_radius=10,image_fit=ft.ImageFit.CONTAIN,height=40,width=40,on_click=self.back_to_home)]
            #self.update()
            self.pg.update()

    

    def handle_on_hover(self,e):
        e.control.elevation=8 if e.data == "true" else 0
        e.control.shadow=ft.BoxShadow(color="grey",blur_radius=8,spread_radius=2) if e.data == "true" else ft.BoxShadow(color="grey",blur_radius=4,spread_radius=1)
        e.control.update()
    # Definir la función que se ejecutará al hacer clic en el botón
    def open_website(self,e):
        print(self.car_instance.link)
        self.pg.launch_url(self.car_instance.link)
    def back_to_home(self,e):
        from mainpage_menu.Utils import create_mainpage
        self.pg.clean()
        self.pg.update()
        create_mainpage(self.pg,None)