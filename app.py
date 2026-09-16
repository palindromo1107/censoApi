from flask import Flask, request
import helpers.files.fileEndpoint as helper
from models.instituicaoEncino import InstituicaoEncino
from helpers.database import getConn

# TODO: GET BY ID PRONTO E ATUALIZAR
# TODO: dbeaver

def listar():
    # ler arquivo
    data = helper.read("instituicoesEncino.json")

    # converter json -> ie
    instituicoesEncino = [InstituicaoEncino(
            row["id"],
            row["co_entidade"],
            row["no_entidade"],
            row["qt_mat_bas"]
        ).toDict() for row in data]

    # retornar lista
    return instituicoesEncino

def salvar(data):
    helper.update("instituicoesEncino.json", data)

def buscarId(id):
    dataset = helper.read("instituicoesEncino.json")
    instituicaoEscolhida = [ InstituicaoEncino(row["id"],row["co_entidade"],row["no_entidade"],row["qt_mat_bas"]) for row in dataset if str(row["id"]) == str(id)]
    
    return instituicaoEscolhida

IEs = "/instituicoesEnsino"
app = Flask(__name__)

@app.route("/")
def index():
    return {"version": "1.0.0"}, 200

@app.route("/health")
def health():
    return {"status": "OK"}, 200

# ROTAS E METODOS

# GET / GET CO ENTIDADE
@app.get(IEs)
def getAllInstituicoes():
    insituicoesEnsino = listar()
    co_entidade = request.args.get("co_entidade")
    if co_entidade is not None:
        insituicoesEnsinoReponse = [ ie.toDict() for ie in insituicoesEnsino if ie.co_entidade == co_entidade ]
    else:
        insituicoesEnsinoReponse = [ ie.toDict() for ie in insituicoesEnsino ]

    return insituicoesEnsinoReponse, 200

# GET ID
@app.get(f"{IEs}/<int:id>")
def getByIdInstituicoesEnsino(id):
    traget = buscarId(id)

    if id is not None:
        instituicaoResponde = [ data.toDict() for data in traget if str(data.id) == str(id) ]   
        return instituicaoResponde,200

# POST
@app.post(f"{IEs}/post")
def postData():
    data = request.get_json()
    instituicoesEncino = listar()
    instituicoesEncino.append({"id": data.get("id"), "nome": data.get("nome")})
    salvar(instituicoesEncino)
    return instituicoesEncino, 201

# DELETE
@app.delete(f"{IEs}/delet")
def deleteInstituicoesEncino():
    id = request.json.get("id")
    instituicoesEncino = listar()
    data = buscarId(id, instituicoesEncino, False)
    salvar(data)
    return data, 200

# PUT
@app.put(f"{IEs}/put")
def putInstituicoesEncino():
    instituicoesEncino = listar()
    id = request.json.get("id")
    nome = request.json.get("nome")
    data = buscarId(id, instituicoesEncino, False)
    data.append({"id": id, "nome": nome})
    salvar(data)
    return data, 201

def main(arg=[]):
    app.run(debug=True)

if __name__ == "__main__":
    main()


"""
instituicoesEncino = listar()
    coEntidade = request.args.get("co_entidade")
    if not coEntidade:
        return instituicoesEncino, 200
    else:
        newInstituicoesEncino = [ie for ie in instituicoesEncino if ie["co_entidade"] == int(coEntidade)]
        return newInstituicoesEncino
"""
