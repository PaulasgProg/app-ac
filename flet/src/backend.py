# backend.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

# uvicorn backend:app --reload
# Crear una instancia de FastAPI
app = FastAPI()


# Modelos de datos para autenticación
class LoginRequest(BaseModel):
    email: str
    password: str


# Modelo de datos para registro de usuario
class RegisterRequest(BaseModel):
    nombre: str
    email: str
    password: str


# Modelo de datos para actualizar usuario
class UpdateUserRequest(BaseModel):
    email: str
    nombre: str


# Modelo de datos para cambiar contraseña
class ChangePasswordRequest(BaseModel):
    email: str
    old_password: str
    new_password: str


# Modelo de datos para favoritos
class FavoriteItem(BaseModel):
    id: str
    title: str
    price: str
    images: List[str]
    location: dict
    link: str = ""


# Lista de usuarios (en memoria)
USERS = [
    {
        "email": "test@test.com",
        "password": "000000",
        "nombre": "Admin User",
        "favorites": [],
        "recientes": []
    }
]

# # Endpoints de autenticación
# @app.post("/api/login")
# async def login(request: LoginRequest):
#     user = next((user for user in USERS 
#                  if user["email"] == request.email 
#                  and user["password"] == request.password), None)
    
#     if user:
#         return {"status": "success", "user": user}
#     raise HTTPException(status_code=401, detail="Credenciales incorrectas")


# Endpoints de perfil de usuario
@app.get("/api/user/{email}")
async def get_user_profile(email: str):
    # Buscar usuario por email
    user = next((user for user in USERS if user["email"] == email), None)
    if not user:
        # Si no se encuentra, lanzar un error 404
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user  # Devolver el usuario encontrado


# Endpoint para actualizar perfil de usuario
@app.put("/api/user/update")
async def update_user_profile(request: UpdateUserRequest):
    # Buscar usuario por email
    user = next(
        (user for user in USERS if user["email"] == request.email), None)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Actualizar nombre del usuario y su email
    user["nombre"] = request.nombre
    user["email"] = request.email
    # Devolver el usuario actualizado
    return {"status": "success", "user": user}


# Endpoint para cambiar contraseña
@app.put("/api/user/change-password")
async def change_password(request: ChangePasswordRequest):
    user = next(
        (user for user in USERS if user["email"] == request.email), None)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Verificar si la contraseña actual es correcta
    if user["password"] != request.old_password:
        raise HTTPException(
            status_code=400, detail="Contraseña actual incorrecta")

    # Actualizar contraseña
    user["password"] = request.new_password
    return {"status": "success", "message": "Contraseña actualizada"}


# Endpoint para ver usuarios
# http://localhost:8000/api/users
@app.get("/api/users")
async def get_users():
    return {"users": USERS}  # Devolver todos los usuarios


# Endpoint para obtener favoritos del usuario
@app.get("/api/favorites/{email}")
async def get_favorites(email: str):
    user = next((user for user in USERS if user["email"] == email), None)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    # Devuelve la lista de favoritos del usuario
    return {"favorites": user["favorites"]}


# Endpoint para agregar favoritos
@app.post("/api/favorites/{email}")
async def add_favorite(email: str, favorite: FavoriteItem):
    user = next((user for user in USERS if user["email"] == email), None)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Verificar si el favorito ya existe
    if not any(fav["id"] == favorite.id for fav in user["favorites"]):
        # Si no existe, lo agrega a la lista de favoritos
        user["favorites"].append(favorite.model_dump())

    # Devuelve la lista de favoritos actualizada
    return {"status": "success", "favorites": user["favorites"]}


# Endpoint para eliminar favoritos
@app.delete("/api/favorites/{email}/{car_id}")
async def remove_favorite(email: str, car_id: str):
    user = next((user for user in USERS if user["email"] == email), None)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Filtra la lista de favoritos para eliminar el ítem especificado
    user["favorites"] = [fav for fav in user["favorites"] if fav["id"] != car_id]
    # Devuelve la lista de favoritos actualizada
    return {"status": "success", "favorites": user["favorites"]}


# Endpoint para autenticación de usuario
@app.post("/api/login")
async def login(request: LoginRequest):
    # Buscar usuario por email y contraseña
    user = next((user for user in USERS
                if user["email"] == request.email
                and user["password"] == request.password), None)

    if user:
        # Asegurar que el usuario tiene el campo favorites y recientes
        if "favorites" not in user:
            user["favorites"] = []
        if "recientes" not in user:
            user["recientes"] = []
        return {
            "status": "success",
            "user": {
                "email": user["email"],
                "nombre": user["nombre"],
                "favorites": user["favorites"],
                "recientes": user["recientes"]
            }
        }
    raise HTTPException(status_code=401, detail="Credenciales incorrectas")


# Endpoint para registro de usuario
@app.post("/api/register")
async def register(request: RegisterRequest):
    # Verificar si el email ya está registrado
    if any(user["email"] == request.email for user in USERS):
        raise HTTPException(status_code=400, detail="Email ya registrado")

    new_user = {
        "email": request.email,
        "password": request.password,
        "nombre": request.nombre,
        "favorites": [],  # Inicializa favorites al crear usuario
        "recientes": []  # Inicializa recientes al crear usuario
    }

    # Agregar usuario a la lista de usuarios
    USERS.append(new_user)
    return {"status": "success", "user": new_user}


# Obtención de busquedas recientes del usuario
@app.get("/api/recientes/{email}")
async def get_busquedas(email: str):
    user = next((user for user in USERS if user["email"] == email), None)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    # Devuelve las busquedas recientes del usuario
    return {"recientes": user["recientes"]}


# Agregar busqueda reciente del usuario
@app.post("/api/recientes/{email}")
async def add_busqueda(email: str, busqueda: dict):
    user = next((user for user in USERS if user["email"] == email), None)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    else:
        # Agrega la busqueda a la lista de recientes
        user["recientes"].append(busqueda)
        print(busqueda)
        print(user["recientes"])

    return {"status": "success", "recientes": user["recientes"]}
