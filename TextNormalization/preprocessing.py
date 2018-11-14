import locale
import functools
import hgtk
import numpy as np
import pandas as pd
import string
import re

class preprocess() :
    def __init__(self,text_name):
        self.corpus = self.fileopen(text_name)
        
    def fileopen(self,text_name) :
        f = open(text_name + ".txt",encoding = 'cp949',mode = "r")
        dictionary = f.read()
        words = dictionary.split('\n')
        f.close()
        return words
    
    def clean_text(self) :
        correct = list()
        words = self.corpus
        for word in words :
            if word == '':
                continue
            else :
                correct.append(word)

        # 단어 하나씩 분해
        word_deletet = list()
        A = ""
        for word in words :
            for w in word :
                if w == word[-1] :
                    word_deletet.append(A+w)
                    A=""
                elif w == '\t' :
                    word_deletet.append(A)
                    A=""
                else :
                    A = A+w

        #특수문자와 숫자 제거
        word_save_han = list()
        for word in word_deletet:
            condition_1 = re.compile("[^ㄱ-ㅎ가-힣()/]") 
            check_1 = condition_1.search(word)
            if check_1:
                word_save_han.append(re.sub('[^ㄱ-ㅎ가-힣()]','',word))
            else :
                word_save_han.append(word)

        #괄호 삭제
        deletew = ""
        word_del_ = list()
        for word in word_save_han :
            if '(' in word:
                i = word.index('(')
                word = word[:i]
                word_del_.append(word)
            else :
                word_del_.append(word)

        word_del2 = list() 
        for word in word_del_ :
            if '/' in word :
                word_del2.append(word[:word.index('/')])
                word_del2.append(word[word.index('/')+1:])
            else :
                word_del2.append(word)        
        return word_del2
    
    def prepro(self) :
        corpus_clean = self.clean_text()
        return corpus_clean