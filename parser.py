#-*- coding: utf-8 -*-
### parser para as páginas
import re
import unicodedata

def retiraLinks(html):
    try:
        r = [a.end() for a in re.finditer("href=\"/empresa/", html)]
        if len(r)>0:
            # essa parte vai descobrir o nome da empresa:
            # procura-se pela string dentro do finditer acima
            # se ela for encontrada, armazenda todas as respostas.
            # o finditer retorna posição de início e de fim da string buscada
            # utilizamos apenas a de fim, porque queremos o que está após essa
            # string buscada
            p = r[0]
            nomeEmpresa = []
            # seguimos, abaixo, caracter a caracter até termos o nome
            # completo da empresa em questão
            while html[p] != "/":
                    nomeEmpresa.append(html[p])
                    p=p+1

            # ou não há nome para a empresa
            if len(nomeEmpresa)==0:
                    nomeEmpresa = "semnome"

            # usando a mesma lógica para encontrar os links para cada pergunta
            r = [a.end() for a in re.finditer("href=\"/"+''.join(nomeEmpresa), html)]
            links = []
            for posicao in r:
                p = posicao
                link = []
                while html[p] != "\"":
                    link.append(html[p])
                    p=p+1
                links.append(''.join(link))

            return links, ''.join(nomeEmpresa)
    except:
        return None, None

def retiraRepetidos(topicos):
    if len(topicos)>1:
        for i in range(1, len(topicos)):
            if topicos[i] == topicos[i-1]:
                topicos.pop(i)
                if len(topicos)>=i:
                    break
    return topicos



def trataTopicosAssociados(topicosAssociados):

	for i in range(0, len(topicosAssociados)):
		topicosAssociados[i] = list(topicosAssociados[i])

	for i in range(0, len(topicosAssociados)):

		topicosAssociados[i].pop(0)
		topicosAssociados[i].pop(0)
		topicosAssociados[i].pop(0)

	for i in range(0, len(topicosAssociados)):

		topicosAssociados[i] = ''.join(topicosAssociados[i])

	topicosAssociados = sorted(topicosAssociados)
	#### agora irei retirar os elementos repetidos
	topicosAssociados = retiraRepetidos(topicosAssociados)

	t = " "
	for i in topicosAssociados:
		t = " " +  i + t 

	return t

def retiraInfo(html, nomeEmpresa):
    # pegando o título com o trecho:
    # <div class="col-md-10 col-sm-12"> <h1 class="ng-binding">
    r = [a.end() for a in re.finditer(
               "<div class=\"col-md-10 col-sm-12\"> <h1 class=\"ng-binding\">",
               html)]

    titulo = parseIt(r, html, "<")
    # print(titulo)

    # primeiro pegamos o ID
    r = [a.end() for a in re.finditer("ID: ", html)]
    idReclamacao = parseIt(r, html, "<")
    # print(idReclamacao)

    # pegando o local <ul class="local-date list-inline"> \
    #                 <li class="ng-binding">\
    #                 <img src="../../../images/pin-maps.52fa5ca3.png" \
    #                 height="14" width="10">
    var = "<ul class=\"local-date list-inline\"> <li class=\"ng-binding\"><img src=\"../../../images/pin-maps.52fa5ca3.png\" height=\"14\" \width=\"10\">"
    r = [a.end() for a in re.finditer(var, html)]
    local = parseIt(r, html, "<")
    # print(local)

    # pega o horário e data <li class="ng-binding">\
    #                       <i class="fa fa-calendar"></i>

    var = "<li class=\"ng-binding\"><i class=\"fa fa-calendar\"></i>"
    r = [a.end() for a in re.finditer(var, html)]
    horario = parseIt(r, html, "<")
    # print(horario)

    # pegando tópicos associados
    r = [a.end() for a in re.finditer("/busca/", html)]
    topicosAssociados = parseIt(r, html, "\"")
    # print(topicosAssociados)

    # pegando a reclamação <p ng-bind-html="reading.complains.\
    #                      description|textModerateDecorator" \
    #                      class="ng-binding">
    var = "<p ng-bind-html=\"reading.complains.description|textModerateDecorator\" class=\"ng-binding\">"

    r = [a.end() for a in re.finditer(var, html)]
    if len(r)==0:
        print("Erro não há dados da reclamação !")
        return

    reclamacao = parseIt(r, html, "</p>")
    reclamacao = reclamacao.replace("\n", " ")
    reclamacao = reclamacao.replace('\t', " ")

    # print(reclamacao)

    if topicosAssociados is not None:
            t = trataTopicosAssociados(topicosAssociados)
    else:
            t = "-"

    # O id da reclamação, o nome da empresa, o título da postagem, 
    # o local onde ele está, o horário em que o post foi feito,
    # tópicos associadso à postagem (se existirem) e a reclamação de fato
    info = idReclamacao[0] + '\t' + nomeEmpresa + '\t' + titulo[0] + \
           '\t' + local[0] + '\t' + horario[0] + '\t' + t + \
           '\t' + reclamacao

    return info

def parseIt(posicoes, html, final):

	retornos = []
	if final != "</p>":
		for i in range(0, len(posicoes)):
			p = posicoes[i]
			ret = []
			while html[p] != final:
				ret.append(html[p])
				p=p+1
			ret = ''.join(ret)
			
			retornos.append(ret)
		
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

	
		#retornos = unicode(retornos, 'utf-8') #### retornando a reclamação
	


	if (len(retornos)==0) or (retornos is None):
		retornos = []
		return retornos.append('-')

	else:
		return retornos
