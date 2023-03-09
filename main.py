from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4

app = FastAPI()



class Produtores(BaseModel):
    id: Optional[str]
    nome: str
    qnt_fazendas: int
    sexo: str
    cor: str



#HOME
@app.get("/")
def read_root():
    return {"TESTE"}

#OBTENDO UM PRODUTOR PELO ID
@app.get("/produtores/{produtor_id}")
def obter_produtor(produtor_id: str):
    for produtor in banco:
        if(produtor.id == produtor_id):
            return produtor
    return {"erro: Produtor não localizado"}

#RETIRANDO UM PRODUTOR PELO ID
@app.delete("/produtores/{produtor_id}")
def remover_produtor(produtor_id:  str):
    posicao = -1
    for index, produtor in enumerate(banco):
        if produtor.id == produtor_id:
            posicao = index
            break
    
    if posicao != -1:
        banco.pop(posicao)
        return {"Produtor removido com sucesso"}
    else:
        return {"Produtor não removido"}

#LISTANDO OS PRODUTORES
@app.get("/produtores")
def listar_fazendeiros():
    return banco

#CRIANDO NOVOS PRODUTORES
@app.post("/produtores")
def criar_produtor(produtor: Produtores):
    Produtores.id = str(uuid4())
    banco.append(produtor)
    return None

#CRIANDO NOVAS FAZENDAS
@app.post("/produtores/{produtor_id}/fazendas")
def criar_fazendas(produtor_id: str, fazenda: Fazenda):
    for produtor in banco:
        if(produtor.id == produtor_id):
            Fazenda.id = str(uuid4())
            bancoFazenda.append(fazenda)
            return None
    return {"erro: Produtor não localizado"}

#Mostrando Fazendas
@app.get("/produtores/{produtor_id}/fazendas")
def mostrar_fazendas(produtor_id: str):
    for produtor in banco:
        if(produtor.id == produtor_id):
            if(len(bancoFazenda) != 0):
                return bancoFazenda
            return {"Esse produtor nao tem fazendas"}