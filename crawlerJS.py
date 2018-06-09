#-*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unicodedata
import re
import parser 
import requests
### crawler para a página do reclame aqui para disciplina de mineração de dados

def pegaLinks(page, idEmpresa):

	try:
		driver.get("https://www.reclameaqui.com.br/indices/lista_reclamacoes/?id="+str(idEmpresa)+"&page="+str(page)+"&size=10&status=ALL")
		html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
		links, nomeEmpresa = parser.retiraLinks(html)

		if links is not None:
			for i in range(0, len(links)):
				
				if i>=len(links):
					break
				
				if len([(a.end()) for a in list(re.finditer("https://www.reclameaqui.com.br/"+nomeEmpresa, links[i]))]) == 0:
					links.pop(i)

		return links, nomeEmpresa

	except:

		return None, None


	


if __name__ == "__main__":

	#idsEmpresas = ["4421", "1492", "7712", "2852"]
	idsEmpresas = ['7712']
	#link = "https://www.reclameaqui.com.br/indices/lista_reclamacoes/?id="+idEmpresa+"&page="+page+"&size=10&status=ALL"
	quantidadeTransacoes = 10000
	flag=0
	driver = webdriver.Chrome()
	for idEmpresa in idsEmpresas:

		qt = 0
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
						driver.get(montaLink)
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

