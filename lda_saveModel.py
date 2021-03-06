#encoding=utf-8
import jieba
import jieba.posseg
import jieba.analyse
import jieba.posseg as pseg
import pickle
import numpy as np
import os
import csv
import gensim
import blah
import sys
import csv
from gensim import corpora, models, similarities 
# jieba 設定斷詞
jieba.set_dictionary('jieba/dict.txt.big')
# jieba 設定停止詞
jieba.analyse.set_stop_words("jieba/stop_words.txt")
# 儲存斷詞陣列

notwants=[]
f = open('data/testcsv.csv', 'r')
not_want = open('jieba/not_want.txt', 'r')
for row in csv.reader(not_want):
    notwants.append(', '.join(row).decode('utf-8'))
finalcontent=[]
words=[]
for row in csv.reader(f):
    content=', '.join(row).decode('utf-8')
    content=content.replace(" ","")

    if(content.find('//@u')==-1 and content.find(u'转发微博')==-1 and content.find(u'转发微博')==-1):
        if not any(word in content for word in notwants ):
            if(len(content)>5):
                # jieba_word=jieba.analyse.extract_tags(content,20)
                psegwords = pseg.cut(content)

                # for line in jieba_word:
                #     print line.encode('utf-8')
                # 從此開始
                nounword=[]

                for word in psegwords:
                    if(word.flag=="n" and word.word!="" and word.word!= " "):
                        nounword.append(word.word)
                   
                
                if (nounword!=[]):
                    finalcontent.append(content)
                    words.append(nounword)
                
print "文字讀取結束"
dic = corpora.Dictionary(words)
print "轉換為字典"
dic.filter_extremes(no_below=1, no_above=0.8)#去高频词
print "去高屏詞"
corpus = [dic.doc2bow(text) for text in words]
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]#此处已经计算得出所有评论的tf-idf 值
# print tfidf[vec]
corpus_tfidf = tfidf[corpus]
documentsort=[]
if(words!=[[]]):
    # lsi = models.LsiModel(corpus_tfidf, id2word=dic, num_topics=10)
    lda = gensim.models.ldamodel.LdaModel(corpus_tfidf, id2word=dic, num_topics=20, update_every=1, chunksize=10000, passes=1)
    lda_Out=lda.print_topics(20)

    for line in lda_Out:
        for word in line:
            print word
    corpus_lda = lda[corpus_tfidf]
    # print corpus_lda[0]
    # print sorted(corpus_lda[0], key=lambda x: x[1])[-1]
   
    # print sorted(corpus_lda[0], key=lambda x: x[1])[-1][0]
    
    index=similarities.MatrixSimilarity(lda[corpus])
    query="苍井女孩"
    query_bow = dic.doc2bow(list(jieba.cut(query)))
    print query_bow
    query_lsi = lda[query_bow]
    print query_lsi

    lda.save('lda_Webo.lda')
    
    for doc in corpus_lda:       
        documentsort.append(sorted(doc, key=lambda x: x[1])[-1][0])
        # print doc

   
f = open('data/finalcsv.csv', 'w')
for x in range(len(documentsort)):
    line= str(x)+" ,"+str(documentsort[x])+" ,"+finalcontent[x]+"\n"
    # print u''.join(line).encode('utf-8')
    f.write(u''.join(line).encode('utf-8'))


f.close()
