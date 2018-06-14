# coding: utf-8
# user/bin/python
import nltk
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer
import string
import gensim
from gensim import corpora
import re
import unicodedata

##### esse código será responsável por fazer a modelagem de tópicos no nosso trabalho

def leitura(arquivo, posicao):

	arq = open(arquivo, "r")
	info = arq.read()
	arq.close()
	info = info.split('\n')
	data = []

	for i in range(0, len(info)):

		info[i] = info[i].split('\t')
		data.append(info[i][posicao]) ### posicao é 7 para base do reclame aqui
									### tem que olhar qual posição na base do twitter

	finalData = []
	for i in range(0, len(data)):
		for j in range(0, len(data[i])):
			finalData.append(data[i][j].lower())

	return data

def preProcessamento(info): ### pré processando os dados
	
	stop_free = " ".join([i for i in info.lower().split() if i not in stop]) ## retirando stop words
	punc_free = ''.join(ch for ch in stop_free if ch not in exclude) ### retirando pontuação

	return punc_free


def removeWords(adjectives, text):
	
	i=0
	while(i<len(text)):

		j=0
		while(j<len(text[i])):

			if len([(a.end()) for a in list(re.finditer(text[i][j], adjectives))]) != 0:

				text[i].pop(j)
				j=j-1

			j=j+1

			if len(text[i]) == 0:
				break

		if len(text) == 0:
			break

		i=i+1

	return text

def readWords(file_name):

	text_file = open(file_name, 'r')
	info = text_file.read()
	
	text_file.close()

	return info

def removeNumbers(info):
	i=0
	while(i<len(info)):
		j=0
		while(j<len(info[i])):
			if (re.match(r'^[0-9]+$', info[i][j])):
				info[i].pop(j)
				j=j-1
			j=j+1
		i=i+1

	return info


def stemming(sentence):

	stemmer = RSLPStemmer()
	phrase = []
	for word in sentence:
		word = unicode(word, 'utf-8')
		word = unicodedata.normalize("NFKD", word)
		phrase.append(stemmer.stem(word.lower()))

	return phrase

def saida(info):

	arq_saida = open("baseReclamacoes", "w")
	aux = 0
	aux2 = 0
	for i in info:
		aux2 = 0
		for j in i:
			j = unicode(j, 'utf-8')
			j = unicodedata.normalize("NFKD", j)
			if aux2<len(info[aux])-1:arq_saida.write(u''.join(j).encode('utf-8')+' ')
			else:arq_saida.write(u''.join(j).encode('utf-8'))

			aux2 = aux2+1		
		
		if aux<len(info)-1:arq_saida.write('\n')
		aux=aux+1
		
	arq_saida.close()

def removeLenWord(info, limiar): ### retira palavras com tamanho menor que uma limiar
	
	i=0
	while(i<len(info)):
		j=0
		while(j<len(info[i])):

			if len(info[i][j])<=limiar:
				info[i].pop(j)
				j=j-1
			j=j+1
		i=i+1
	return info

if __name__ == '__main__':
	
	info = leitura("tim.txt", 6)
	stop = set(stopwords.words('portuguese'))
	exclude = set(string.punctuation) 

	pontuacao = ['<br', '.', ',', '?', '!', '(', ')', ':', '-', '...', '<', '>', 'RT']
	for i in range(0, len(info)):
		for j in pontuacao:

			info[i] = info[i].replace(j, ' ')

	info = [preProcessamento(data).split() for data in info] ## ao final tenho tudo pre processado
	adjectives = readWords('lista_adjetivos')
	stop = readWords('stop_words')

	info = removeWords(adjectives, info) ### retirando adjetivos
	info = removeWords(stop, info) ### retirando stop words
	info = removeNumbers(info)
	info = removeLenWord(info, 3) ### retira palavras que tem tamanho menor igual ao número passado


	#for i in range(0, len(info)):
	#	info[i] =  stemming(info[i])


	saida(info)

