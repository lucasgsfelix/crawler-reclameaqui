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

    # idsEmpresas = ["4421", "1492", "7712", "2852"]
    Empresas = ['4421']

    # link = "https://www.reclameaqui.com.br/indices/lista_reclamacoes/?id="
    #        +idEmpresa
    #        +"&page="
    #        +page
    #        +"&size=10&status=ALL"
    output_file = 'reclamacoes.tsv'
    file_header = ['Link','Id_Reclamacao','Nome_Empresa','Titulo_Reclamacao',
                  'Local_Postagem', 'Horario_Postagem', 'Topicos_Associados',
                  'Texto_Reclamacao','\n']
    quantidadeTransacoes = 1
    driver = webdriver.Chrome()

    # testa se o arquivo já existe. Se existir, remove.
    # Isso é necessário porque a cada vez que o arquivo for aberto daqui pra
    # frente ele terá apenas conteúdo adicionado
    if os.path.isfile(output_file):
        os.remove(output_file)

    # escreve cabeçalho no arquivo de saída
    with open(output_file, 'w') as f:
        f.write('\t'.join(file_header))

    for idEmpresa in Empresas:
        qt = 0
        page = 1
        ### fazer flag dos 15 minutos
        while(qt<quantidadeTransacoes):
            links = []
            while len(links) == 0:
                links, nomeEmpresa = pegaLinks(page, idEmpresa)
                if links is None:
                    break
            if links is not None and nomeEmpresa is not None:
                for item in links:
                     montaLink = "https://www.reclameaqui.com.br/" \
                                 +nomeEmpresa \
                                 +item
                     print(montaLink)
                     try:
                         inicio = time.time()
                         driver.get(montaLink)
                         final = time.time()
                         if final - inicio >= 1:
                             # para evitar erros onde não carrega a página
                             driver.refresh()
                             # estratégia para quebrar strings muito longas é
                             # colocar elas entre parênteses
                             script = ("return document.getElements"
                                       "ByTagName('html')[0].innerHTML")
                             html = driver.execute_script(script)
                         time.sleep(1)
                         info = parser.retiraInfo(html, nomeEmpresa)
                         with open(output_file, 'a') as f:
                             f.write(montaLink + '\t' + info + '\n')
                     except:
                         print( "Page Erro ! Link: " + montaLink)

            qt += 1
            page = page + 1
    driver.close()
