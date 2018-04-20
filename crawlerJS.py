#-*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unicodedata
import re
import parser 
import requests
### crawler para a página do reclame aqui para disciplina de mineração de dados




if __name__ == "__main__":

	idsEmpresas = ["4421", "1492", "7712", "2852"]
	page =  1
	#link = "https://www.reclameaqui.com.br/indices/lista_reclamacoes/?id="+idEmpresa+"&page="+page+"&size=10&status=ALL"

	driver = webdriver.Firefox()
	for idEmpresa in idsEmpresas:

		while(page<1000):

			driver.get("https://www.reclameaqui.com.br/indices/lista_reclamacoes/?id="+str(idEmpresa)+"&page="+str(page)+"&size=10&status=ALL")
			html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
			links, nomeEmpresa = parser.retiraLinks(html)
			#driver.close()
	
			for i in range(0, len(links)):
				#https://www.reclameaqui.com.br/vivo-celular-fixo-internet-tv/vivo-sem-fibra_VLyoNXl_8gkiMgi8/
				montaLink = "https://www.reclameaqui.com.br/"+nomeEmpresa+links[i]
				driver.get(montaLink)
				html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
				parser.retiraInfo(html, nomeEmpresa)
				#driver.close()
				exit()

				


			page = page + 1


	arq = open("saida.txt", 'w')
	html = html.encode('utf-8')
	arq.write(html)
	#print(p_element.text)


#phantomjs save_page.js https://www.reclameaqui.com.br/empresa/oi-movel-fixo-tv/ > page.html
