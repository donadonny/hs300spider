#coding:utf-8
import sys,subprocess
sys.path.append("../")
sys.path.append("")
from util import *
import datetime,random

#TTP: Train, Test, Predicting


#---------------------------------------------------------------------------
#split_data_2_train_test (90% vs 10%)
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
    fd_test.close()
    fd_train.close()
    pass
#---------------------------------------------------------------------------

def normalize_data(input,output,rules,restore=False):
    cmd_template = "c:\\tools\\svm-scale.exe -%s %s %s"
    cmd = cmd_template%('r'  if restore else 's', rules,input)
    print 'CMD = %s'%cmd
    outFD= open(output,'w')
    returnCode = subprocess.call(cmd,stdout=outFD)
    outFD.flush()
    outFD.close()
    print 'returncode:', returnCode 

def gbdt_train(data,model_file,predict_file,feature_num):
    cmd_template = "c:\\tools\\gbdt_train.exe %s %s %s %s %d"
    train_data = data+'.train'
    test_data = data+'.test'
    split_data_2_train_test(data, train_data, test_data)
    
    cmd = cmd_template%(train_data,test_data,model_file,predict_file,feature_num)
    print 'CMD = %s'%cmd
    returnCode = subprocess.call(cmd)  
    print 'returncode:', returnCode  

#---------------------------------------------------------------------------
def gdbt_predict(model_file,feature_num,predict_input,predict_output):
    cmd_template = "c:\\tools\\gbdt_predict.exe %s %d %s %s"
    cmd = cmd_template%(model_file,feature_num,predict_input,predict_output)
    print 'CMD = %s'%cmd
    returnCode = subprocess.call(cmd)  
    print 'returncode:', returnCode     

#---------------------------------------------------------------------------
if __name__ == "__main__":
    data= "d:\\stock_data\\stock_data.txt"
    model= "d:\\stock_data\\model.txt"
    predict= "d:\\stock_data\\predict.txt"
    feature_num = 74
    #gbdt_train(data,model,predict,feature_num)
    #gdbt_predict(model, feature_num, "d:\\stock_data\\stock_data.txt.test", predict)
    normalize_data("d:\\stock_data\\data.txt", data, "d:\\stock_data\\norm_rules.txt",restore=True)
#---------------------------------------------------------------------------
