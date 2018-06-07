# coding: utf-8
# user/bin/python
import gensim
from gensim import corpora

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

	return data


if __name__ == '__main__':
	#### parte de modelagem de tópicos
	dictionary = corpora.Dictionary(info)
	doc_term_matrix = [dictionary.doc2bow(doc) for doc in info]
	#Lda = gensim.models.ldamodel.LdaModel
	#ldamodel = Lda(doc_term_matrix, num_topics=10, id2word = dictionary, passes=50)
	ldamodel = gensim.models.ldamodel.LdaModel(corpus=doc_term_matrix,
                                           id2word=dictionary,
                                           num_topics=len(info), 
                                           random_state=100,
                                           update_every=1,
                                           chunksize=100,
                                           passes=10,
                                           alpha='auto',
                                           per_word_topics=True)

	topicos = ldamodel.print_topics(num_topics=10, num_words=4)
	t = []
	for i in range(0, len(topicos)):
		topicos[i] = str(topicos[i]).split('"')
		for j in range(0, len(topicos[i])):
			if j % 2 != 0:
				t.append(topicos[i][j])
	print t