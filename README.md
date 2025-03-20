# AlertaCoches Flet App

Este proyecto es una simulación de Alerta Coches (conectado a su API) y está creado con Flet y Docker.

[![Ver video de demostración](https://github.com/PaulasgProg/app-ac/blob/main/assets/images/imagen-presentacion.jpg)](https://github.com/PaulasgProg/app-ac/raw/main/assets/videos/video-app-demostracion.mp4)




## 1. Estructura del Proyecto

```tree
src/
├── assets/
│   └── coche.jpg
├── anuncio_page/
│   ├──PaginaAnuncio.py     # Vista del anuncio
│   └──Utils.py             # Utilidades compartidas
├── favoritos/
│   └── favoritos.py        # Vista favoritos
├── login_register/         # Módulo de autenticación
│   ├── login.py            # Vista de login
│   ├── register.py         # Vista de registro
│   ├── recoverpass.py      # Vista de recuperación
│   └── utils.py            # Utilidades compartidas
├── mainpage_menu/          # Módulo de la app principal
│   ├── PaginaPrincipal.py  # Vista principal
│   ├── Filtro_Contenido.py # Lógica de filtros
│   └── Utils.py            # Utilidades compartidas
├── profile_view/           # Módulo de la vista del perfil
│   ├── components.py       # Utilidades compartidas
│   ├── profile.py          # Vista de la página del perfil
│   └── validators.py       # Validaciones del perfil
├── recientes_page/         # Módulo de la vista de búsquedas recientes
│   ├── pagina_recientes.py # Vista página recientes
│   └── utils.py            # Utilidades compartidas
├── backend.py              # Lanzamiento servidor
└── main.py                 # Archivo principal

```

## 2. Navegación

La aplicación cuenta con una barra de navegación que incluye 5 secciones principales:

| Sección | Requisitos de Acceso |
|---------|---------------------|
| Inicio | Acceso público |
| Favoritos | Requiere autenticación |
| Recientes | Requiere autenticación |
| Conéctate/Mi perfil | Cambia según estado de autenticación |
| Alertas | Requiere autenticación |

## 3. Estados de Autenticación

### Usuario No Autenticado

- ✖️ Acceso limitado solo a la sección de Inicio
- 🔄 Redirección automática a login en páginas protegidas
- Botón "Conéctate" visible en la navegación

### Usuario Autenticado

- ✅ Acceso completo a todas las funcionalidades
- 🔄 Cambios dinámicos en la interfaz:
  - Icono: `ACCOUNT_CIRCLE` → `FACE`
  - Texto: "Conéctate" → "Mi perfil"
- Visualización de contenido personalizado


## 4. Instalación y ejecución

1. Instalar Docker Desktop
2. Abrir Docker Desktop
3. Clonar el repositorio:

   ```bash
   git clone [URL_DEL_REPOSITORIO]
   ```

4. Nos movemos al directorio de la aplicación y creamos un enlace simbólico:

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
