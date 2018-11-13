from numpy import *
import re
import os

def CombFile(dirpath,date,resultfile):
    filedir = dirpath    ##获取目标文件夹的路径
    filenames = os.listdir(filedir)    #获取当前文件夹中的文件名称列表
    filenames.sort()    #排序
    with open(resultfile, 'w') as f:
        # 先遍历文件名
        for filename in filenames:
            if date in filename:
                filepath = filedir + '/' + filename
                # 遍历单个文件，读取行数
                for line in open(filepath):
                    f.writelines(line)

def CombFile02(dirpath,resultfile):
    filedir = dirpath    ##获取目标文件夹的路径
    filenames = os.listdir(filedir)    #获取当前文件夹中的文件名称列表
    filenames.sort()    #排序
    with open(resultfile, 'w') as f:
        # 先遍历文件名
        for filename in filenames:
            if '.txt' in filename:
                filepath = filedir + '/' + filename
                # 遍历单个文件，读取行数
                for line in open(filepath):
                    f.writelines(line)

def loadDataSet(fileName):
    YMD = []    #年月日
    HMS = []    #时分秒
    dataSet = []    #采集数据:太阳、噪声源、冷空
    with open(fileName) as fr:
        for line in fr.readlines():
            line = line.strip()
            line = re.sub(' +', ' ', line)
            curLine = re.split(" ", line)
            #print(curLine)
            YMD.append(curLine[0])
            HMS.append(curLine[1])
            fltLine = float(curLine[3])   #转变成浮点数
            #print(fltLine)
            dataSet.append(fltLine)
    return YMD,HMS,dataSet

def GetR(HMS,dataSet):
    RS = []    #太阳
    RN = []    #噪声源
    RB = []    #冷空
    m = len(HMS)
    #time0 = HMS.index('07:00:00')
    time1S = HMS.index('09:00:00')
    time1N = HMS.index('09:03:00')
    time1B = HMS.index('09:06:00')
    time2S = HMS.index('12:00:00')
    time2N = HMS.index('12:03:00')
    time2B = HMS.index('12:06:00')
    time3S = HMS.index('15:00:00')
    time3N = HMS.index('15:03:00')
    time3B = HMS.index('15:06:00')
    #timeEND = HMS.index('16:00:00')
    for i in range(0,time1S):
        RS.append(dataSet[i])
    for i in range(time1S,time1N):    #09:00:00 - 09:02:59
        RN.append(dataSet[i])
    for i in range(time1N,time1B):    #09:03:00 - 09:05:59
        RB.append(dataSet[i])
    for i in range(time1B,time2S):
        RS.append(dataSet[i])
    for i in range(time2S,time2N):    #12:00:00 - `12:02:59
        RN.append(dataSet[i])
    for i in range(time2N,time2B):    #12:03:00 - 12:05:59
        RB.append(dataSet[i])
    for i in range(time2B,time3S):
        RS.append(dataSet[i])
    for i in range(time3S,time3N):    #15:00:00 - 15:02:59
        RN.append(dataSet[i])
    for i in range(time3N,time3B):    #15:03:00 - 15:05:59
        RB.append(dataSet[i])
    for i in range(time3B,m):
        RS.append(dataSet[i])
    return RS,RN,RB

def calS0(RS,RN,RB,S=100):
    RS_M = mean(RS)
    RN_M = mean(RN)
    RB_M = mean(RB)
    S0 = S * RN_M / (RS_M - RB_M + 1e-7) #加上1e-7防止除0
    #print('RS:',RS_M,'    RN:',RN_M,'    RB:',RB_M)
    return S0

def PredictS(RS,RN,RB,S0):
    RS_M = mean(RS)
    RN_M = mean(RN)
    RB_M = mean(RB)
    S = S0 * (RS_M - RB_M)/RN_M
    return S

def MyTest(dirpath,S0_M=648):
    #dirpath = input('请输入文件夹的路径：')
    #/Users/sunxin/Documents/大四上/项目设计/11月20-24/23
    CombFile02(dirpath,dirpath+'/testdata.txt')    #将该文件夹下所有txt文件合并
    #filedate = input('请输入日期（格式如：2018-07-06）：')
    myTMD, myHMS, myData = loadDataSet(dirpath+'/testdata.txt')
    RS, RN, RB = GetR(myHMS, myData)
    S = PredictS(RS, RN, RB, S0_M)    #计算F107指数
    #print('当天的F107指数是：'.format(),S)
    os.remove(dirpath+'/testdata.txt')   #删除文件
    return S

#MyTest()
