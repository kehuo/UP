
# coding: utf-8

# In[1]:


import pandas as pd
import os


# In[ ]:


"""
1. 在hive数据库中插表：将交易商户数、新增商户数、二维码交易笔数、二维码商户数、控件交易笔数、控件商户数、外部控件交易笔数、外部控件商户数插入
upw_hive.tmj_daily_trans_report_2表；
2. 将用户GPS+手机号归属地插入upw_hive.tmj_daily_frequent_location_by_user表；
3. 在zeppelin上定时执行所有所需CSV，并下载至raw_data文件夹中，如遇定时执行不成功或数据库缺数时手动调整，确保进入raw_data中的csv是准确的；
4. 执行脚本自动生成日报。

"""


# In[13]:


file_path ="C:\\Users\\tuomengjiao\\Desktop\\daily_tranaction_report\\data\\raw_data\\"
fileList = os.listdir(file_path)


# In[14]:


fileList


# In[15]:


fileList[0]


# In[16]:


fileList[6][:-27]


# In[18]:


dfs = {}
for i in range(len(fileList)):
    df = pd.read_csv(file_path + fileList[i])
    dfs[fileList[i][:-27]] = df


# In[ ]:


df_pv_l=dfs[fileList[0]]
df_pv_2=dfs[fileList[1]]
df_pv_3=dfs[fileList[2]]
df_trans=dfs[fileList[3]]
df_remain=dfs[fileList[4]]


# In[24]:


for i in dfs:
    print(i)


# In[27]:





# In[ ]:


# 总体交易情况
"""
总体交易情况：2020年1月19日，云闪付APP总体交易商户40.67万，环比增长-0.86%，同比增长53.78%。当日新增交易商户106家，环比增长19.81%，
同比增长18.69%，新增商户主要集中在辽宁、重庆、广西等地区。

二维码交易商户40.05万，占总交易商户的98.49%，环比下降-0.88%；手机支付控件交易商户4868家，占总交易商户的1.16%，环比下降2.16%，手机外部支付
控件交易商户3929家，环比下降-0.05%。
"""

# 可修改的变量
# 1 日期
current_date = datetime.now().strftime("%Y-%m-%d").split("-")
current_date = current_date[0] + "年" + current_date[1] + "月" + current_date[2] + "日"

# 总体交易商户


# In[28]:


# 支付类交易情况
"""
当日，云闪付APP发生支付类交易1133.76万笔，其中被扫、乘车码、远程转账、信用卡还款、一般主扫、快速收款码、小微主扫、手机外部支付控件、
无感支付、人到人转账交易笔数排名前十，占到交易总量的98.94%。
"""
df_transaction_cnt_by_day=dfs['raw_transaction_cnt_by_day']
df_transaction_cnt_by_day


# In[34]:


df_transaction_cnt_by_day['ratio']=df_transaction_cnt_by_day['ratio'].apply(lambda x: format(float(x), '.2%')) 


# In[35]:


df_transaction_cnt_by_day


# In[39]:


df_transaction_cnt_by_day['proportion'] = df_transaction_cnt_by_day['cnt_today'] / df_transaction_cnt_by_day['cnt_today'].sum()
df_transaction_cnt_by_day['proportion'] = df_transaction_cnt_by_day['proportion'].apply(lambda x: format(float(x), '.2%')) 


# In[40]:


df_transaction_cnt_by_day


# In[44]:


df_transaction_cnt_by_day_print=df_transaction_cnt_by_day.loc[:,['index','cnt_today','proportion','ratio'] ] 


# In[45]:


df_transaction_cnt_by_day_print


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


# In[52]:


df_qr_transaction_cnt_by_scene


# In[ ]:



df_qr_transaction_cnt_by_scene['proportion'] = df_qr_transaction_cnt_by_scene['proportion'].apply(lambda x: format(float(x), '.2%'))
df_qr_transaction_cnt_by_scene['ratio'] = df_qr_transaction_cnt_by_scene['ratio'].apply(lambda x: format(float(x), '.2%'))


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


# In[78]:


df_qr_transaction_top10_merchant


# In[79]:


df_qr_transaction_top10_merchant_print=df_qr_transaction_top10_merchant.loc[:,['mchnt_nm','type1','scene','cnt_today','cnt_ratio',
                                                                      'discnt_today','dis_proportion'] ] 


# In[80]:


df_qr_transaction_top10_merchant_print


# In[98]:


df_qr_transaction_by_amount_of_money


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


# In[ ]:


#手机支付控件TOP100商户交易情况
df_qr_transaction_by_amount_of_money=dfs['raw_qr_transaction_by_amount_of_money']
df_qr_transaction_by_amount_of_money['proportion'] = df_qr_transaction_by_amount_of_money['cnt_today'] / df_qr_transaction_by_amount_of_money['cnt_today'].sum()
df_qr_transaction_by_amount_of_money['avg_cnt'] = df_qr_transaction_by_amount_of_money['cnt_today'] / df_qr_transaction_by_amount_of_money['mchnt_today']
df_qr_transaction_by_amount_of_money['ratio'] = df_qr_transaction_by_amount_of_money['ratio'].apply(lambda x: format(float(x), '.2%'))
df_qr_transaction_by_amount_of_money['proportion'] = df_qr_transaction_by_amount_of_money['proportion'].apply(lambda x: format(float(x), '.2%'))
df_qr_transaction_by_amount_of_money


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


# In[ ]:


df_control_out_by_area_cd=dfs['raw_control_out_by_area_cd']
df_qr_transaction_by_amount_of_money['proportion'] = df_qr_transaction_by_amount_of_money['cnt_today'] / df_qr_transaction_by_amount_of_money['cnt_today'].sum()
df_qr_transaction_by_amount_of_money['avg_cnt'] = df_qr_transaction_by_amount_of_money['cnt_today'] / df_qr_transaction_by_amount_of_money['mchnt_today']
df_qr_transaction_by_amount_of_money['ratio'] = df_qr_transaction_by_amount_of_money['ratio'].apply(lambda x: format(float(x), '.2%'))
df_qr_transaction_by_amount_of_money['proportion'] = df_qr_transaction_by_amount_of_money['proportion'].apply(lambda x: format(float(x), '.2%'))
df_qr_transaction_by_amount_of_money

