import pandas as pd
import numpy as np
import os
import jieba 
 
def my_cut(text): 
    
    my_words = ['哈']    
    for i in my_words:
        jieba.add_word(i)
        
    # 加载停用词
    stop_words = [] 
    with open(r"cn_stopwords.txt", 'r',encoding='utf-8') as f:
       lines = f.readlines()
       for line in lines:
           stop_words.append(line.strip())
    # stop_words[:10]
           
    return [w for w in jieba.cut(text) if w not in stop_words and len(w)>1]
 
 
 
def str2csv(filePath, s, x):
    '''
    将字符串写入到本地csv文件中
    :param filePath: csv文件路径
    :param s: 待写入字符串(逗号分隔格式)
    '''
    if x=='node':
        with open(filePath, 'w', encoding='gbk') as f:
            f.write("Label,Weight\r")
            f.write(s)
        print('写入文件成功,请在'+filePath+'中查看')
    else:
        with open(filePath, 'w', encoding='gbk') as f:
            f.write("Source,Target,Weight\r")
            f.write(s)
        print('写入文件成功,请在'+filePath+'中查看')
 
 
 
def sortDictValue(dict, is_reverse):
    '''
    将字典按照value排序
    :param dict: 待排序的字典
    :param is_reverse: 是否按照倒序排序
    :return s: 符合csv逗号分隔格式的字符串
    '''
    # 对字典的值进行倒序排序,items()将字典的每个键值对转化为一个元组,key输入的是函数,item[1]表示元组的第二个元素,reverse为真表示倒序
    tups = sorted(dict.items(), key=lambda item: item[1], reverse=is_reverse)
    s = ''
    for tup in tups:  # 合并成csv需要的逗号分隔格式
        s = s + tup[0] + ',' + str(tup[1]) + '\n'
    return s
 
 
def build_matrix(co_authors_list, is_reverse):
    '''
    根据共同列表,构建共现矩阵(存储到字典中),并将该字典按照权值排序
    :param co_authors_list: 共同列表
    :param is_reverse: 排序是否倒序
    :return node_str: 三元组形式的节点字符串(且符合csv逗号分隔格式)
    :return edge_str: 三元组形式的边字符串(且符合csv逗号分隔格式)
    '''
    node_dict = {}  # 节点字典,包含节点名+节点权值(频数)
    edge_dict = {}  # 边字典,包含起点+目标点+边权值(频数)
    # 第1层循环,遍历整表的每行信息
    for row_authors in co_authors_list:
        row_authors_list = row_authors.split(' ') # 依据','分割每行,存储到列表中
        # 第2层循环
        for index, pre_au in enumerate(row_authors_list): # 使用enumerate()以获取遍历次数index
            # 统计单个词出现的频次
            if pre_au not in node_dict:
                node_dict[pre_au] = 1
            else:
                node_dict[pre_au] += 1
            # 若遍历到倒数第一个元素,则无需记录关系,结束循环即可
            if pre_au == row_authors_list[-1]:
                break
            connect_list = row_authors_list[index+1:]
            # 第3层循环,遍历当前行词后面所有的词,以统计两两词出现的频次
            for next_au in connect_list:
                A, B = pre_au, next_au
                # 固定两两词的顺序
                # 仅计算上半个矩阵
                if A==B:
                    continue
                if A > B:
                    A, B = B, A
                key = A+','+B  # 格式化为逗号分隔A,B形式,作为字典的键
                # 若该关系不在字典中,则初始化为1,表示词间的共同出现次数
                if key not in edge_dict:
                    edge_dict[key] = 1
                else:
                    edge_dict[key] += 1
    # 对得到的字典按照value进行排序
    node_str = sortDictValue(node_dict, is_reverse)  # 节点
    edge_str = sortDictValue(edge_dict, is_reverse)   # 边
    return node_str, edge_str
 
 
if __name__ == '__main__':
    
    filePath1 = 'node.csv'
    filePath2 = 'edge.csv'
    # 读取csv文件获取数据并存储到列表中
    df = pd.read_csv('三国演义弹幕1.csv')
    df_ = [w for w in df['弹幕内容'] if len(w)>20]
    co_ist = [ " ".join(my_cut(w)) for w in df_] 
    # 根据共同词列表, 构建共现矩阵(存储到字典中), 并将该字典按照权值排序
    node_str, edge_str = build_matrix(co_ist, is_reverse=True)
    #print(edge_str)
    # 将字符串写入到本地csv文件中
    str2csv(filePath1,node_str,'node')
    str2csv(filePath2,edge_str,'edge')
