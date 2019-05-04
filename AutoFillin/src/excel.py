import time
from datetime import datetime
from datetime import timedelta
from datetime import date
import openpyxl
from xlutils.copy import copy
import pandas as pd


#返回今天的日期 格式：2019-04-17
def getDate():
    day=date.today()
    return day

#0-6分别代表周一至周日（判断相应加分时使用）
def getWeek():
    w = datetime.now().weekday()
    return w

#返回第二列
def takeSecond(elem):
    return elem[1]

#按步数从高到低降序排列
def specialSort(listz):
  
    listz.sort(reverse=True,key=takeSecond)
    return listz

#加分规则:
def points(listz):
    score=[x[1] for x in listz];
    #score = list(map(int, score))
    week=getWeek()
    if (week>=0 and week<=4):
        if(score[0]>10000):
            score[0]=0.2
        else:
            score[0]=0
        if(score[1]>10000):
            score[1]=0.15
        else:
            score[1]=0
        if(score[2]>10000):
            score[2]=0.10
        else:
            score[2]=0
        for i in range(len(score)-3):
            if(score[3+i]>10000):
                score[3+i]=0.05
            else:
                score[3+i]=0
    else:
       if(score[0]>8000):
            score[0]=0.2
       if(score[1]>8000):
            score[1]=0.15
       if(score[2]>8000):
            score[2]=0.10
       for i in range(len(score)-3):
            if(score[3+i]>8000):
                score[3+i]=0.05
            else:
                score[3+i]=0
    return score

#把得分按照学号顺序排列(excel中学号的列表，步数与学号的二维列表，换算后对应得分的列表)
def IdSort(IdNums,bfScores,afScores):
    l=len(IdNums)
    array=IdNums
    for i in range(l):
        for j in range(l):
            if IdNums[i]==bfScores[j][0]:
                array[i]=afScores[j]
    return array

#追加一列数据
def insert(path,data,SOT):
    wb=openpyxl.load_workbook(path)
    ws=wb.worksheets[0]
    ws.insert_cols(3)
    for index,row in enumerate(ws.rows):
        if index==0:
            row[2].value=getDate()
        for i in range(len(data)):
            # print(row[1].value,"--",data[i][0])
            if row[1].value==data[i][0]:
                # print("true")
                row[2].value=SOT[i]
    wb.save(path)
 
    #获取表格中学号的顺序，学号在第二行
def getIdlist(path, sheet_name):
    df=pd.read_excel(path,usecols=[1],names=None)
    df_li = df.values.tolist()
    result = []
    for s_li in df_li:
        result.append(s_li[0])
    return result

#Run
def XlsRun(path,sheet,data):
    #先处理数据
    specialSort(data)
    ScoresOfToday=points(data)
    #填入第三行
    #Idlist=getIdlist(path, sheet)#一个与第二列数据一样的list
    insert(path,data,ScoresOfToday)

# TestArray2=[[201892231,8888],[201892475,12345],[201892547,22222],[201899999,10001]]
# TestArray=[[201892210,3668],[201892433,31588],[201892270,9337],[201892344,16044],[201892457,15252],   
#           [201892230,16722],[201892111,11808],[201892222,22227],[201892241,8060],[201892345,6951]]
# TestArray3=[[170600202,12222],[181020224,8888],[181020126,7777],[170600204,8887],[180600302,15776],
#             [160600330,22222],[171020208,12333],[180600219,18836]]
# XlsRun("xx.xlsx","Sheet1",TestArray3)
