class InstituicaoEncino:
    def __init__ (self, id, co_entidade, no_entidade, qt_mat_bas):

        self.id = id
        self.co_entidade = co_entidade
        self.no_entidade = no_entidade
        self.qt_mat_bas = qt_mat_bas

    def __str__(self):
        return (
            f"<InstituicaoEnsino: "
            f"{self.id}, "
            f"{self.co_entidade}, "
            f"{self.no_entidade}, "
            f"{self.qt_mat_bas}>"
        )

    def toDict(self):
        return {
            "id": self.id,
            "co_entidade": self.co_entidade,
            "no_entidade": self.no_entidade,
            "qt_mat_bas": self.qt_mat_bas,
        }