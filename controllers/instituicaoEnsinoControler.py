from flask import request, jsonify, Blueprint
from sqlite3 import OperationalError
from marshmallow import ValidationError

from helpers.logger import logger
from models.instituicaoEncino import InstituicaoEnsinoSchema
from services.instituicaoEnsinoService import InstituicaoEnsinoService


instituicaoEnsinoSchema = InstituicaoEnsinoSchema()
instituicoesEnsinoSchema = InstituicaoEnsinoSchema(many=True)

instituicaoEnsino_bp = Blueprint(
    'instituicaoEnsino',
    __name__,
    url_prefix='/instituicoesEnsino'
)

# TODO: GET
@instituicaoEnsino_bp.get('/')
def get_all_instituicoes():
    try:
        service = InstituicaoEnsinoService()
        instituicoes = service.get_all()

        return jsonify(
            instituicoesEnsinoSchema.dump(instituicoes)
        ), 200

    except OperationalError:
        logger.exception("Erro ao listar instituições")

        return jsonify({
            "mensagem": "Problema ao conectar com o banco de dados"
        }), 500

# TODO: GET ID
@instituicaoEnsino_bp.get('/<int:id>')
def getById(id):
    try:
        service = InstituicaoEnsinoService()
        instituicao = service.get_by_id(id)

        if instituicao is None:
            return jsonify({
                "mensagem": "Instituição não encontrada"
            }), 404

        return jsonify(
            instituicaoEnsinoSchema.dump(instituicao)
        ), 200

    except OperationalError:
        logger.exception("Erro ao buscar instituição")

        return jsonify({
            "mensagem": "Problema ao conectar com o banco de dados"
        }), 500

# TODO: POST
@instituicaoEnsino_bp.post('/')
def postData():
    try:
        dados = request.get_json()

        if dados is None:
            return jsonify({
                "mensagem": "Dados não enviados"
            }), 400

        service = InstituicaoEnsinoService()
        instituicao = service.postData(dados)

        return jsonify(
            instituicaoEnsinoSchema.dump(instituicao)
        ), 201

    except ValidationError as erro:
        return jsonify({
            "mensagem": "Dados inválidos",
            "campos": erro.messages
        }), 400

    except OperationalError:
        logger.exception("Erro ao cadastrar instituição")

        return jsonify({
            "mensagem": "Problema ao conectar com o banco de dados"
        }), 500

# TODO: DELETE
@instituicaoEnsino_bp.delete('/<int:id>')
def deleteInstituicoesEnsino(id):
    try:
        service = InstituicaoEnsinoService()
        instituicao = service.deleteInstituicoesEnsino(id)

        if instituicao is None:
            return jsonify({
                "mensagem": "Instituição não encontrada"
            }), 404

        return jsonify({
            "mensagem": "Instituição excluída com sucesso",
            "instituicao": instituicaoEnsinoSchema.dump(instituicao)
        }), 200

    except OperationalError:
        logger.exception("Erro ao excluir instituição")

        return jsonify({
            "mensagem": "Problema ao conectar com o banco de dados"
        }), 500

# TODO: PUT
@instituicaoEnsino_bp.put('/<int:id>')
def putInstituicoesEnsino(id):
    try:
        dados = request.get_json()

        if dados is None:
            return jsonify({
                "mensagem": "Dados não enviados"
            }), 400

        service = InstituicaoEnsinoService()
        instituicao = service.putInstituicoesEnsino(id, dados)

        if instituicao is None:
            return jsonify({
                "mensagem": "Instituição não encontrada"
            }), 404

        return jsonify(
            instituicaoEnsinoSchema.dump(instituicao)
        ), 200

    except ValidationError as erro:
        return jsonify({
            "mensagem": "Dados inválidos",
            "campos": erro.messages
        }), 400

    except OperationalError:
        logger.exception("Erro ao atualizar instituição")

        return jsonify({
            "mensagem": "Problema ao conectar com o banco de dados"
        }), 500
