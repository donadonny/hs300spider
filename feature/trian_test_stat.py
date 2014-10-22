#coding : utf-8
import sys
import subprocess,math
sys.path.append("../")
from util import *
import datetime,random
import feature_generation_entry as g


def g_data():
    y_day = datetime.date(2014,10,19)   
    fd_train = open("d:\\stock_train.txt",'w')
    fd_test = open("d:\\stock_test.txt",'w')
    fd_y = open("d:\\stock_label_y.txt",'w')
    g.generate_data(fd_train,fd_test,fd_y,y_day)



def train():
    cmd = "d:\\libFM.exe -task r -train d:\\stock_train.txt -test d:\\stock_test.txt -dim '1,1,8' -iter 1000 -method als -learn_rate 0.5 -regular '0,0,20' -init_stdev 0.1 -out d:\\stock.model.txt"
    returnCode = subprocess.call(cmd)  
    print 'returncode:', returnCode  


def stat():
    fd_test = open("d:\\stock.model.txt")
    fd_y = open("d:\\stock_label_y.txt")
    
    y=[]
    y_hat=[]
    
    for ln in fd_y:
        y.append(float(ln[:-1]))
    
    for ln in fd_test:
        y_hat.append(float(ln[:-1]))
        
    print len(y),len(y_hat)
    
    def bool2int(b):
        if b:return 1
        else:return -1
        
    def loss(y_hat,y):
        return bool2int(y_hat*y>0) * abs(y)
    
    lossA= [loss(1,y[i]) for i in range(len(y))]
    lossB = [loss(y_hat[i],y[i]) for i in range(len(y))]
    
    return sum(lossA),sum(lossB)
    
if __name__ == "__main__":
    r = []
    for i in range(10):
        g_data()
        train()
        r.append(stat())
    for i in range(10):
        print r[i]
