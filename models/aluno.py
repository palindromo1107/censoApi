from pessoa import Pessoa

class Aluno(Pessoa):

    def __init__(self, nome, cpf, matricula):
        super().__init__(nome, cpf)
        self.matricula = matricula