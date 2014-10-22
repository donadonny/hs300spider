#coding : utf-8
import sys
import subprocess,math
sys.path.append("../")
from util import *
import datetime,random
import feature_generation_entry as g
import threading, time 


def split_data_2_train_test(data_path,train_data_path,test_data_path):
    fd_data = open(data_path)
    fd_train = open(train_data_path,'w')
    fd_test = open(test_data_path,'w')
    for ln in fd_data:
        rand = random.randint(0,9)
        if rand == 0:
            fd_test.write(ln)
        else:
            fd_train.write(ln)
    fd_test.flush()
    fd_train.flush()

cmd_template = "d:\\stock_data\\libFM.exe -task r -train %s -test %s -dim '1,20,40' -iter 100 -method als -regular '0,0.1,1' -init_stdev 0.1 -out %s"
def train(train_data_path,test_data_path,predict_out_path):
    cmd = cmd_template%(train_data_path,test_data_path,predict_out_path)
    returnCode = subprocess.call(cmd)  
    print 'returncode:', returnCode  


def stat(predict_out_path,test_data_path):
    fd_test = open(predict_out_path)
    fd_y = open(test_data_path)
    
    y=[]
    y_hat=[]
    
    for ln in fd_y:
        y.append(float(ln[:ln.find(' ')]))
    
    for ln in fd_test:
        y_hat.append(float(ln[:-1]))
        
    #print len(y),len(y_hat)
    
    def bool2int(b):
        if b:return 1
        else:return -1
        
    def loss(y_hat,y):
        return bool2int((y_hat*y)>0) * abs(y)
    

        
    lossA= [loss(1,y[i]) for i in range(len(y))]
    lossB = [loss(y_hat[i],y[i]) for i in range(len(y))]
    lossC= [loss(random.randint(-10,10),y[i]) for i in range(len(y))]
    cost = len(y)*100
    print '--------------------------------'
    for i in range(len(y)):
        #print y[i],y_hat[i]
        pass
    
    print 'Predict stock count:',len(y)
    return sum(lossA),sum(lossB),sum(lossC),cost

lock = threading.Lock() 

    
r = []
def thread_entry_wrapper(thread_id):
    def thread_entry():  
        print thread_id,'start waiting:', time.strftime('%H:%M:%S')  
        train_data_path = tmp_train_data_path%thread_id
        test_data_path = tmp_test_data_path%thread_id
        predict_out_path = tmp_predict_out_path%thread_id
        split_data_2_train_test(data_path,train_data_path,test_data_path)
        train(train_data_path,test_data_path,predict_out_path)
        stat_res = stat(predict_out_path,test_data_path)
        lock.acquire()  
        r.append(stat_res)
        lock.release()
        print thread_id,'stop waiting', time.strftime('%H:%M:%S')
    return thread_entry
    


tmp_train_data_path = 'd:\\stock_data\\tmp\\train_data_%d.txt'
tmp_test_data_path = 'd:\\stock_data\\tmp\\test_data_%d.txt'
tmp_predict_out_path='d:\\stock_data\\tmp\\predict_out_%d.txt'
data_path = 'd:\\stock_data\\stock_data.txt'

    
def one_pass():
    N=8
    threads = []
    #g_data()
    for i in range(N):
        thread = threading.Thread(target = thread_entry_wrapper(i))
        thread.start()
        threads.append(thread)
    for i in range(N):
        threads[i].join()
    
    print '------------------------------------------------'
    (a,b,c,cost)=(0,0,0,0)
    
    for i in range(N):
        a += r[i][0]
        b += r[i][1]
        c += r[i][2]
        cost += r[i][3]
        print r[i][0],r[i][1],r[i][2],r[i][3]
        
    print cost,len(r)
    print a*100*200/cost,b*100*200/cost,c*100*200/cost
        
if __name__ == "__main__":
    one_pass()
