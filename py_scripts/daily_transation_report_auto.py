
# coding: utf-8

# In[223]:


import pandas as pd
import os
from datetime import datetime, date, timedelta


# In[ ]:


"""
1. 在hive数据库中插表：将交易商户数、新增商户数、二维码交易笔数、二维码商户数、控件交易笔数、控件商户数、外部控件交易笔数、外部控件商户数插入
upw_hive.tmj_daily_trans_report_2表；
2. 将用户GPS+手机号归属地插入upw_hive.tmj_daily_frequent_location_by_user表；
3. 在zeppelin上定时执行所有所需CSV，并下载至raw_data文件夹中，如遇定时执行不成功或数据库缺数时手动调整，确保进入raw_data中的csv是准确的；
4. 执行脚本自动生成日报。

"""


# In[166]:


file_path ="C:\\Users\\tuomengjiao\\Desktop\\daily_tranaction_report\\data\\raw_data\\"
fileList = os.listdir(file_path)


# In[167]:


fileList


# In[168]:


dfs = {}
for i in range(len(fileList)):
    df = pd.read_csv(file_path + fileList[i])
    dfs[fileList[i][:-27]] = df


# In[169]:


for i in dfs:
    print(i)


# In[180]:


# 总体交易情况
"""
总体交易情况：2020年1月19日，云闪付APP总体交易商户40.67万，环比增长-0.86%，同比增长53.78%。当日新增交易商户106家，环比增长19.81%，
同比增长18.69%，新增商户主要集中在辽宁、重庆、广西等地区。

二维码交易商户40.05万，占总交易商户的98.49%，环比下降-0.88%；手机支付控件交易商户4868家，占总交易商户的1.16%，环比下降2.16%，手机外部支付
控件交易商户3929家，环比下降-0.05%。
"""

# 可修改的变量
# 1 日期
#current_date = datetime.now().strftime("%Y-%m-%d").split("-")
#current_date = current_date[0] + "年" + current_date[1] + "月" + current_date[2] + "日"

# 总体交易商户
df_overview=dfs['raw_overview']
df_overview


# In[243]:


#当前日期
today = (date.today() + timedelta(days = -1)).strftime("%Y-%m-%d").split("-")
current_date = today[0] + "年" + today[1] + "月" + today[2] + "日"
#总体交易商户
all_mchnt=df_overview['cnt_today'][df_overview['index']=='all_mchnt_cnt'].values[0]
all_mchnt_by_yesterday=df_overview['ratio_by_yesterday'][df_overview['index']=='all_mchnt_cnt'].values[0]
all_mchnt_by_last_year=df_overview['ration_by_last_year'][df_overview['index']=='all_mchnt_cnt'].values[0]
#新增交易商户
new_mchnt=df_overview['cnt_today'][df_overview['index']=='new_mchnt_cnt'].values[0]
new_mchnt_by_yesterday=df_overview['ratio_by_yesterday'][df_overview['index']=='new_mchnt_cnt'].values[0]
new_mchnt_by_last_year=df_overview['ration_by_last_year'][df_overview['index']=='new_mchnt_cnt'].values[0]
#二维码交易商户
qr_mchnt=df_overview['cnt_today'][df_overview['index']=='qr_code_mchnt_cnt'].values[0]
qr_mchnt_by_yesterday=df_overview['ratio_by_yesterday'][df_overview['index']=='qr_code_mchnt_cnt'].values[0]
qr_mchnt_by_last_year=df_overview['ration_by_last_year'][df_overview['index']=='qr_code_mchnt_cnt'].values[0]
#手机控件商户
control_mchnt=df_overview['cnt_today'][df_overview['index']=='control_mchnt'].values[0]
control_mchnt_by_yesterday=df_overview['ratio_by_yesterday'][df_overview['index']=='control_mchnt'].values[0]
control_mchnt_by_last_year=df_overview['ration_by_last_year'][df_overview['index']=='control_mchnt'].values[0]
#手机外部支付控件商户
control_out_mchnt=df_overview['cnt_today'][df_overview['index']=='control_out_mchnt'].values[0]
control_out_mchnt_by_yesterday=df_overview['ratio_by_yesterday'][df_overview['index']=='control_out_mchnt'].values[0]
control_out_mchnt_by_last_year=df_overview['ration_by_last_year'][df_overview['index']=='control_out_mchnt'].values[0]
#新增商户地区
new_mchnt_area="辽宁、重庆、广西"


# In[241]:


