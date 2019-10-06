from html.parser import HTMLParser
from models import Status, Encomenda
import datetime
import re


class HTMLClasses(object):
    DATA_STATUS = 'sroDtEvent'
    DESCRICAO_STATUS = 'sroLbEvent'


class StatusParser(HTMLParser):
    def __init__(self, html):
        HTMLParser.__init__(self)
        self.status_list = []

        self.parsing_status = False
        self.parsing_data_local = False
        self.parsing_hora = False
        self.parsing_local = False
        self.parsing_situacao_descricao = False
        self.parsing_situacao = False

        self.status_situacao = ""
        self.status_descricao = ""
        self.status_local = ""
        self.status_data = ""
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            self.parsing_status = True

        if self.parsing_status and tag == 'td' and self._has_html_class(attrs, HTMLClasses.DATA_STATUS):
            self.parsing_data_local = True

        if self.parsing_status and tag == 'td' and self._has_html_class(attrs, HTMLClasses.DESCRICAO_STATUS):
            self.parsing_situacao_descricao = True

        if self.parsing_status and tag == 'strong':
            self.parsing_situacao = True

        if self.parsing_status and self.parsing_situacao_descricao:
            if not self.parsing_situacao:  # parsing descricao
                self.status_descricao += '<linebreak>'

    def handle_data(self, data):
        if self.parsing_status:
            if self.parsing_data_local:
                if not self.parsing_local:
                    self.status_data += self._formatar_string(data)
                    if not self.parsing_hora:
                        self.parsing_hora = True
                    else:
                        self.parsing_hora = False
                        self.parsing_local = True
                else:
                    self.status_local += self._formatar_string(data)

            if self.parsing_situacao_descricao:
                if self.parsing_situacao:
                    self.status_situacao += self._formatar_string(data)
                else:
                    self.status_descricao += data

    def handle_endtag(self, tag):
        if tag == 'tr':
            status_obj = Status(
                self.status_situacao,
                self._formatar_descricao(self.status_descricao),
                self.status_local,
                self._formatar_datetime(self.status_data)
            )
            self.status_list.append(status_obj)
            self.reset_attributes()
            self.parsing_status = False

        if tag == 'td' and self.parsing_data_local:
            self.parsing_data_local = False

        if tag == 'td' and self.parsing_situacao_descricao:
            self.parsing_situacao_descricao = False

        if tag == 'strong' and self.parsing_situacao:
            self.parsing_situacao = False

    def reset_attributes(self):
        self.parsing_status = False
        self.parsing_data_local = False
        self.parsing_hora = False
        self.parsing_local = False
        self.parsing_situacao_descricao = False
        self.parsing_situacao = False
        self.status_situacao = ""
        self.status_descricao = ""
        self.status_local = ""
        self.status_data = ""

    def _has_html_class(self, attrs, _class):
        for attr in attrs:
            if attr[0] == 'class' and attr[1] == _class:
                return True

    def _limpar_tabeamento(self, string):
        return string.replace('\t', '')

    def _limpar_quebra_de_linha(self, string):
        return string.replace('\r\n', ' ')

    def _formatar_string(self, string):
        string = self._limpar_tabeamento(string)
        string = self._limpar_quebra_de_linha(string)
        string = string.replace('  ', ' ')
        string = string.strip()
        return string

    def _formatar_descricao(self, descricao):
        linhas = descricao.split('<linebreak>')
        resultado = []
        for linha in linhas:
            lin = self._limpar_tabeamento(linha)
            lin = lin.replace('\r\n', ' ')
            lin = lin.replace('  ', ' ')
            lin = lin.strip()
            if lin != '':
                resultado.append(lin)
        return '\r\n'.join(resultado)

    def _formatar_datetime(self, data):
        re_match = '\d{2}/\d{2}/\d{4}'
        dma = re.search(re_match, data)[0]
        dia, mes, ano = dma.split('/')
        hora, minuto = data.replace(dma, '').split(':')
        return datetime.datetime(
            int(ano),
            int(mes),
            int(dia),
            int(hora),
            int(minuto),
            0, 0
        )


