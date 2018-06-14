# coding: utf-8
#!/usr/bin/env python
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
import unicodedata

def leitura(arquivo):

	arq = open(arquivo, "r")
	info = arq.read()
	arq.close()
	info = info.split('\n')
	for i in range(0, len(info)):
		info[i]=info[i].split(' ')

	for i in range(0, len(info)):
		for j in range(0, len(info[i])):
			info[i][j] = info[i][j].decode('unicode_escape').encode('ascii','ignore')

	return info

def returnTopics(topicos):

	t = []
	
	for i in range(0, len(topicos)):
		topicos[i] = str(topicos[i]).split('"')
		for j in range(0, len(topicos[i])):
			if j % 2 != 0:
				t.append(topicos[i][j])
	return t

def make_bigrams(texts):
    return [bigram_mod[doc] for doc in texts]

def make_trigrams(texts):
    return [trigram_mod[bigram_mod[doc]] for doc in texts]

if __name__ == '__main__':
	#### parte de modelagem de tópicos
	info = leitura('baseReclamacoes2')
	### bigramas e trigramas são conjuntos de duas e três palavras que co-ocorrem com muita frequência
	bigram = gensim.models.Phrases(info, min_count=5, threshold=100) # quanto maior o threshold menor o tamanho das frases
	trigram = gensim.models.Phrases(bigram[info], threshold=100)  

	bigram_mod = gensim.models.phrases.Phraser(bigram)
	trigram_mod = gensim.models.phrases.Phraser(trigram)


	dictionary = corpora.Dictionary(info)
	doc_term_matrix = [dictionary.doc2bow(doc) for doc in info]

	ldamodel = gensim.models.ldamodel.LdaModel(corpus=doc_term_matrix,
                                           id2word=dictionary,
                                           num_topics=10, 
                                           random_state=100,
                                           update_every=1,
                                           chunksize=100,
                                           passes=10,
                                           alpha='auto',
                                           per_word_topics=True)

	topicos = ldamodel.top_topics(corpus=doc_term_matrix, dictionary=dictionary, coherence='u_mass', topn=1, processes=-1)
	print topicos
	#t = returnTopics(topicos)
	#doc_lda = ldamodel[doc_term_matrix]
	# Perplexity é uma medida de quão bom o modelo é, quanto menor melhor
	#print 'Perplexity: ', ldamodel.log_perplexity(doc_term_matrix)  
	#coherence_model_lda = CoherenceModel(model=ldamodel, texts=info, dictionary=dictionary, coherence='c_v')
	#coherence_lda = coherence_model_lda.get_coherence()
	#print coherence_lda

