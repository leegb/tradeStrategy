# -*- coding:utf-8 -*-
from pdsql import *
from fileoperation import *
from tradeStrategy import *

if __name__ == '__main__': 
    data={}
    stronge_ma_3_list=[]
    result_column=['code','o_ma5_rate','ct_o_ma5_num','o_ma10_rate','ct_o_ma10_num','reversal']
    result_df=pd.DataFrame(data,columns=result_column)
    codes=get_all_code(RAW_HIST_DIR)
    for code in codes:
        code_data={}
        stock_hist_obj=Stockhistory(code,'D')
        over_ma5_rate,continue_over_ma5_num=stock_hist_obj.get_recent_over_ma(ma_type='ma5',ma_offset=0.002,recent_count=20)
        over_ma10_rate,continue_over_ma10_num=stock_hist_obj.get_recent_over_ma(ma_type='ma10',ma_offset=0.002,recent_count=40)
        is_drop_up,actual_turnover_rate=stock_hist_obj.is_drop_then_up(great_dropdown=-3.0,turnover_rate=0.75,turnover_num=1)
        if True:#over_ma_rate>0.75 and continue_over_ma_num:
            code_data={'code':code,'o_ma5_rate':over_ma5_rate,'ct_o_ma5_num':continue_over_ma5_num,'o_ma10_rate':over_ma10_rate,'ct_o_ma10_num':continue_over_ma10_num,'reversal':actual_turnover_rate}
            code_df=pd.DataFrame(code_data,index=['code'],columns=result_column)
            result_df=result_df.append(code_df,ignore_index=True)
            #print('result_df=',result_df)
    #result_df=result_df.sort_index(axis=0, by='ct_o_num', ascending=False)
    result_df=result_df.sort_values(axis=0, by='o_ma5_rate', ascending=False)
    result_df.set_index('code')
    update_to_db=True
    stock_sql_obj=StockSQL()
    if update_to_db:
        stock_sql_obj.insert_table(result_df, 'madata')
    print(result_df)