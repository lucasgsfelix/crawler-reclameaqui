#-*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unicodedata
import re
import parser
import requests
import time
import os
####################################################
##
## Crawler Reclame Aqui
## Autor: Lucas G. Felix
## Contribuição: Luiz Angioletti
##
####################################################

def pegaLinks(page, idEmpresa):
    try:
        driver.get(
            "https://www.reclameaqui.com.br/indices/lista_reclamacoes/?id="
            +str(idEmpresa)
            +"&page="
            +str(page)
            +"&size=10&status=ALL"
        )

        html = driver.execute_script(
                "return document.getElementsByTagName('html')[0].innerHTML"
               )
        links, nomeEmpresa = parser.retiraLinks(html)
        links = retiraLinksProibidos(links)

        return links, nomeEmpresa

    except:
        return None, None

# Revisar se está realmente retirando os links proibidos
def retiraLinksProibidos(links):
    '''Retira links que estão listados no arquivo de links proibidos'''
    with open('Aux/links_proibidos') as f:
        links_proibidos = f.read().split('\n')

    if links is not None:
        for count, item in enumerate(links):
            if item in links_proibidos:
                links.pop(count) ## retirando o link proibido
    return links

if __name__ == "__main__":

    #idsEmpresas = ["4421", "1492", "7712", "2852"]
    idsEmpresas = ['4421']
    quantidadeTransacoes = 10000
    flag=0
    driver = webdriver.Chrome()
    for idEmpresa in idsEmpresas:

        qt = 0
        page = 1
        ### fazer flag dos 15 minutos
        while(qt<quantidadeTransacoes):

            links = []
            while len(links) == 0:

                links, nomeEmpresa = pegaLinks(page, idEmpresa)
                if links is None: break

            if links is not None and nomeEmpresa is not None:
                for i in range(0, len(links)):
                    montaLink = "https://www.reclameaqui.com.br/"+nomeEmpresa+links[i]
                    print(montaLink)
                    try:
                        inicio = time.time()
                        driver.get(montaLink)
                        final = time.time()
                        if final - inicio >= 1:
                                driver.refresh() ### para evitar erros onde não carrega a página
                        html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
                        parser.retiraInfo(html, nomeEmpresa)
                        flag=1
                    except:
                        print("Page Erro ! Link: " + montaLink)

                    if flag == 1:
                        qt=qt+1
                        flag=0
            page = page + 1

    with open('saida.txt', 'w') as f:
        html = html.encode('utf-8')
        f.write(html)
