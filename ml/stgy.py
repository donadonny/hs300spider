#coding:utf-8
import random

def stgy_top1(predict_res):
    return predict_res[0][2]        #按照预测y值最高的1个
    
def stgy_top3(predict_res):
    return sum([i[2] for i in predict_res[0:3]])/3.0

def stgy_top5(predict_res):
    return sum([i[2] for i in predict_res[0:5]])/5.0

def stgy_all(predict_res):
    return sum([i[2] for i in predict_res[0:len(predict_res)]])/len(predict_res)

def stg_random(predict_res):
    i = random.randint(0,len(predict_res))
    return predict_res[i][2]