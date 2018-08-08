#encoding=utf-8
"""
计算给定数据集的熵，这是测试了解信息增益
"""
from math import log

#计算熵
def calcShannonEnt(dataSet):
    numEntries = len(dataSet)   #矩阵的行数
    labelCounts ={}
    for featVec in dataSet:
        currentLabel = featVec[-1]  #取最后一个分类标签
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel]=0
        labelCounts[currentLabel] +=1
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries   #按个数进行求概率
        shannonEnt -=prob*log(prob,2)   #直接求熵，
    return shannonEnt

#划分数据集，将第axis列中含有value值得其余列内容划分出来
def split_dataset(dataset,axis,value) :
    """
    :param axis 列
           value 列中取值
    """
    ret_dataset = list()
    for feat_vec in dataset :
        if feat_vec[axis] == value :
            reduced_feat_vec = feat_vec[:axis]  
            reduced_feat_vec.extend(feat_vec[axis+1:])
            ret_dataset.append(reduced_feat_vec)
    return ret_dataset
        

#数据集建立
def createDataSet():
    dataSet = [[1,1,'yes'],[1,1,'yes'],[1,0,'no'],[0,1,'no'],[0,1,'no']]
    labels = ['no surfacing','flippers']
    return dataSet,labels

def chose_best_feature_split(data_set) :
    num_feature = len(data_set[0]) -1   #看列数，除去分类值列
    base_entropy = calcShannonEnt(data_set)
    best_info_gain = 0.0
    best_feature = -1
    for i in range(num_feature) :
        feature_list = [example[i] for example in data_set] #取第i列内容
        unique_vals = set(feature_list)
        new_entropy = 0.0
        for values in unique_vals :
            sub_dataset = split_dataset(data_set,i,values)
            prob = len(sub_dataset)/float(len(data_set))
            new_entropy += prob*calcShannonEnt(sub_dataset)
        info_gain = base_entropy - new_entropy
        if (info_gain > best_info_gain) :
            best_info_gain = info_gain
            best_feature = i
    return best_feature

#叶子节点采用多数投票的原则取
def majority_cnt(class_list) :
    class_count={}
    for vote in class_list :
        if vote not in class_count.keys() :
            class_count[vote] = 0
        class_count[vote] += 1
    sorted_class_count = sorted(class_count.iteritems(),key = operator.itemgetter(1),
            reverse=True)   #成为一个二维数组
    return sorted_class_count[0][0]

#创建树
def create_tree(data_set,labels) :
    class_list = [example[-1] for example in data_set]
    if class_list.count(class_list[0]) == len(class_list[0]) :  #终止条件一，只有一个类型
        return class_list[0]
    if len(data_set[0]) == 1 :  #终止条件2，叶子节点，按大多数决定
        return majority_cnt(class_list)
    best_feat = chose_best_feature_split(data_set)
    best_feat_label = labels[best_feat]
    my_tree = {best_feature:{}}
    del(labels[best_feat])
    feat_vals = [example[best_feat] for exmaple in data_set]
    unique_vals = set(feat_vals)
    for value in unique :
        sub_labels = labels[:]
        my_tree[best_feat_label[value] = creat_tree(split_dataset(data_set,best_feat,value),sub_label)
    return my_tree
