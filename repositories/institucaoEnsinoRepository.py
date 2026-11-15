from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from helpers.database import getConnection
from models.instituicaoEncino import InstituicaoEnsino

class InstituicaoEnsinoRepository:

    def row_to_IE(self, row):
        if row is None:
            return None

        return InstituicaoEnsino(
            id=row[0],
            no_entidade=row[1],
            co_entidade=row[2],
            no_uf=row[3],
            sg_uf=row[4],
            co_uf=row[5],
            no_municipio=row[6],
            co_municipio=row[7],
            nu_ano_censo=row[8],
            qt_mat_bas=row[9],
            qt_mat_inf=row[10],
            qt_mat_fund=row[11],
            qt_mat_med=row[12],
            qt_mat_prof=row[13],
            qt_mat_eja=row[14],
            qt_mat_esp=row[15],
            created=row[16]
        )

    def getInstituicoes(self, page=1, perPage=100):
        connection = getConnection()

        try:
            offset = (page - 1) * perPage

            resultado = connection.execute(
                            text("""
                                SELECT id, no_entidade, co_entidade, no_uf, sg_uf, co_uf, 
                                no_municipio, co_municipio, nu_ano_censo, qt_mat_bas, qt_mat_inf, 
                                qt_mat_fund, qt_mat_med, qt_mat_prof, qt_mat_eja, qt_mat_esp, created
                                FROM tb_instituicao_encino WHERE deleted IS NULL
                                ORDER BY id LIMIT :perPage OFFSET :offset
                            """),
                            {
                                "perPage": perPage,
                                "offset": offset
                            }
                        )

            instituicoesEnsino = [self.row_to_IE(row) for row in resultado.fetchall()]

            return instituicoesEnsino

        except SQLAlchemyError:
            connection.rollback()
            raise
        finally:
            connection.close()

    def getInstituicao(self, id):
        connection = getConnection()

        try:
            resultado  = connection.execute(text("""
                SELECT id, no_entidade, co_entidade, no_uf, sg_uf,
                    co_uf, no_municipio, co_municipio, nu_ano_censo,
                    qt_mat_bas, qt_mat_inf, qt_mat_fund, qt_mat_med,
                    qt_mat_prof, qt_mat_eja, qt_mat_esp, created
                FROM tb_instituicao_encino
                WHERE id = :id AND deleted IS NULL
            """), {"id": id})

            return self.row_to_IE(resultado.fetchone())

        except SQLAlchemyError:
            connection.rollback()
            raise
        finally:
            connection.close()

    def postData(self, data):
        connection = getConnection()

        try:

            resultado =  connection.execute(text("""
                INSERT INTO tb_instituicao_encino (
                    co_entidade, no_entidade, no_uf, sg_uf, co_uf,
                    no_municipio, co_municipio, nu_ano_censo,
                    qt_mat_bas, qt_mat_inf, qt_mat_fund, qt_mat_med,
                    qt_mat_prof, qt_mat_eja, qt_mat_esp
                )
                VALUES (
                        :co_entidade, :no_entidade, :no_uf, :sg_uf,
                        :co_uf, :no_municipio, :co_municipio,
                        :nu_ano_censo, :qt_mat_bas, :qt_mat_inf,
                        :qt_mat_fund, :qt_mat_med, :qt_mat_prof,
                        :qt_mat_eja, :qt_mat_esp
                    )
            """), {
                    'co_entidade': data['co_entidade'],
                    'no_entidade': data['no_entidade'],
                    'no_uf': data['no_uf'],
                    'sg_uf': data['sg_uf'],
                    'co_uf': data['co_uf'],
                    'no_municipio': data['no_municipio'],
                    'co_municipio': data['co_municipio'],
                    'nu_ano_censo': data['nu_ano_censo'],
                    'qt_mat_bas': data['qt_mat_bas'],
                    'qt_mat_inf': data['qt_mat_inf'],
                    'qt_mat_fund': data['qt_mat_fund'],
                    'qt_mat_med': data['qt_mat_med'],
                    'qt_mat_prof': data['qt_mat_prof'],
                    'qt_mat_eja': data['qt_mat_eja'],
                    'qt_mat_esp': data['qt_mat_esp'],
                })

            connection.commit()

            return self.getInstituicao(resultado.lastrowid())

        except SQLAlchemyError:
            connection.rollback()
            raise
        finally:
            connection.close()

    def deleteInstituicao(self, id):
        connection = getConnection()

        try:

            resultado = connection.execute(text("""
                UPDATE tb_instituicao_encino
                SET deleted = CURRENT_TIMESTAMP
                WHERE id = :id AND deleted IS NULL
            """), {"id": id})

            if resultado.rowcount == 0:
                return None

            connection.commit()

            return self.row_to_IE(
                connection.execute(text("""
                    SELECT id, no_entidade, co_entidade, no_uf, sg_uf,
                        co_uf, no_municipio, co_municipio, nu_ano_censo,
                        qt_mat_bas, qt_mat_inf, qt_mat_fund, qt_mat_med,
                        qt_mat_prof, qt_mat_eja, qt_mat_esp, created
                    FROM tb_instituicao_encino
                    WHERE id = :id
                """), {"id": id}).fetchone()
            )

        except SQLAlchemyError:
            connection.rollback()
            raise
        finally:
            connection.close()

    def putData(self, id, data):
        connection = getConnection()

        try:

            resultado = connection.execute(text("""
                UPDATE tb_instituicao_encino
                    SET co_entidade = :co_entidade,
                        no_entidade = :no_entidade,
                        no_uf = :no_uf,
                        sg_uf = :sg_uf,
                        co_uf = :co_uf,
                        no_municipio = :no_municipio,
                        co_municipio = :co_municipio,
                        nu_ano_censo = :nu_ano_censo,
                        qt_mat_bas = :qt_mat_bas,
                        qt_mat_inf = :qt_mat_inf,
                        qt_mat_fund = :qt_mat_fund,
                        qt_mat_med = :qt_mat_med,
                        qt_mat_prof = :qt_mat_prof,
                        qt_mat_eja = :qt_mat_eja,
                        qt_mat_esp = :qt_mat_esp
                    WHERE id = :id AND deleted IS NULL
            """), {
                    'id': id,
                    'co_entidade': data['co_entidade'],
                    'no_entidade': data['no_entidade'],
                    'no_uf': data['no_uf'],
                    'sg_uf': data['sg_uf'],
                    'co_uf': data['co_uf'],
                    'no_municipio': data['no_municipio'],
                    'co_municipio': data['co_municipio'],
                    'nu_ano_censo': data['nu_ano_censo'],
                    'qt_mat_bas': data['qt_mat_bas'],
                    'qt_mat_inf': data['qt_mat_inf'],
                    'qt_mat_fund': data['qt_mat_fund'],
                    'qt_mat_med': data['qt_mat_med'],
                    'qt_mat_prof': data['qt_mat_prof'],
                    'qt_mat_eja': data['qt_mat_eja'],
                    'qt_mat_esp': data['qt_mat_esp'],
                })

            if resultado.rowcount == 0:
                return None

            connection.commit()

            connection.execute(text("""
                SELECT id, no_entidade, co_entidade, no_uf, sg_uf,
                    co_uf, no_municipio, co_municipio, nu_ano_censo,
                    qt_mat_bas, qt_mat_inf, qt_mat_fund, qt_mat_med,
                    qt_mat_prof, qt_mat_eja, qt_mat_esp, created
                FROM tb_instituicao_encino
                WHERE id = :id
            """), (id,))

            return self.row_to_IE(resultado.fetchone())

        except SQLAlchemyError:
            connection.rollback()
            raise
        finally:
            connection.close()