target_text1="总体交易情况：{},云闪付APP总体交易商户{}万，环比增长{}%，同比增长{}%。当日新增交易商户{}家，环比增长{}%，同比增长{}%，新增商户主要集中在{}等地区。".format(current_date, 
        round(all_mchnt/10000,2),
        round(all_mchnt_by_yesterday*100,2),
        round(all_mchnt_by_last_year*100,2),
        new_mchnt,
        round(new_mchnt_by_yesterday*100,2),
        round(new_mchnt_by_last_year*100,2),
        new_mchnt_area
                                                                                                
       )

target_text1


# In[244]:


target_text2="二维码交易商户{}万，占总交易商户的{}%，环比增长{}%；手机支付控件交易商户{}家，占总交易商户的{}%，环比增长{}%，手机外部支付控件交易商户{}家，环比增长{}%。".format(
        round(qr_mchnt/10000,2),
        round(qr_mchnt/all_mchnt*100,2),
        round(qr_mchnt_by_yesterday*100,2),
        control_mchnt,
        round(control_mchnt/all_mchnt*100,2),
        round(control_mchnt_by_yesterday*100,2),
        control_out_mchnt,
        round(control_out_mchnt_by_yesterday*100,2)
                                                                                                
       )

target_text2


# In[150]:


''# 支付类交易情况
"""
当日，云闪付APP发生支付类交易1133.76万笔，其中被扫、乘车码、远程转账、信用卡还款、一般主扫、快速收款码、小微主扫、手机外部支付控件、
无感支付、人到人转账交易笔数排名前十，占到交易总量的98.94%。
"""
df_transaction_cnt_by_day=dfs['raw_transaction_cnt_by_day']
df_transaction_cnt_by_day['ratio']=df_transaction_cnt_by_day['ratio'].apply(lambda x: format(float(x), '.2%')) 
df_transaction_cnt_by_day['proportion'] = df_transaction_cnt_by_day['cnt_today'] / df_transaction_cnt_by_day['cnt_today'].sum()
df_transaction_cnt_by_day['proportion'] = df_transaction_cnt_by_day['proportion'].apply(lambda x: format(float(x), '.2%')) 
df_transaction_cnt_by_day=df_transaction_cnt_by_day_print=df_transaction_cnt_by_day.loc[:,['index','cnt_today','proportion','ratio'] ]
df_transaction_cnt_by_day


# In[246]:


total=df_transaction_cnt_by_day['cnt_today'].sum()


# In[251]:


list_trans=df_transaction_cnt_by_day.head(10)['index']


# In[ ]:


total=df_transaction_cnt_by_day['cnt_today'].sum


target_text3="当日，云闪付APP发生支付类交易{}万笔，其中{}交易笔数排名前十，占到交易总量的{}%。".format(
        round(total/10000,2),
        round(qr_mchnt/all_mchnt*100,2),
        round(qr_mchnt_by_yesterday*100,2)
                                                                                                
       )
target_text3


# In[51]:


# 二维码交易情况 
"""
二维码交易情况：当日，二维码（含乘车码）交易笔数为647.79万笔，环比增长-11.31%，同比增长24.34%。其主要场景分布在公交地铁、零售、餐饮场景，
占比分别达61%、22.96%、6.17%。其中各城市TOP100商户交易笔数599.57万笔，占当日二维码总交易笔数的92.56%；交易商户3.01万，占二维码交易商户数
的7.45%。
"""
df_qr_transaction_cnt_by_scene=dfs['raw_qr_transaction_cnt_by_scene']
df_qr_transaction_cnt_by_scene['proportion'] = df_qr_transaction_cnt_by_scene['cnt_today'] / df_qr_transaction_cnt_by_scene['cnt_today'].sum()
df_qr_transaction_cnt_by_scene['proportion'] = df_qr_transaction_cnt_by_scene['proportion'].apply(lambda x: format(float(x), '.2%'))
df_qr_transaction_cnt_by_scene['ratio'] = df_qr_transaction_cnt_by_scene['ratio'].apply(lambda x: format(float(x), '.2%'))


# In[161]:


df_qr_transaction_cnt_by_scene_top100_in_city=dfs['raw_qr_transaction_cnt_by_scene_top100_in_city']
df_scece_new=pd.merge(df_qr_transaction_cnt_by_scene,df_qr_transaction_cnt_by_scene_top100_in_city,on='scene')
df_scece_new['proportion_xy'] = df_scece_new['cnt_today_y'] / df_scece_new['cnt_today_x']
df_scece_new['proportion_xy'] = df_scece_new['proportion_xy'].apply(lambda x: format(float(x), '.2%'))
df_scece_new['ratio_y'] = df_scece_new['ratio_y'].apply(lambda x: format(float(x), '.2%'))
df_scece_new=df_scece_new.head(11).loc[:,['scene','cnt_today_x','proportion','ratio_x','cnt_today_y',
                                                                      'ratio_y','proportion_xy'] ] 
