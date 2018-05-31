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

		if links != None:
			for i in range(0, len(links)):
				
				if i>=len(links):
					break
				
				if len([(a.end()) for a in list(re.finditer("https://www.reclameaqui.com.br/"+nomeEmpresa, links[i]))]) == 0:
					links.pop(i)

		return links, nomeEmpresa

	except:

		return None, None


	


if __name__ == "__main__":

	idsEmpresas = ["4421", "1492", "7712", "2852"]

	#link = "https://www.reclameaqui.com.br/indices/lista_reclamacoes/?id="+idEmpresa+"&page="+page+"&size=10&status=ALL"

	driver = webdriver.Chrome()
	for idEmpresa in idsEmpresas:

		page = 1

		while(page<100):

			links = []
			while len(links) == 0:

				links, nomeEmpresa = pegaLinks(page, idEmpresa)
			
			if links != None:
				
				for i in range(0, len(links)):
					
					montaLink = "https://www.reclameaqui.com.br/"+nomeEmpresa+links[i]
					print montaLink
					try:
						driver.get(montaLink)
						html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
						parser.retiraInfo(html, nomeEmpresa)
					except:
						print "Page Erro ! Link: " + montaLink
				

				
			page = page + 1


	arq = open("saida.txt", 'w')
	html = html.encode('utf-8')
	arq.write(html)
	#print(p_element.text)

