from helpers.logger import logger
from models.instituicaoEncino import InstituicaoEnsinoSchema
from repositories.institucaoEnsinoRepository import InstituicaoEnsinoRepository

class InstituicaoEnsinoService:

    def __init__(self):
        self.repository = InstituicaoEnsinoRepository()
        self.schema = InstituicaoEnsinoSchema()

    # TODO: GET
    def get_all(self):
        logger.info("Buscando instituições de ensino")

        return self.repository.getInstituicoes()

    # TODO: GET ID
    def get_by_id(self, id):
        logger.info(f"Buscando instituição de ID {id}")

        return self.repository.getInstituicao(id)

    # TODO: POST
    def postData(self, dados):
        logger.info("Validando dados da instituição")

        data = self.schema.load(dados)

        instituicao = self.repository.postData(data)

        logger.info("Instituição cadastrada com sucesso")

        return instituicao

    # TODO: DELETE
    def deleteInstituicoesEnsino(self, id):
        logger.info(f"Excluindo instituição de ID {id}")

        instituicao = self.repository.deleteInstituicao(id)

        if instituicao is None:
            return None

        logger.info("Instituição excluída com sucesso")

        return instituicao

    # PUT - Atualizar
    def putInstituicoesEnsino(self, id, dados):
        logger.info(f"Atualizando instituição de ID {id}")

        data = self.schema.load(dados)

        instituicao = self.repository.putData(id, data)

        if instituicao is None:
            return None

        logger.info("Instituição atualizada com sucesso")

        return instituicao
