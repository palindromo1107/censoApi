from helpers.database import getConn
from helpers.logger import logger
from models.instituicaoEncino import InstituicaoEnsino

from flask import request
from sqlite3 import OperationalError

class InstituicaoEnsinoService:
    def __init__(self):
        pass
    
    def row_to_IE(self, row):
        return InstituicaoEnsino( row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16] )

    def getAll(self):
        logger.info('INFO: Tentando conexão com o banco de dados')
        try:
            logger.info('INFO: Buscando instituições de ensino')
            # FAZER CONEXÃO
            conn = getConn()

            # ADQUIRIR CURSOR
            cursor = conn.cursor()

            # DEFINIR CONSULTA
            cursor.execute('select * from tb_instituicao_encino')

            # CONVERTER TABELA
            data = cursor.fetchall()

            # CONVERTER DADOS E CRIAR LISTA
            instituicoesEnsino = [self.row_to_IE(row) for row in data]

            co_entidade = request.args.get("co_entidade")
            if co_entidade is not None:
                instituicoesEnsinoReponse = [ ie.toDict() for ie in instituicoesEnsino if ie.co_entidade == co_entidade ]
            else:
                instituicoesEnsinoReponse = [ ie.toDict() for ie in instituicoesEnsino ]
            logger.info('INFO: Finalizando busca')
            return instituicoesEnsinoReponse, 200
        except OperationalError:
            logger.error('ERROR: Erro de listagem')
            conn.rollback()
            raise