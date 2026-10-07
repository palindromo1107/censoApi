from flask import request, jsonify
from marshmallow import ValidationError
from sqlite3 import OperationalError

from models.instituicaoEncino import InstituicaoEnsino, InstituicaoEnsinoSchema
from helpers.database import getConn
from helpers.aplication import app

def row_to_IE(row):
    return InstituicaoEnsino(
        row[0],
        row[1],
        row[2],
        row[3],
        row[4],
        row[5],
        row[6],
        row[7],
        row[8],
        row[9],
        row[10],
        row[11],
        row[12],
        row[13],
        row[14],
        row[15]
        )

URL_BASE = "/instituicoesEnsino"

@app.route("/")
def index():
    return {"version": "1.0.0"}, 200

@app.route("/health")
def health():
    return {"status": "OK"}, 200

# TODO: ROTAS E METODOS

# TODO: GET / GET CO ENTIDADE
@app.get(URL_BASE)
def getAllInstituicoes():
    try:
        # FAZER CONEXÃO
        conn = getConn()
        
        # ADQUIRIR CURSOR
        cursor = conn.cursor()
        
        # DEFINIR CONSULTA
        cursor.execute('select * from tb_instituicao_encino where deleted is not null')
        
        # CONVERTER TABELA
        data = cursor.fetchall()
        
        # CONVERTER DADOS E CRIAR LISTA
        instituicoesEnsino = [row_to_IE(row) for row in data]
        
        co_entidade = request.args.get("co_entidade")
        if co_entidade is not None:
            instituicoesEnsinoReponse = [ ie.toDict() for ie in instituicoesEnsino if ie.co_entidade == co_entidade ]
        else:
            instituicoesEnsinoReponse = [ ie.toDict() for ie in instituicoesEnsino ]
        
        return instituicoesEnsinoReponse, 200
    except OperationalError:
        conn.rollback()
        raise

# TODO: GET ID
@app.get(f"{URL_BASE}/<int:id>")
def getByIdInstituicoesEnsino(id):
    try:
        instituicao = None
        conn = getConn()
        
        cursor = conn.cursor()
        
        cursor.execute('select * from tb_instituicao_encino where id = ?', (id,))
        
        data = cursor.fetchone()
        
        if data is not None:
            instituicao = [row_to_IE(row) for row in data]
            return instituicao.toDict(), 200
        else:
            return 'not found', 404
    except OperationalError:
        conn.rollback()
        raise

# TODO: POST
@app.post(f"{URL_BASE}/post")
def postData():
    try:
        # TODO: ENTRADA DOS DADOS E VALIDAÇÃO
        schema = InstituicaoEnsinoSchema()
        
        data = schema.load(request.get_json())
        
        # TODO: CONEXÃO
        conn = getConn()
        
        # TODO: CURSOR
        cursor = conn.cursor()
        
        # TODO: PREPARAR DML
        cursor.execute(
            '''
            INSERT INTO tb_instituicao_encino 
            ( id, co_entidade, no_entidade, no_uf, sg_uf, co_uf, no_municipio, co_municipio, nu_ano_censo, qt_mat_bas, qt_mat_inf, 
            qt_mat_fund, qt_mat_med, qt_mat_prof, qt_mat_eja, qt_mat_esp )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            returning id, created
            ''',
            ( data['id'], data['co_entidade'], data['no_entidade'], data['no_uf'], data['sg_uf'], data['co_uf'], data['no_municipio'], 
            data['co_municipio'], data['nu_ano_censo'], data['qt_mat_bas'], data['qt_mat_inf'], data['qt_mat_fund'], data['qt_mat_med'],
            data['qt_mat_prof'], data['qt_mat_eja'], data['qt_mat_esp'] )
        )

        resultSet = cursor.fetchone()
        id = resultSet[0]
        created = resultSet[1]

        conn.commit()
        
        instituicao = InstituicaoEnsino(**data, id=id, created=created)
        
        conn.close()
        
        return jsonify(InstituicaoEnsinoSchema.dump(instituicao)), 201
    except ValidationError as err:
        return {'erro': 'invalid data', 'campos': err.messages}, 400

# TODO: DELETE
@app.delete(f"{URL_BASE}/delet")
def deleteInstituicoesEnsino():
    id = request.json.get("id")
    
    conn = getConn()

    cursor = conn.cursor()
    
    cursor.execute('delete from tb_instituicao_encino where id = ?', (id,))
    
    data = cursor.fetchall()
    
    instituicoesEnsino = [row_to_IE(row) for row in data]
    
    data = [ie.toDict() for ie in instituicoesEnsino]

    return data, 200

# TODO: PUT
@app.put(f"{URL_BASE}/put")
def putInstituicoesEnsino():
    schema = InstituicaoEnsinoSchema()
    
    data = schema.load(request.get_json())
    
    conn = getConn()
    
    cursor = conn.cursor()
    
    cursor.execute("""
        update tb_instituicao_encino set co_entidade = ?, no_entidade = ?, no_uf = ?, sg_uf = ?, co_uf = ?, no_municipio = ?, 
        co_municipio = ?, nu_ano_censo = ?, qt_mat_bas = ?, qt_mat_inf = ?, qt_mat_fund = ?, qt_mat_med = ?, qt_mat_prof = ?, 
        qt_mat_eja = ?, qt_mat_esp = ? where id = ?
        """, 
        ( 
            data['id'], data['co_entidade'], data['no_entidade'], data['no_uf'], data['sg_uf'], data['co_uf'], data['no_municipio'], 
            data['co_municipio'], data['nu_ano_censo'], data['qt_mat_bas'], data['qt_mat_inf'], data['qt_mat_fund'], data['qt_mat_med'],
            data['qt_mat_prof'], data['qt_mat_eja'], data['qt_mat_esp'] 
        ))

    conn.commit()
    
    conn.close()

    return 'data', 201

def main(arg=[]):
    app.run(debug=True)

if __name__ == "__main__":
    main()