#-*- coding: utf-8 -*-

from __future__ import division
from collections import Counter
import math as calc
import re
import hgtk
import tensorflow as tf

def splitWord(word):
    word = re.sub('ㅙ','ㅗㅐ',word)
    word = re.sub('ㅘ','ㅗㅏ',word)
    word = re.sub('ㅚ','ㅗㅣ',word)
    word = re.sub('ㅞ','ㅜㅔ',word)
    word = re.sub('ㅟ','ㅜㅣ',word)
    word = re.sub('ㅞ','ㅜㅔ',word)
    word = re.sub('ㅝ','ㅜㅓ',word)
    word = re.sub('ㅢ','ㅡㅣ',word)
    word = re.sub('ㅖ','ㅕㅣ',word)
    word = re.sub('ㅒ','ㅑㅣ',word)
    word = re.sub('ㄲ','ㄱㄱ',word)
    word = re.sub('ㄸ','ㄷㄷ',word)
    word = re.sub('ㅃ','ㅂㅂ',word)
    word = re.sub('ㅆ','ㅅㅅ',word)
    word = re.sub('ㅉ','ㅈㅈ',word)
    word = re.sub('ㄳ','ㄱㅅ',word)
    word = re.sub('ㄵ','ㄴㅈ',word)
    word = re.sub('ㄶ','ㄴㅎ',word)
    word = re.sub('ㄺ','ㄹㄱ',word)
    word = re.sub('ㄻ','ㄹㅁ',word)
    word = re.sub('ㄼ','ㄹㅂ',word)
    word = re.sub('ㄽ','ㄹㅅ',word)
    word = re.sub('ㄾ','ㄹㅌ',word)
    word = re.sub('ㄿ','ㄹㅍ',word)
    word = re.sub('ㅀ','ㄹㅎ',word)
    word = re.sub('ㅄ','ㅂㅅ',word)
    return word

class nGram():
#unigram & bigram에 대한 Maximum Likelihood Probabilistic Language Model(Laplace Add-1 smoothing)를 생성하고 hash-able dictionary형태로 저장. 

