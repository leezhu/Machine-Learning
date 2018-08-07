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
    for line in arrayOfLines :
        line = line.strip()
        listFromLine = line.split('\t') #按tab进行分割
        returnMat[index,:] = listFromLine[0:3]  #将一行的list数据放入矩阵的每行当中
        classLabelVector.append(listFromLine[-1])  #将末尾的目标值放入单独的分类vector
        index +=1
    return returnMat,classLabelVector

#添加归一化特征值
def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet))  #按照dataSet的维度来建立零矩阵
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals,(m,1)) #往y轴方向复制m行
    normDataSet = normDataSet/tile(ranges,(m,1))    #这是范围值矩阵
    return normDataSet,ranges,minVals

#分类器针对约会网站的测试代码
def datingClassTest():
    hoRatio = 0.10
    datingDataMat,datingLabels = file2matrix('datingTestSet.txt')
    normMat,ranges,minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m*hoRatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        #是将10%的测试数据作为目标值，求每行目标值与实际值最相近的距离，并取出结果。如果最相近的值与结果值不同，那么就是错误值
        classifierResult = classify0(normMat[i,:],normMat[numTestVecs:m,:],datingLabels[numTestVecs:m],3)
        print "the classifier came back with:%s,the real answer is: %s " % (classifierResult,datingLabels[i])
        if (classifierResult!=datingLabels[i]):
            errorCount +=1.0
        print "the total error rate is: %f" %(errorCount/float(numTestVecs))

#构建系统化的应用
def classifyPerson():
    resultList = ['not at all','n small doses','in large doses']
    percentTats = float(raw_input("percentage of time spent playing video games?"))
    ffMiles = float(raw_input("frequen flier miles earned per year?"))
    iceCream = float(raw_input("liters of ice cream consumed per year?"))
    datingDataMat,datingLabels = file2matrix('datingTestSet.txt')
    normMat,ranges,minVals= autoNorm(datingDataMat)
    inArr = array([ffMiles,percentTats,iceCream])
    classifierResult = classify0((inArr-minVals)/ranges,normMat,datingLabels,3) #测试目标值也需要归一化
    print("You will probably like this person:%s" % classifierResult)




#识别系统代码添加
#图像元素转矩阵
def img2vector(filename):
    returnVect =zeros((1,1024))
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnVect[0,32*i+j]=int(lineStr[j])    #0行，为了按32*32二维来存一维的
    return returnVect


#手写数字识别系统的测试代码
def handwritingClassTest():
    hwLabels=[]
    trainingFileList = listdir('traningDigits')
    m = len(traningFileList)    #获取个数
    for i in range(m):
        fileNameStr=trainingFileList[i]
        fileStr = fileNameStr.split('.')[0] #将文件名拆分，取其名称
        classNumStr = int(fileStr.split('_')[0])    #取文件序号,就是识别的号码
        hwLabels.append(classNumStr)
        trainingMat[i,:]=img2vector('trainingDigits/%s' % fileNameStr)
    testFileList = listdir('testDigits')
    errorCount=0.0
    mTest = len(testFileList)
    #对测试集也做处理
    for i in range(mTest):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split('.')[0]
        classNumStr = int(fileStr.split('_')[0])
        vectorUnderTest = img2vector('testDigits/%s' % fileNameStr)
        classifierResult = classify0(vectorUnderTest,trainingMat,hwLabels,3)
        print "the classifier came back with:%d,the real answer is:%d" % (classifierResult,classNumStr)
        if (classifierResult != classNumStr):
            errorCount +=1.0
    print "\nthe total number of errors is:%d" % errorCount
    print "\nthe total error rate is:%f" % (errorCount/float(mTest))
