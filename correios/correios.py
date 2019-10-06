from urllib.parse import urlencode
import requests
from models import Status, Encomenda
from parsers import StatusParser


class Correios(object):
    url = 'https://www2.correios.com.br/sistemas/rastreamento/ctrl/ctrlRastreamento.cfm?'

    def _get_headers(self):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        return headers

    def _get_request_data(self, identificador):
        data = {
            'objetos': identificador
        }
        encoded_data = urlencode(data).encode()
        return encoded_data

    def buscar_encomenda(self, identificador):
        headers = self._get_headers()
        data =  self._get_request_data(identificador)

        response = requests.post(self.url, data=data, headers=headers)
        response.encoding = 'iso-8859-1'
        html = response.text
        response.close()

        parser = StatusParser(html)
        status_encomenda = parser.status_list
        parser.close()

        encomenda = Encomenda(identificador, status_encomenda)
        return encomenda


a = Correios().buscar_encomenda('OG007852303BR')
print('Identificador: ' + a.identificador)
for status in a.status:
    print('Data: ' + status.data.__str__())
    print('Local: ' + status.local)
    print('Situação: ' + status.situacao)
    print('Descrição: ' + status.descricao)
    print('------------------------------')
