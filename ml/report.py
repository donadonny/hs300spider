#coding:utf-8
import sys
import subprocess,math
sys.path.append("../")
sys.path.append("../feature")
from util import *
import datetime,random
import feature_generation_entry as fge
import threading, time 
import ttp


model_file = 'd:\\stock_data\\GBDT_MODEL'
feature_num = 74
norm_rules = 'd:\\stock_data\\norm_rules'

def train_model(yday):
    orign_data = "d:\\stock_data\\orign_data.txt"
    orign_label_data = "d:\\stock_data\\orign_label_data.txt"
    norm_data = "d:\\stock_data\\norm_data.txt"
    predict_file = 'd:\\stock_data\\GBDT_MODEL.predict'

    #生成训练\测试数据
    fd = open(orign_data,'w')
    labelFD = open(orign_label_data,'w')
    fge.generate_data(fd,y_day,date_range=90,labelFD=labelFD)
    
    #规则化数据
    ttp.normalize_data(orign_data, norm_data, norm_rules,restore=False)
    
    #训练模型
    ttp.gbdt_train(norm_data, model_file, predict_file, feature_num)
    

def predict(y_day):
    orign_data = "d:\\stock_data\\predict\\orign_data.txt"
    orign_label_data = "d:\\stock_data\\predict\\orign_label_data.txt"
    norm_data = "d:\\stock_data\\predict\\norm_data.txt"
    predict_file = 'd:\\stock_data\\predict\\data.predict'
    
    #生成预测数据集
    fd = open(orign_data,'w')
    labelFD = open(orign_label_data,'w')
    fge.generate_data(fd,y_day,date_range=1,labelFD=labelFD) 
    
    #规则化数据
    ttp.normalize_data(orign_data, norm_data, norm_rules,restore=True)
    
    #预测数据
    ttp.gdbt_predict(model_file,feature_num,norm_data,predict_file)


def generator_html(yday,res):
    def render_tb_header():
        return """<tr><th>StockName</th><th>YDAY</th><th>Y</th><th>Y_HAT(⇊)</th></tr>"""
    
    def __helper_0(v):
        if v>0:return '#FF0000'
        else:return '#009900'
    def __helper_1(v):
        return '<FONT COLOR="%s">%f</FONT>' % (__helper_0(v),v)
    def __helper_2(ls):
        t = ls[:]
        t[2] = __helper_1(ls[2])
        t[3] = __helper_1(ls[3])
        return tuple(t)
    def render_summary():
        N = len(res)
        if N <=0:return ""
        TP=0
        FP=0
        TN=0
        FN=0
        for item in res:
            if item[3] >0:
                if item[2] >0:TP+=1
                else:FP+=1
            else:
                if item[2] <0:TN+=1
                else:FN+=1
        ALL_P = TP + FN
        ALL_N = TN + FP
        html = ""
        html += "N=%d<br>"%N
        html += "TP=%d,FN=%d<br>"%(TP,FN)
        html += "TN=%d,FP=%d<br>"%(TN,FP)
        html += "ALL_P=%d<br>"%ALL_P
        html += "ALL_N=%d<br>"%ALL_N
        
        html += "RANDOM BUY: %f%%<br>" % (ALL_P*100.0/N)
        html += "MODEL BUY: %f%%<br>"  % (TP*100.0/(TP+FP))        
        html += "RANDOM SELL: %f%%<br>" % (ALL_N*100.0/N)
        html += "MODEL SELL: %f%%<hr>" % (TN*100.0/(TN+FN))
        return html
    def render_data_item(item):
        return """<tr><th>%s</th><th>%s</th><th>%s</th><th>%s</th></tr>""" %__helper_2(item)
    def render_tb_body():
        sorted_res = sorted(res, cmp=lambda x,y:cmp(x[3],y[3]),reverse=True)
        eles = [render_data_item(item) for item in sorted_res]
        return '\n'.join(eles)
    def render_head():
        return """<head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
	<title>%s 模型预测结果</title>
	<style>
        table, th, td {
          border: 1px solid black;
          border-collapse: collapse;
        }
        th, td {
          padding: 5px;
          text-align: left;
        }
        </style>
        </head>"""%yday
    def render_table():
        return """<table class="reference" style="width:100%%">%s %s<tbody></tbody></table>"""%(render_tb_header(),render_tb_body())
    def render_body():
        return """<body><h2>Stock Price Prediction For %s </h2> %s <br/>%s <body>""" % (yday,render_summary(),render_table())
    def render_html():
        return """<html lang="en-US" style="height: 100%%;"> %s %s</html>"""%(render_head(),render_body())
    
    html_file  ='d:\\stock_data\\report\\%s.html'%yday
    open(html_file,'w').write(render_html())

def report(yday):
    predict_file = 'd:\\stock_data\\predict\\data.predict'
    orign_label_data = "d:\\stock_data\\predict\\orign_label_data.txt"
    
    y=[]
    y_hat=[]
    for ln in open(orign_label_data):
        (stock_name,yday,real_label) = ln[:-1].split(' ')
        real_label  = float(real_label)
        y.append([stock_name,yday,real_label])
    for ln in open(predict_file):
        predict_label = ln[:-1].split(' ')[0]
        y_hat.append(float(predict_label))        
        
    
    assert(len(y)==len(y_hat))
    for i in range(len(y)):
        y[i].append(y_hat[i])
    generator_html(yday,y)
    
def generator_html_index(yday_list):
    def render_html():
        t = """<html lang="en-US" style="height: 100%%;">
    <head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"></head> <body>%s</body></html>"""
        link = ['<a href="%s.html">%s</a><br />'%(yday,yday)for yday in yday_list]
        return t%''.join(link)
    html_file  ='d:\\stock_data\\report\\index.html'
    open(html_file,'w').write(render_html())    
    
if __name__ == "__main__":
    y_day = datetime.date(2014,10,10)    
    #train_model(y_day)    
    oneday = datetime.timedelta(days=1)
    y_day_list=[]
    
    tday = set(hs300_last_trade_day(count = 30))
    for i in range(15):
        y_day +=oneday
        y_day_fmt = y_day.strftime(DT_FMT_SHORT)
        if not y_day_fmt in tday:
            continue
        y_day_list.append(y_day_fmt)
        predict(y_day)
        report(y_day_fmt)
    
    generator_html_index(y_day_list)
