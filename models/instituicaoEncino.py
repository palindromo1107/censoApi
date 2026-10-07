from marshmallow import Schema
class InstituicaoEnsino:
    def __init__(
        self, id, co_entidade, no_entidade, no_uf, sg_uf,
        co_uf, no_municipio, co_municipio, nu_ano_censo,
        qt_mat_bas, qt_mat_inf, qt_mat_fund, qt_mat_med,
        qt_mat_prof, qt_mat_eja, qt_mat_esp, created
    ):
        self.id = id
        self.co_entidade = co_entidade
        self.no_entidade = no_entidade
        self.no_uf = no_uf
        self.sg_uf = sg_uf
        self.co_uf = co_uf
        self.no_municipio = no_municipio
        self.co_municipio = co_municipio
        self.nu_ano_censo = nu_ano_censo
        self.qt_mat_bas = qt_mat_bas
        self.qt_mat_inf = qt_mat_inf
        self.qt_mat_fund = qt_mat_fund
        self.qt_mat_med = qt_mat_med
        self.qt_mat_prof = qt_mat_prof
        self.qt_mat_eja = qt_mat_eja
        self.qt_mat_esp = qt_mat_esp
        self.created = created

    def __str__(self):
        return (
            f"<InstituicaoEnsino: "
            f"{self.id}, "
            f"{self.co_entidade}, "
            f"{self.no_entidade}, "
            f"{self.no_uf}, "
            f"{self.sg_uf}, "
            f"{self.co_uf}, "
            f"{self.no_municipio}, "
            f"{self.co_municipio}, "
            f"{self.nu_ano_censo}, "
            f"{self.qt_mat_bas}, "
            f"{self.qt_mat_inf}, "
            f"{self.qt_mat_fund}, "
            f"{self.qt_mat_med}, "
            f"{self.qt_mat_prof}, "
            f"{self.qt_mat_eja}, "
            f"{self.qt_mat_esp}>"
        )

    def toDict(self):
        return {
            "id": self.id,
            "co_entidade": self.co_entidade,
            "no_entidade": self.no_entidade,
            "no_uf": self.no_uf,
            "sg_uf": self.sg_uf,
            "co_uf": self.co_uf,
            "no_municipio": self.no_municipio,
            "co_municipio": self.co_municipio,
            "nu_ano_censo": self.nu_ano_censo,
            "qt_mat_bas": self.qt_mat_bas,
            "qt_mat_inf": self.qt_mat_inf,
            "qt_mat_fund": self.qt_mat_fund,
            "qt_mat_med": self.qt_mat_med,
            "qt_mat_prof": self.qt_mat_prof,
            "qt_mat_eja": self.qt_mat_eja,
            "qt_mat_esp": self.qt_mat_esp,
        }
from marshmallow import Schema, fields

class InstituicaoEnsinoSchema(Schema):
    id = fields.Int(dump_only=True)
    co_entidade = fields.Int(required=True)
    no_entidade = fields.String(required=True)
    no_uf = fields.String(required=True)
    sg_uf = fields.String(required=True)
    co_uf = fields.Int(required=True)
    no_municipio = fields.String(required=True)
    co_municipio = fields.Int(required=True)
    nu_ano_censo = fields.Int(required=True)
    qt_mat_bas = fields.Int(required=True)
    qt_mat_inf = fields.Int(required=True)
    qt_mat_fund = fields.Int(required=True)
    qt_mat_med = fields.Int(required=True)
    qt_mat_prof = fields.Int(required=True)
    qt_mat_eja = fields.Int(required=True)
    qt_mat_esp = fields.Int(required=True)