# 사용예시:
# >>> ng = nGram(True, True, True)
# >>> print ng.sentenceprobability('hold your horses', 'bi', 'log')
# >>> -18.655540764

    def __init__(self, uni=False, bi=False):
        # 말뭉치를 load해서 파라미터에 따라 unigram / bigram 생성
        self.words = self.loadCorpus()
        #self.createUnigram(self.words)
        if uni : 
            self.unigram=self.createUnigram(self.words)#self.make_ngram(self.words,1) 
            self.trigram=self.createTrigram(self.words)#self.make_ngram(self.words,3) 
        if bi : self.bigram=self.createBigram(self.words)#self.make_ngram(self.words,2) 
        return
    
    def loadCorpus(self):
        # 원시말뭉치 load
	# 말뭉치는 문장의 시작에 <s>으로 sentence start token을 삽입하여 문장단위를 구별할 수 있음.
	# 예시) <s> first interstate has 42 franchise banks that offer first interstate financial services in ten states
        print ("Loading Corpus from data file")
        corpusfile = open('corpus_test.txt',encoding = 'utf-16', mode='r') # "corpus.txt"는 utf-8, "corpus_test"는 utf-16
        corpus = corpusfile.read()
        corpusfile.close()
        print ("Processing Corpus")
        words = corpus.split('\n')
        word_clear = []
        condition = re.compile('[ㄱ-ㅎ가-힣 ]+')        # 문장부호, 영어, 한자등은 삭제. 한글, 띄어쓰기만 남겨둠.
    #    condition.search()
        for i in range(len(words)) :
            clear_sentence = condition.findall(words[i])

        for i in range(len(clear_sentence)) :
            if clear_sentence[i] == ' ' :
                continue
            else : word_clear.append(' '.join(clear_sentence[i]))
        self.corpus = word_clear
        return word_clear
   
    def make_ngram(self,morphs,n):
        ngram = []
        n_append = ngram.append
        for sent in morphs:
            split = sent.split(' ')
            for i in range(len(split)):
                if i < len(split)-n+1:
                    n_append(' '.join(split[i:i+n]))
        return ngram
    
    def createUnigram(self, words):
        # 말뭉치에서 load된 단어에 대한 unigram 생성.
        # Counter함수를 이용해서 count해서 *'단어':횟수* 형식으로 저장함.
        print("Creating Unigram Model")
        unigram = dict()
        unigramfile = open('unigram.txt', encoding='utf-8',mode='w')
        print("Calculating Count for Unigram Model")
        unigram = Counter(words)
        #unigramfile.write(str(unigram))
        #unigramfile.close()
        return unigram

    def createBigram(self, words):
        # 말뭉치에서 load된 단어에 대한 bigram 생성
	# 두 단어를 공백과 같이 붙여서 시퀀스를 생성하고 counter함수를 이용해서 *'단어 단어':횟수* 형식으로 저장함.         

        print("Creating Bigram Model")
        biwords = []
            
        for index, item in enumerate(words):
            if index==len(words)-1:
                break
            biwords.append(item+' '+words[index+1])
        print("Calculating Count for Bigram Model")
        bigram = dict()
        #bigramfile = open('bigram.data', 'w')
        bigram = Counter(biwords)
        #bigramfile.write(str(bigram))
        #bigramfile.close()
        return bigram

    def createTrigram(self,words) :
        # trigram 생성. 
        # 세 단어를 공백과 같이 붙여서 시퀀스 생성, counter 함수를 이용해 "'단어 단어 단어':횟수" 저장
        print("Creating Trigram Model")
        triwords = []
        for index,item in enumerate(words):
            if index == len(words)-2 :
                break
            triwords.append(item+' '+words[index+1]+' '+words[index+2])
        print("Calculating Count for Trigram Model")
        trigram = dict()
        trigram = Counter(triwords)
        return trigram

    def cal_biProb(self, uni_count, bi_count, texts):
        Probs = []
        P = 0.0
        P_append = Probs.append
        for text in texts:
            morphs =[]
            m_append = morphs.append
            split = text.split(' ')
            for i in range(len(split)):# text bigram 형태로 만듦
                if i != len(split)-1:
                    m_append(' '.join(split[i:i+2]))
            Prob = 1
            for m in morphs: # bigram 확률 계산
                w = m.split(' ')
                try:
                    numer = float(bi_count[m]) + 1 # +1 스무딩
                except:
                    numer = 1 # OOV 일때 1이 분자로
                try:
                    denom = float(uni_count[w[0]]) + 1 # +1 스무딩
                except:
                    denom = 31055413 + 1 # OOV 일때 분모는 전체 morph 계산
                Prob = Prob * (numer/denom)
    #            print('\'{}\'의 확률 {} / {} = {}'.format(m, numer,denom,numer/denom))
            P_append(Prob)
        P = max(Probs)
     #   P = float(("%0.10f"%P))
        return P

    def cal_triProb(self, bi_count, tri_count, texts):
        Probs = []
        P=0.0
        P_append = Probs.append
        for text in texts:
            morphs =[]
            m_append = morphs.append
            split = text.split(' ')
            for i in range(len(split)):# text trigram 형태로 만듦
                if i < len(split)-2:
                    m_append(' '.join(split[i:i+3]))
            Prob = 1
            for m in morphs: # trigram 확률 계산
                w = m.split(' ')
                try:
                    numer = float(tri_count[m]) + 1 # +1 스무딩
                except:
                    numer = 1 # OOV 일때 1이 분자로
                try:
                    denom = float(bi_count[' '.join(w[:2])]) + 1 # +1 스무딩
                except:
                    denom = 31055413 + 1 # OOV 일때 분모는 전체 morph 계산
                Prob = Prob * (numer/denom)
          #      print('\'{}\'의 확률 {} / {} = {}'.format(m, numer,denom,numer/denom))
            P_append(Prob)
        P = max(Probs)
     #   P = float(("%0.10f"%P))
        return P
    
    def probability(self, word, words = "",words_n = "", gram = 'uni'):
        # 구한 unigram과 bigram으로 단어의 maximum likelihood probability를 구함.
	# 우변 1을 더하는 이유 & 좌변에 unigram의 길이를 더하는 이유 -> Add-1 Smoothing이용
	# unigram의 분모에는 전체 corpus의 단어의 개수가 들어감.
	# bigram의 분모에는 앞에오는 단어(given)가 출현하는 횟수가 들어감.
        #unigram = self.unigram
        #bigram = self.bigram
        #trigram = self.trigram
        unigram = self.make_ngram(self.corpus,1)
        bigram = self.make_ngram(self.corpus,2)
        trigram = self.make_ngram(self.corpus,3)
        uni_count = dict(Counter(unigram))
        bi_count = dict(Counter(bigram))
        tri_count = dict(Counter(trigram))
        
        if gram == 'uni':
            return calc.log((self.unigram[word]+1)/(len(self.words)+len(self.unigram)))
        elif gram == 'bi':
            return calc.log(self.cal_biProb(uni_count, bi_count, words))
            #return calc.log((self.bigram[words]+1)/(self.unigram[word]+len(self.unigram)))
        elif gram == 'tri':
            return calc.log(self.cal_triProb(bi_count, tri_count, words_n))
            #return calc.log(float(self.trigram[words_n]+1), 2) - calc.log(float(self.bigram[words]+1), 2)

    def sentenceprobability(self, sentence, gram='uni', form='antilog'):
	# 문장과 n-gram방식, 확률계산 방식을 paramter로 입력받아서 그에 따라 문장의 Maximum LIkelihood Probability를 계산.     
        words = list()
        for w in sentence :
            if w==' ':
                continue
            words.append(w)
        P=0.0
        if gram == 'uni':
            for index, item in enumerate(words):
                P = P + self.probability(item)
        if gram == 'bi':
            for index, item in enumerate(words):
                if index == len(words)- 1: break
                P = P + self.probability(item, words = item+words[index+1],gram =  'bi')
        if gram == 'tri':
            for index, item in enumerate(words):
                if index == len(words)-2 : break
                P = P + self.probability(item, item+words[index+1],item+words[index+1]+words[index+2],'tri')
        
        if form == 'log':
            return P
	# calc.pow(calc.e,P)는 exp(P)를 뜻함. 따라서 P가 자연로그 상태이기 때문에 실수 확률이 리턴됨.
        elif form == 'antilog':
            return calc.pow(calc.e, P)

help(nGram)
