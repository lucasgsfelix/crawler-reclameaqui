#-*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unicodedata
import re
import parser 
import requests
import time
### crawler para a página do reclame aqui para disciplina de mineração de dados

def pegaLinks(page, idEmpresa):

	try:
		driver.get("https://www.reclameaqui.com.br/indices/lista_reclamacoes/?id="+str(idEmpresa)+"&page="+str(page)+"&size=10&status=ALL")
		html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
		links, nomeEmpresa = parser.retiraLinks(html)

		links = retiraLinksProibidos(links)


		return links, nomeEmpresa

	except:

		return None, None

def retiraLinksProibidos(links):

	arq = open("Aux/links_proibidos")
	links_proibidos = arq.read()
	links_proibidos = links_proibidos.split('\n')
	arq.close()

	if links is not None:
		i=0
		while i<len(links):
			
			j=0
			while j<len(links_proibidos):

				if links[i] == links_proibidos[j]:

					links.pop(i) ## retirando o link proibido
					i=i-1
					break
				
				j=j+1

			i=i+1

	return links

	
if __name__ == "__main__":

	#idsEmpresas = ["4421", "1492", "7712", "2852"]
	idsEmpresas = ['2852']
	#link = "https://www.reclameaqui.com.br/indices/lista_reclamacoes/?id="+idEmpresa+"&page="+page+"&size=10&status=ALL"
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
					print montaLink
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
						print "Page Erro ! Link: " + montaLink

					if flag == 1:
						qt=qt+1
						flag=0
				
			page = page + 1


	arq = open("saida.txt", 'w')
	html = html.encode('utf-8')
	arq.write(html)
	#print(p_element.text)