df_scece_new


# In[68]:


#二维码TOP10分公司交易情况
df_qr_transaction_by_area_cd=dfs['raw_qr_transaction_by_area_cd']
df_qr_transaction_by_area_cd['proportion'] = df_qr_transaction_by_area_cd['cnt_today'] / df_qr_transaction_by_area_cd['cnt_today'].sum()
df_qr_transaction_by_area_cd['dis_proportion'] = df_qr_transaction_by_area_cd['dis_cnt_today'] / df_qr_transaction_by_area_cd['cnt_today']
df_qr_transaction_by_area_cd['proportion'] = df_qr_transaction_by_area_cd['proportion'].apply(lambda x: format(float(x), '.2%'))
df_qr_transaction_by_area_cd['ratio'] = df_qr_transaction_by_area_cd['ratio'].apply(lambda x: format(float(x), '.2%'))
df_qr_transaction_by_area_cd['dis_proportion'] = df_qr_transaction_by_area_cd['dis_proportion'].apply(lambda x: format(float(x), '.2%'))
df_qr_transaction_by_area_cd['dis_ratio'] = df_qr_transaction_by_area_cd['dis_ratio'].apply(lambda x: format(float(x), '.2%'))


# In[69]:


df_qr_transaction_by_area_cd_print=df_qr_transaction_by_area_cd.head(10).loc[:,['branch','cnt_today','proportion','ratio','dis_cnt_today',
                                                                      'dis_proportion','dis_ratio'] ] 


# In[70]:


df_qr_transaction_by_area_cd_print


# In[77]:


# 二维码TOP10商户交易情况
df_qr_transaction_top10_merchant=dfs['raw_qr_transaction_top10_merchant']
df_qr_transaction_top10_merchant['dis_proportion'] = df_qr_transaction_top10_merchant['discnt_today'] / df_qr_transaction_top10_merchant['cnt_today']
df_qr_transaction_top10_merchant['cnt_ratio'] = df_qr_transaction_top10_merchant['cnt_ratio'].apply(lambda x: format(float(x), '.2%'))
df_qr_transaction_top10_merchant['dis_proportion'] = df_qr_transaction_top10_merchant['dis_proportion'].apply(lambda x: format(float(x), '.2%'))


# In[79]:


df_qr_transaction_top10_merchant_print=df_qr_transaction_top10_merchant.loc[:,['mchnt_nm','type1','scene','cnt_today','cnt_ratio',
                                                                      'discnt_today','dis_proportion'] ] 


# In[80]:


df_qr_transaction_top10_merchant_print


# In[99]:


# 二维码交易金额分布
df_qr_transaction_by_amount_of_money=dfs['raw_qr_transaction_by_amount_of_money']
df_qr_transaction_by_amount_of_money['proportion'] = df_qr_transaction_by_amount_of_money['cnt_today'] / df_qr_transaction_by_amount_of_money['cnt_today'].sum()
df_qr_transaction_by_amount_of_money['avg_cnt'] = df_qr_transaction_by_amount_of_money['cnt_today'] / df_qr_transaction_by_amount_of_money['mchnt_today']
#df_qr_transaction_by_amount_of_money['ratio'] = df_qr_transaction_by_amount_of_money['ratio'].apply(lambda x: format(float(x), '.2%'))
df_qr_transaction_by_amount_of_money['proportion'] = df_qr_transaction_by_amount_of_money['proportion'].apply(lambda x: format(float(x), '.2%'))
df_qr_transaction_by_amount_of_money_print=df_qr_transaction_by_amount_of_money.loc[:,['金额','cnt_today','proportion','ratio','mchnt_today',
                                                                      'avg_cnt'] ] 
df_qr_transaction_by_amount_of_money_print


# In[163]:


#手机支付控件TOP100商户交易情况
df_control_by_merchant_details=dfs['raw_control_by_merchant_details']
#df_qr_transaction_by_amount_of_money['proportion'] = df_qr_transaction_by_amount_of_money['cnt_today'] / df_qr_transaction_by_amount_of_money['cnt_today'].sum()
#df_qr_transaction_by_amount_of_money['avg_cnt'] = df_qr_transaction_by_amount_of_money['cnt_today'] / df_qr_transaction_by_amount_of_money['mchnt_today']
#df_qr_transaction_by_amount_of_money['ratio'] = df_qr_transaction_by_amount_of_money['ratio'].apply(lambda x: format(float(x), '.2%'))
#df_qr_transaction_by_amount_of_money['proportion'] = df_qr_transaction_by_amount_of_money['proportion'].apply(lambda x: format(float(x), '.2%'))
#df_qr_transaction_by_amount_of_money


