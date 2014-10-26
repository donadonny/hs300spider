#coding:utf-8
import sys
sys.path.append("../")
from util import *
import datetime,random
import x_features, y_label

'''
x_days : trade days to extra features 
y_day : trade day to extra label (numberic target, stock price up or down)
'''
def generate_xy_days(y_day,x_range=3):
    last_trade_days = hs300_last_trade_day(count=90)
    last_trade_days = set(last_trade_days)    
    oneday = datetime.timedelta(days=1)
    x_days = []
    y_day_fmt = y_day.strftime(DT_FMT_SHORT)
    if not y_day_fmt in last_trade_days:
        print '--> %s is not trade_day, ignore and continue.'%y_day_fmt
        return (None,None)
    
    x_day = y_day
    top = x_range+10
    counter = 0
    while len(x_days) < x_range:
        counter += 1
        if counter >= top:
            print 'CANNOT got enough trade days. Please check mongodb trade day list. '
            return (None,None)
        x_day -= oneday
        x_day_fmt = x_day.strftime(DT_FMT_SHORT)
        if not x_day_fmt in last_trade_days:
            pass
        else:
            x_days.append(x_day_fmt)
            print '-- trade day : %s'%x_day_fmt
    return (x_days,y_day_fmt)

def generate_single_data(fd,stock_name,x_days,yday,labelFD):
    feature = x_features.generate_feature(stock_name,x_days)
    ylabel = y_label.generate_ylabel(stock_name,yday)
    if not feature or not ylabel:return
    if ylabel>10 or ylabel<-10:return
        
    fd.write('%f'%ylabel)
    for i in range(len(feature)):
        s = ' %d:%s'%(i,str(feature[i]))
        fd.write(s)
    fd.write('\n')
    fd.flush()
    
    if labelFD:
        labelFD.write('%s %s %f\n'%(stock_name,yday,ylabel))
        labelFD.flush()

    return ylabel


#生成y_day（含）往前date_range个自然日的训练数据，可选额外输出数据标签
def generate_data(fd,y_day,date_range=6,labelFD=None):
    hs_300list = hs300_list()
    oneday = datetime.timedelta(days=1)
    for i in range(date_range):
        (x_days,y_day_fmt)= generate_xy_days(y_day, x_range=3)
        y_day -= oneday
        if not x_days or not y_day_fmt:
            continue
        for stock_name in hs_300list:
            generate_single_data(fd, stock_name, x_days, y_day_fmt,labelFD)

if __name__ == "__main__":
    y_day = datetime.date(2014,10,19)   
    fd = open("d:\\stock_data\\data.txt",'w')
    generate_data(fd,y_day,date_range=90)
    pass
