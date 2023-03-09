import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Optional
from uuid import uuid4

app = FastAPI()

class Produtores(BaseModel):
    id: Optional[str]
    nome: str
    qnt_fazendas: int
    sexo: str
    cor: str

class Fazenda(BaseModel):
    id: Optional[str]
    nome: str
    tamanho: str

@app.get("/")
def read_root():
    return {"message": "API para  listar produtores e suas fazendas"}

@app.get("/produtores")
def list_produtores():
    produtores = os.listdir("./produtores")
    return {"produtores": produtores}

@app.post("/produtores")
def create_produtor(produtor: Produtores):
    Produtores.id = str(uuid4())
    produtor_path = f"./produtores/{produtor}"
    os.makedirs(produtor_path, exist_ok=True)
    return {"message": f"Produtor {produtor} criado com sucesso"}

@app.get("/produtores/{produtor_id}/fazendas")
def list_fazendas(produtor_id: str):
    produtor_path = f"./produtores/{produtor_id}"
    if not os.path.isdir(produtor_path):
        raise HTTPException(status_code=404, detail="Produtor não encontrado")
    fazendas = os.listdir(produtor_path)
    return {"fazendas": fazendas}

@app.post("/produtores/{produtor_id}/fazendas")
def create_fazenda(produtor_id: str, fazenda: Fazenda):
    produtor_path = f"./produtores/{produtor_id}"
    if not os.path.isdir(produtor_path):
        raise HTTPException(status_code=404, detail="Produtor não encontrado")
    fazenda_path = f"./produtores/{produtor_id}/{fazenda}"
    os.makedirs(fazenda_path, exist_ok=True)
    return {"message": f"Fazenda {fazenda} do produtor {produtor_id} criada com sucesso"}
    
@app.post("/produtores/{produtor_id}/{fazenda_id}/perimetros")
def upload_shapefile(
    produtor_id: str,
    fazenda_id: str,
    shapefile: UploadFile = File(...)
):
    perimetros_path = f"./produtores/{produtor_id}/{fazenda_id}/perimetros"
    os.makedirs(perimetros_path, exist_ok=True)
    with open(f"{perimetros_path}/{shapefile.filename}", "wb") as buffer:
        buffer.write(shapefile.file.read())
    return {"filename": shapefile.filename, "size": len(shapefile.file.read())}

@app.delete("/produtores/{produtor_id/fazendas/{fazenda_id}")
def excluir_fazenda(produtor_id: str, fazenda_id: str):
    fazenda_path = f"./produtores/{produtor_id}/{fazenda_id}"
    if not os.path.exists(fazenda_path):
        return {"erro": f"A fazenda {fazenda_id} não foi encontrada para o produtor {produtor_id}."}
    try:
        os.system(f"rm -rf {fazenda_path}")
        return {"mensagem": f"Fazenda {fazenda_id} excluída com sucesso do produtor {produtor_id}!"}
    except:
        return {"erro": f"Erro ao excluir a fazenda {fazenda_id} do produtor {produtor_id}."}

@app.delete("/produtores/{produtor_id}")
def excluir_produtor(produtor_id: str):
    produtor_path = f"./produtores/{produtor_id}"
    if not os.path.exists(produtor_path):
        return {"erro": f"O produtor nao foi encontrado"}
d