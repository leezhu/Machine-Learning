#encoding=utf-8

"""
Created on 2019/08/14
@author:leezhu
"""

from numpy import *

def loadDataSet():
    postingList=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                 ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                 ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                 ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                 ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0,1,0,1,0,1]    #1 is abusive, 0 not
    return postingList,classVec
                 
def createVocabList(dataSet):
    vocabSet = set([])  #create empty set
    for document in dataSet:
        vocabSet = vocabSet | set(document) #union of the two sets
    return list(vocabSet)
#词集模型，出现多次只记录为1
def setOfWords2Vec(vocabList, inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else: print "the word: %s is not in my Vocabulary!" % word
    return returnVec
#词袋模型，多次出现累加
def setOfWords2Vec(vocabList, inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1
        else: print "the word: %s is not in my Vocabulary!" % word
    return returnVec
#训练函数
def train_NBO(train_matrix,train_category):
	num_trains_doc = len(train_matrix)	#训练数据的行数
	num_words = len(train_matrix[0])	#单词向量的个数
	p_abusive = sum(train_category)/float(num_trains_doc)	#敏感词是为1，因此就是一个类别的个数
	p_0_num = ones(num_words)
	p_1_num = ones(num_words)
	p_0_denom = 2.0
	p_1_denom = 2.0
	for i in range(num_trains_doc):
		if train_category[i] == 1:
			p_1_num += train_matrix[i]
			p_1_denom += sum(train_matrix[i])	#这里就是统计p(w0|c)概率)
		else:
			p_0_num += train_matrix[i]
			p_0_denom += sum(train_matrix[i])
	p1_vect = log(p_1_num/p_1_denom)	
	p0_vect = log(p_0_num/p_0_denom)	
	return p0_vect,p1_vect,p_abusive

#朴素贝叶斯分类函数
def classifyNB(vec2Classify,p0Vec,p1Vec,pClass):
    p1 = sum(vec2Classify * p1Vec) + log(pClass)
    p0 = sum(vec2Classify * p0Vec) + log(1.0-pClass)
    if p1 > p0:
        return 1
    else:
        return 0

#测试分类函数
def testingNB():
    listOPosts,listClasses = loadDataSet()
    myVocabList = createVocabList(listOPosts)
    trainMat=[setOfWords2Vec(myVocabList,postingdoc) for postingdoc in listOPosts]
    p0V,p1V,pAb = train_NBO(trainMat,listClasses)
    testEntry=['love','my','dalmation']
    thisDoc = setOfWords2Vec(myVocabList,testEntry)
    print testEntry,'classify as:',classifyNB(thisDoc,p0V,p1V,pAb)

