

class Status(object):

    def __init__(self, situacao, descricao, local, data):
        self.situacao = situacao
        self.descricao = descricao
        self.local = local
        self.data = data

    def __str__(self):
        return self.situacao


class Encomenda(object):

    def __init__(self, identificador, status):
        self.identificador = identificador
        self.status = status

    def __str__(self):
        return self.identificador

