#-*- coding: utf-8 -*-
### parser para as páginas
import re
import unicodedata

def retiraLinks(html):

	r = [(a.end()) for a in list(re.finditer("href=\"/empresa/", html))]
	p = r[0]
	nomeEmpresa = [] #### essa parte vai descobrir o nome da empresa
	while html[p] != "/":
		nomeEmpresa.append(html[p])
		p=p+1

	###################### links para cada pergunta
	r = [(a.end()) for a in list(re.finditer("href=\"/"+''.join(nomeEmpresa), html))]
	html = list(html) ### transformando numa lista
	links = []
	for posicao in r:
		p = posicao
		link = []
		while html[p] != "\"":
			link.append(html[p])
			p=p+1
		links.append(''.join(link))

	return links, ''.join(nomeEmpresa)

def retiraInfo(html, nomeEmpresa):


	r  =[(a.end()) for a in list(re.finditer("<div class=\"col-md-10 col-sm-12\"> <h1 class=\"ng-binding\">", html))] #<div class="col-md-10 col-sm-12"> <h1 class="ng-binding">
	titulo = parseIt(r, html, "<")
	r = [(a.end()) for a in list(re.finditer("ID: ", html))] ### primeiro irei pegar o id
	idReclamacao = parseIt(r, html, "<")
	r = [(a.end()) for a in list(re.finditer("<ul class=\"local-date list-inline\"> <li class=\"ng-binding\"><img src=\"../../../images/pin-maps.52fa5ca3.png\" height=\"14\" width=\"10\">", html))] ###pegando o local <ul class="local-date list-inline"> <li class="ng-binding"><img src="../../../images/pin-maps.52fa5ca3.png" height="14" width="10">
	local = parseIt(r, html, "<")
	r = [(a.end()) for a in list(re.finditer("<li class=\"ng-binding\"><i class=\"fa fa-calendar\"></i>", html))] ### pega o horário e data <li class="ng-binding"><i class="fa fa-calendar"></i>
	horario = parseIt(r, html, "<")
	r = [(a.end()) for a in list(re.finditer("/busca/", html))] ### pegando tópicos associados
	topicosAssociados = parseIt(r, html, "\"")
	r = [(a.end()) for a in list(re.finditer("<p ng-bind-html=\"reading.complains.description|textModerateDecorator\" class=\"ng-binding\">", html))] #pegando a reclamação <p ng-bind-html="reading.complains.description|textModerateDecorator" class="ng-binding">
	reclamacao = parseIt(r, html, "</p>")

	reclamacao = reclamacao.replace("\n", " ")
	reclamacao = reclamacao.replace('\t', " ")
	t = " "
	for i in topicosAssociados:
		t = i + t + " "

	arq = open("reclameAqui.txt", "a")
	arq.write(idReclamacao[0]+'\t'+nomeEmpresa+'\t'+titulo[0]+'\t'+local[0]+'\t'+horario[0]+'\t'+t+'\t'+reclamacao+'\n')
	arq.close()
	

	#### O que foi dito pelo consumidor, o local onde ele está,  se foi respondida ou não, se foi qual a resposta
	#### o que ele falou, data e hora de postagem, tópicos associados aquela postagem


def parseIt(posicoes, html, final):

	retornos = []
	if final != "</p>":
		for i in range(0, len(posicoes)):
			p = posicoes[i]
			ret = []
			while html[p] != final:
				ret.append(html[p])
				p=p+1

			retornos.append(''.join(ret))
	else:
		p = posicoes[0]
		r = [(a.start()) for a in list(re.finditer("</p>", html))]

		for k in r:
			if k>p:
				break

		flag=0
		while p<k:
			if html[p]==">":
				flag=1
				p=p+1

			if flag==1:
				retornos.append(html[p])

			p=p+1

		retornos = ''.join(retornos)



	return retornos

