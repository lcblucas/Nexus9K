import requests
import json
import ssl
from urllib.request import urlopen
import urllib3
import csv
import datetime

class Usuario:
    def __init__(self, usuario, senha):
        self.user = usuario
        self.passwd = senha

class Equipamento:
    def __init__(self, comando, url_equipamento, usuario):
        self.comando = comando
        self.url_equipamento = url_equipamento
        self.usr = usuario

    def pegar_hostname(self):
        myheaders = {'content-type': 'application/json-rpc'}
        payload = {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": "show hostname",
                "version": 1
            },
            "id": 1
        }

        retorno_hostname = requests.post(self.url_equipamento, data=json.dumps(payload), headers=myheaders,auth=(self.usr.user, self.usr.passwd), verify=False)
        self.retorno_dicionario_hostname = json.loads(retorno_hostname.text)
        self.hostname = self.retorno_dicionario_hostname["result"]["body"]["hostname"]

    def aplicar_comando(self):
        myheaders = {'content-type': 'application/json-rpc'}
        payload = {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
                "cmd": self.comando,
                "version": 1
            },
            "id": 1
        }

        retorno = requests.post(self.url_equipamento, data=json.dumps(payload), headers=myheaders,auth=(self.usr.user, self.usr.passwd), verify=False)
        self.retorno_dicionario = json.loads(retorno.text)

    def sh_ip_arp_vrf(self):
        horario = datetime.datetime.now()
        nome_do_arquivo = self.hostname + '_' + str(horario)
        arquivo = open(nome_do_arquivo+'.'+'csv', 'w+', newline='')
        writer = csv.writer(
            arquivo,
            delimiter=',',
            #quotechar='|',
            quoting=csv.QUOTE_MINIMAL
        )

        # Percorre o dicionário até o parâmetro que lista os mac address
        saida_lista_final = self.retorno_dicionario["result"]["body"]["TABLE_vrf"]["ROW_vrf"]["TABLE_adj"]["ROW_adj"]

        for i in saida_lista_final:
            print("Hostname: " + self.hostname + " | " + "IP: " + i["ip-addr-out"] + " | " + ("ARP: " + i["mac"]))
            writer.writerow([("Hostname: " + self.hostname + " | " + "IP: " + i["ip-addr-out"] + " | " + ("ARP: " + i["mac"]))])
        arquivo.close()