# In[164]:


df_control_by_merchant_details.head()


# In[ ]:


# 手机外部支付控件TOP100商户


# In[126]:


# 外部控件商户侧归属地
df_control_out_by_area_cd=dfs['raw_control_out_by_area_cd']
df_control_out_by_area_cd['交易笔数占比'] = df_control_out_by_area_cd['交易笔数'] / df_control_out_by_area_cd['交易笔数'].sum()
#df_control_out_by_area_cd['交易笔数环比'] = df_control_out_by_area_cd['交易笔数环比'].apply(lambda x: format(float(x), '.2%'))
#df_control_out_by_area_cd['优惠笔数环比'] = df_control_out_by_area_cd['优惠笔数环比'].apply(lambda x: format(float(x), '.2%'))
df_control_out_by_area_cd['交易笔数占比'] = df_control_out_by_area_cd['交易笔数占比'].apply(lambda x: format(float(x), '.2%'))
df_control_out_by_area_cd['优惠笔数占比'] = df_control_out_by_area_cd['优惠交易笔数'] / df_control_out_by_area_cd['交易笔数']
df_control_out_by_area_cd['优惠笔数占比'] = df_control_out_by_area_cd['优惠笔数占比'].apply(lambda x: format(float(x), '.2%'))
df_control_out_by_area_cd_print=df_control_out_by_area_cd.head(10).loc[:,['pro','交易笔数','交易笔数占比','交易笔数环比','优惠交易笔数',
                                                                    '优惠笔数占比','优惠笔数环比'] ] 
df_control_out_by_area_cd_print


# In[141]:


# 外部控件用户侧归属地
df_control_out_by_user_gps=dfs['raw_control_out_by_user_gps'].sort_values(by="交易笔数" , ascending=False)
df_control_out_by_user_gps['交易笔数占比'] = df_control_out_by_user_gps['交易笔数'] / df_control_out_by_area_cd['交易笔数'].sum()
df_control_out_by_user_gps['交易笔数环比'] = df_control_out_by_user_gps['交易笔数环比'].apply(lambda x: format(float(x), '.2%'))
df_control_out_by_user_gps['优惠笔数环比'] = df_control_out_by_user_gps['优惠笔数环比'].apply(lambda x: format(float(x), '.2%'))
df_control_out_by_user_gps['交易笔数占比'] = df_control_out_by_user_gps['交易笔数占比'].apply(lambda x: format(float(x), '.2%'))
df_control_out_by_user_gps['优惠笔数占比'] = df_control_out_by_user_gps['优惠交易笔数'] / df_control_out_by_area_cd['交易笔数']
df_control_out_by_user_gps['优惠笔数占比'] = df_control_out_by_user_gps['优惠笔数占比'].apply(lambda x: format(float(x), '.2%'))
df_control_out_by_user_gps=df_control_out_by_user_gps.head(10).loc[:,['branch','交易笔数','交易笔数占比','交易笔数环比','优惠交易笔数',
                                                                '优惠笔数占比','优惠笔数环比'] ] 
df_control_out_by_user_gps


# In[208]:


# 外部控件交易金额分布
control_out_mchnt=df_overview['cnt_today'][df_overview['index']=='control_out_mchnt'].values[0]


# In[211]:


df_control_out_transaction_by_amount_of_money=dfs['raw_control_out_transaction_by_amount_of_money']
df_control_out_transaction_by_amount_of_money['交易笔数占比'] = df_control_out_transaction_by_amount_of_money['交易笔数'] / df_control_out_transaction_by_amount_of_money['交易笔数'].sum()
df_control_out_transaction_by_amount_of_money['商户数占比'] = df_control_out_transaction_by_amount_of_money['商户数'] /control_out_mchnt
df_control_out_transaction_by_amount_of_money['商户日均交易笔数'] = df_control_out_transaction_by_amount_of_money['交易笔数'] / df_control_out_transaction_by_amount_of_money['商户数']
df_control_out_transaction_by_amount_of_money['交易笔数占比'] = df_control_out_transaction_by_amount_of_money['交易笔数占比'].apply(lambda x: format(float(x), '.2%'))
df_control_out_transaction_by_amount_of_money['商户数占比'] = df_control_out_transaction_by_amount_of_money['商户数占比'].apply(lambda x: format(float(x), '.2%'))
df_control_out_transaction_by_amount_of_money=df_control_out_transaction_by_amount_of_money.loc[:,['金额区间','交易笔数','交易笔数占比','商户数','商户数占比','商户日均交易笔数']]
df_control_out_transaction_by_amount_of_money

