from flask import Flask, request
import helpers.files.fileEndpoint as helper
from models.instituicaoEncino import InstituicaoEnsino
from helpers.database import getConn

def listar():
    # ler arquivo
    data = helper.read("instituicoesEnsino.json")

    # converter json -> ie
    instituicoesEnsino = [InstituicaoEncino(
            row["id"],
            row["co_entidade"],
            row["no_entidade"],
            row["qt_mat_bas"]
        ).toDict() for row in data]

    # retornar lista
    return instituicoesEnsino

def salvar(data):
    helper.update("instituicoesEnsino.json", data)

def buscarId(id):
    dataset = helper.read("instituicoesEnsino.json")
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

# TODO: ROTAS E METODOS

# TODO: GET / GET CO ENTIDADE
@app.get(IEs)
def getAllInstituicoes():
    # FAZER CONEXÃO
    conn = getConn()

    # ADQUIRIR CURSOR
    cursor = conn.cursor()

    # DEFINIR CONSULTA
    cursor.execute('select * from tb_instituicao_encino')

    # CONVERTER TABELA
    data = cursor.fetchall()

    # CONVERTER DADOS E CRIAR LISTA
    instituicoesEnsino = [InstituicaoEnsino(row[0], row[1], row[2], row[9]) for row in data]

    co_entidade = request.args.get("co_entidade")
    if co_entidade is not None:
        instituicoesEnsinoReponse = [ ie.toDict() for ie in instituicoesEnsino if ie.co_entidade == co_entidade ]
    else:
        instituicoesEnsinoReponse = [ ie.toDict() for ie in instituicoesEnsino ]

    return instituicoesEnsinoReponse, 200

# TODO: GET ID
@app.get(f"{IEs}/<int:id>")
def getByIdInstituicoesEnsino(id):
    instituicao = None
    conn = getConn()
    
    cursor = conn.cursor()
    
    cursor.execute('select * from tb_instituicao_encino where id = ?', (id,))
    
    data = cursor.fetchone()
    
    if data is not None:
        instituicao = InstituicaoEnsino(data[0], data[1], data[2], data[9])
        return instituicao.toDict(), 200
    else:
        return 'not found', 404

# TODO: POST
@app.post(f"{IEs}/post")
def postData():
    # TODO: ENTRADA DOS DADOS E VALIDAÇÃO
    data = request.get_json()
    
    coInep = data.get('co_inep')
    
    conn = getConn()
    
    cursor = conn.cursor()
    
    cursor.execute(
        '''
        INSERT INTO tb_instituicao_encino (
            id,
            co_entidade,
            no_entidade,
            no_uf,
            sg_uf,
            co_uf,
            no_municipio,
            co_municipio,
            nu_ano_censo,
            qt_mat_bas,
            qt_mat_inf,
            qt_mat_fund,
            qt_mat_med,
            qt_mat_prof,
            qt_mat_eja,
            qt_mat_esp
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''',
        (
            data["id"],
            data["co_entidade"],
            data["no_entidade"],
            data["no_uf"],
            data["sg_uf"],
            data["co_uf"],
            data["no_municipio"],
            data["co_municipio"],
            data["nu_ano_censo"],
            data["qt_mat_bas"],
            data["qt_mat_inf"],
            data["qt_mat_fund"],
            data["qt_mat_med"],
            data["qt_mat_prof"],
            data["qt_mat_eja"],
            data["qt_mat_esp"]
        )
    )

    conn.commit()
    
    conn.close()
    
    return {'id': id, 'co_inep': coInep}, 201

# TODO: DELETE
@app.delete(f"{IEs}/delet")
def deleteInstituicoesEnsino():
    id = request.json.get("id")
    
    conn = getConn()

    cursor = conn.cursor()
    
    cursor.execute('delete from tb_instituicao_encino where id = ?', (id,))
    
    data = cursor.fetchall()
    
    instituicoesEnsino = [InstituicaoEnsino(row[0], row[1], row[2], row[9]) for row in data]
    
    data = [ie.toDict() for ie in instituicoesEnsino]

    return data, 200

# TODO: PUT
@app.put(f"{IEs}/put")
def putInstituicoesEnsino():
    instituicoesEnsino = listar()
    id = request.json.get("id")
    nome = request.json.get("nome")
    data = buscarId(id, instituicoesEnsino, False)
    data.append({"id": id, "nome": nome})
    salvar(data)
    return data, 201

def main(arg=[]):
    app.run(debug=True)

if __name__ == "__main__":
    main()