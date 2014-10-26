#coding : utf-8
import sys
sys.path.append("../")
from util import *
import datetime,math

mongodb_coll_summary = DB.hs300_day_summary
mongodb_coll_details = DB.hs300_day_detail
mongodb_coll_details_stat = DB.hs300_day_detail_stat

class detail_accumulator:
    def __init__(self):
        self.feature={
            'ACC_COUNT':0,         #交易次数
            'ACC_AVG_PRICE':0,     #平均价格
            'ACC_PD_COUNT_1':0,    #price_delta >0 ,percent
            'ACC_PD_COUNT_2':0,    #price_delta =0 ,percent
            'ACC_PD_COUNT_3':0,    #price_delta <0 ,percent
            'ACC_AVG_VOL':0,
            'ACC_VAR_VOL':0,
            'ACC_MAX_VOL':0,
            'ACC_MIN_VOL':0,
            'ACC_AVG_AMT':0,
            'ACC_VAR_AMT':0,
            'ACC_MAX_AMT':0,
            'ACC_MIN_AMT':0
        }
        
        self.var_vol_list=[]
        self.var_amt_list=[]
        
    def is_not_valid_info(self,trade_info):
        p = trade_info["price_delta"]/trade_info["price"]
        if abs(p) > 0.15:return True
        return False
    
    def iter(self,trade_info):
        if self.is_not_valid_info(trade_info):return
        
        self.feature['ACC_COUNT'] += 1
        self.feature['ACC_AVG_PRICE'] += trade_info['price']
        self.feature['ACC_PD_COUNT_1'] += 1 if trade_info['price_delta'] >0 else 0
        self.feature['ACC_PD_COUNT_2'] += 1 if trade_info['price_delta'] ==0 else 0
        self.feature['ACC_PD_COUNT_3'] += 1 if trade_info['price_delta'] <0 else 0
        
        self.feature['ACC_AVG_VOL'] += trade_info['volume']
        self.feature['ACC_AVG_AMT'] += trade_info['amount']
        self.feature['ACC_MAX_VOL'] = max([self.feature['ACC_MAX_VOL'],trade_info['volume']])
        self.feature['ACC_MIN_VOL'] = min([self.feature['ACC_MAX_VOL'],trade_info['volume']])
        self.feature['ACC_MAX_AMT'] = max([self.feature['ACC_MAX_AMT'],trade_info['amount']])
        self.feature['ACC_MIN_AMT'] = min([self.feature['ACC_MIN_AMT'],trade_info['amount']])
        
        self.var_vol_list.append(trade_info['volume'])
        self.var_amt_list.append(trade_info['amount'])
        
    def final(self):
        count = self.feature['ACC_COUNT'] * 1.0
        if self.feature['ACC_COUNT'] <=0:
            return
        
        self.feature['ACC_AVG_PRICE'] /= count
        self.feature['ACC_PD_COUNT_1'] /= count
        self.feature['ACC_PD_COUNT_2'] /= count
        self.feature['ACC_PD_COUNT_3'] /= count
        self.feature['ACC_AVG_VOL'] /= count
        self.feature['ACC_AVG_AMT'] /= count
        
        for i in range(self.feature['ACC_COUNT']):
            pVOL = (self.var_vol_list[i] - self.feature['ACC_AVG_VOL'])
            pAMT = (self.var_amt_list[i] - self.feature['ACC_AVG_AMT'])
            pVOL *= pVOL
            pAMT *= pAMT
            self.feature['ACC_VAR_VOL'] += pVOL
            self.feature['ACC_VAR_AMT'] += pAMT
        self.feature['ACC_VAR_VOL'] = math.sqrt(self.feature['ACC_VAR_VOL'] / (count-1))
        self.feature['ACC_VAR_AMT'] = math.sqrt(self.feature['ACC_VAR_AMT'] / (count-1))
        pass

def query_detail(stock_name,date):
    query = {"stock_name":stock_name,'date':date}
    res = mongodb_coll_details.find(query)
    if not res:return None
    
    acc = detail_accumulator()
    for trade_info in res:
        acc.iter(trade_info)
    acc.final()
    
    data_object = acc.feature
    data_object["stock_name"] =  stock_name
    data_object["date"] =  date
    data_object['_update_time_'] = datetime.datetime.now().strftime(DT_FMT)
    update_condition = {"stock_name":data_object['stock_name'],
                            'date':data_object['date']}
    #update !
    #print data_object
    mongodb_update(mongodb_coll_details_stat, update_condition, data_object)
        

#THE ENTRY POINT OF THE WHOLE SPIDER
def detail_stat_entry():    
    hs_300list = hs300_list()
    last_trade_days = hs300_last_trade_day(count=90)
    print 'last_trade_days = ',last_trade_days
    
    trade_day_set = set(last_trade_days)
    D = datetime.date(2014,10,25)
    N = 15
    oneday = datetime.timedelta(days=1)
    for i in range(N):
        D -= oneday
        date = D.strftime(DT_FMT_SHORT)
        
        if not date in trade_day_set:
            print '-- DATE = ', date , " is not trade day, ignore."
            continue
        else:
            print '-- DATE = ', date
        
        for stock_name in hs_300list:        
            try:
                query_detail(stock_name,date)
            except Exception,err:
                print 'ERROR occured at date = ', date
                print 'ERR:', err
                print sys.exc_info()
                exit(-01)
    print '-----------ALL COMPLETE-----------'
    print 'LAST date:',date
    
if __name__ == "__main__":
    detail_stat_entry()