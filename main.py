from fastapi import FastAPI, HTTPException, Request
from bson import ObjectId
from database import usuarios_collection
from models import UserIn, UserOut
from pydantic import BaseModel, EmailStr
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ou especifique seu domínio do frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginIn(BaseModel):
    email: EmailStr

@app.post("/login")
async def login_usuario(login: LoginIn):
    user = usuarios_collection.find_one({"email": login.email})
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")
    # Para teste, não há senha. Apenas retorna o usuário.
    user["_id"] = str(user["_id"])
    return user

@app.post("/usuarios", response_model=UserOut)
async def criar_usuario(usuario: UserIn):
    novo = {
        "name": usuario.nome,
        "email": usuario.email,
        "age": usuario.idade
    }
    resultado = usuarios_collection.insert_one(novo)
    novo["_id"] = str(resultado.inserted_id)
    return novo

@app.get("/usuarios", response_model=list[UserOut])
async def listar_usuarios(name: str = None, email: str = None, age: int = None):
    filtro = {}
    if name: filtro["name"] = name
    if email: filtro["email"] = email
    if age: filtro["age"] = age
    users = [{**user, "_id": str(user["_id"])} for user in usuarios_collection.find(filtro)]        
    return users

@app.put("/usuarios/{id}", response_model=UserOut)
async def atualizar_usuario(id: str, usuario: UserIn):
    dados = {
        "name": usuario.nome,
        "email": usuario.email,
        "age": usuario.idade
    }
    result = usuarios_collection.update_one({"_id": ObjectId(id)}, {"$set": dados})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"_id": id, **dados}

@app.delete("/usuarios/{id}")
async def deletar_usuario(id: str):
    result = usuarios_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"message": "Usuário deletado com sucesso!"}
