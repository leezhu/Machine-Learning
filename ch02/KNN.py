#encoding=utf-8
#K近邻算法，对电影进行分类

from numpy import *
import operator

def createDataSet():
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])  #array是numpy封装，里面是二位数组
    labels = ['A','A','B','B']
    return group,labels

#分类器
def classify0(inX,dataSet,labels,k):    #inX是目标值位置，dataSet是array数组测试样本，labels是结果标签,k是取前几个
    dataSetSize = dataSet.shape[0]   #返回列数

    #距离的计算
    diffMat = tile(inX,(dataSetSize,1))-dataSet #把目标值变成dataSetSize列的二维数组，然后将两者相减，准备求距离
    sqDiffMat = diffMat**2 #每个元素求平方
    sqDistances = sqDiffMat.sum(axis=1) #将每行求平方所得值求和
    distances = sqDistances**0.5    #开方

#   选择距离最小的点
    sortedDistIndicies = distances.argsort()    #一维数组中的值排序，从到到大，且返回的是索引
    classCount = {} 
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]  #从索引中拿样本结果标签
        classCount[voteIlabel] = classCount.get(voteIlabel,0)+1 #从字典中通过key来找到个数，然后加1


    #排序
    sortedClassCount = sorted(classCount.iteritems(),key=operator.itemgetter(1),reverse=True)#自带的字典排序功能
    return sortedClassCount[0][0]   #返回的是二维数组第一个，因为前面排序是将key和键值进行了分开然后排序，形成了二维数组

#read file data
def file2matrix(filename):
    fr = open(filename)
    arrayOfLines = fr.readlines()
    numberOfLines = len(arrayOfLines)
    returnMat = zeros((numberOfLines,3))    #取零的几行几列数组
    classLabelVector = []
    index =0
    for line in arrayOfLines
        line = line.strip()
        listFromLine = line.split('\t') #按tab进行分割
        returnMat[index,:] = listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1]))
        index +=1
    return returnMat,classLabelVector
