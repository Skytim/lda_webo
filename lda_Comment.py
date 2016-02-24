from gensim import corpora, models, similarities 
import gensim

ldaModel = gensim.models.LdaModel.load('lda_Webo.lda')

lda_Out=ldaModel.print_topics(20)
for line in lda_Out:
	for word in line:
		print word