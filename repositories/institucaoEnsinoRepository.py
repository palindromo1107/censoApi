import psycopg2

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

    def getInstituicoes(self, page, perPage=100):
        connection = getConnection()

        try:
            offset = (page - 1) * perPage
            
            cursor = connection.cursor()

            cursor.execute("""
                                SELECT id, no_entidade, co_entidade, no_uf, sg_uf, co_uf, 
                                no_municipio, co_municipio, nu_ano_censo, qt_mat_bas, qt_mat_inf, 
                                qt_mat_fund, qt_mat_med, qt_mat_prof, qt_mat_eja, qt_mat_esp, created
                                FROM tb_instituicao_encino WHERE deleted IS NULL
                                ORDER BY id LIMIT %s OFFSET %s
                            """,
                            (perPage, offset)
                        )

            instituicoesEnsino = [self.row_to_IE(row) for row in cursor.fetchall()]

            return instituicoesEnsino

        except psycopg2.Error:
            connection.rollback()
            raise
        finally:
            connection.close()

    def getInstituicao(self, id):
        connection = getConnection()

        try:
            cursor = connection.cursor()
            
            cursor.execute("""
                SELECT id, no_entidade, co_entidade, no_uf, sg_uf,
                    co_uf, no_municipio, co_municipio, nu_ano_censo,
                    qt_mat_bas, qt_mat_inf, qt_mat_fund, qt_mat_med,
                    qt_mat_prof, qt_mat_eja, qt_mat_esp, created
                FROM tb_instituicao_encino
                WHERE id = %s AND deleted IS NULL
            """, (id,))

            return self.row_to_IE(cursor.fetchone())

        except psycopg2.Error:
            connection.rollback()
            raise
        finally:
            connection.close()

    def postData(self, data):
        connection = getConnection()

        try:
            
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO tb_instituicao_encino (
                    co_entidade, no_entidade, no_uf, sg_uf, co_uf,
                    no_municipio, co_municipio, nu_ano_censo,
                    qt_mat_bas, qt_mat_inf, qt_mat_fund, qt_mat_med,
                    qt_mat_prof, qt_mat_eja, qt_mat_esp
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
                (
                    data['co_entidade'],
                    data['no_entidade'],
                    data['no_uf'],
                    data['sg_uf'],
                    data['co_uf'],
                    data['no_municipio'],
                    data['co_municipio'],
                    data['nu_ano_censo'],
                    data['qt_mat_bas'],
                    data['qt_mat_inf'],
                    data['qt_mat_fund'],
                    data['qt_mat_med'],
                    data['qt_mat_prof'],
                    data['qt_mat_eja'],
                    data['qt_mat_esp']
                ))

            connection.commit()

            return self.getInstituicao(cursor.lastrowid())

        except psycopg2.Error:
            connection.rollback()
            raise
        finally:
            connection.close()

    def deleteInstituicao(self, id):
        connection = getConnection()

        try:
            
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE tb_instituicao_encino
                SET deleted = CURRENT_TIMESTAMP
                WHERE id = %s AND deleted IS NULL
            """, (id,))

            if cursor.rowcount == 0:
                return None

            connection.commit()
            
            cursor.execute("""
                            SELECT id, no_entidade, co_entidade, no_uf, sg_uf, 
                            co_uf, no_municipio, co_municipio, nu_ano_censo, 
                            qt_mat_bas, qt_mat_inf, qt_mat_fund, qt_mat_med, 
                            qt_mat_prof, qt_mat_eja, qt_mat_esp, created
                            FROM tb_instituicao_encino WHERE id = %s
                        """, (id,))

            return self.row_to_IE(
                cursor.fetchone()
            )

        except psycopg2.Error:
            connection.rollback()
            raise
        finally:
            connection.close()

    def putData(self, id, data):
        connection = getConnection()

        try:
            
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE tb_instituicao_encino
                SET co_entidade = %s, no_entidade = %s, no_uf = %s,
                    sg_uf = %s, co_uf = %s, no_municipio = %s,
                    co_municipio = %s, nu_ano_censo = %s,
                    qt_mat_bas = %s, qt_mat_inf = %s, qt_mat_fund = %s,
                    qt_mat_med = %s, qt_mat_prof = %s, qt_mat_eja = %s,
                    qt_mat_esp = %s
                WHERE id = %s AND deleted IS NULL
            """,(
                data['co_entidade'],
                data['no_entidade'],
                data['no_uf'],
                data['sg_uf'],
                data['co_uf'],
                data['no_municipio'],
                data['co_municipio'],
                data['nu_ano_censo'],
                data['qt_mat_bas'],
                data['qt_mat_inf'],
                data['qt_mat_fund'],
                data['qt_mat_med'],
                data['qt_mat_prof'],
                data['qt_mat_eja'],
                data['qt_mat_esp'],
                id
            ))

            if cursor.rowcount == 0:
                return None

            connection.commit()

            cursor.execute("""
                SELECT id, no_entidade, co_entidade, no_uf, sg_uf,
                    co_uf, no_municipio, co_municipio, nu_ano_censo,
                    qt_mat_bas, qt_mat_inf, qt_mat_fund, qt_mat_med,
                    qt_mat_prof, qt_mat_eja, qt_mat_esp, created
                FROM tb_instituicao_encino
                WHERE id = %s
            """, (id,))

            return self.row_to_IE(cursor.fetchone())

        except psycopg2.Error:
            connection.rollback()
            raise
        finally:
            connection.close()
