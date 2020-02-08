
# coding: utf-8

# In[65]:


import pandas as pd
import os
from datetime import timedelta,date


# In[66]:


file_path ="/Users/apple/Desktop/UP/daily_report/raw_data/"
fileList = os.listdir(file_path)
#print(fileList)
dfs = {}
for i in range(len(fileList)):
    if ".csv" in fileList[i]:
        df = pd.read_csv(file_path + fileList[i])
        dfs[fileList[i][:-4]] = df


# In[67]:


# 总体交易商户
df_overview=dfs['raw_overview']
df_overview

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
new_mchnt_area="辽宁、广西、福建"


# In[68]:


target_text1="{},云闪付APP总体交易商户{}万，环比增长{}%，同比增长{}%。当日新增交易商户{}家，环比增长{}%，同比增长{}%，新增商户主要集中在{}等地区。".format(current_date, 
        round(all_mchnt/10000,2),
        round(all_mchnt_by_yesterday*100,2),
        round(float(all_mchnt_by_yesterday)*100,2),
        new_mchnt,
        round(new_mchnt_by_yesterday*100,2),
        round(float(new_mchnt_by_last_year)*100,2),
        new_mchnt_area                                                                                           
       )


# In[69]:


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


# In[70]:


# 支付类交易情况
df_transaction_cnt_by_day=dfs['raw_transaction_cnt_by_day']
df_transaction_cnt_by_day['ratio']=df_transaction_cnt_by_day['ratio'].apply(lambda x: format(float(x), '.2%')) 
df_transaction_cnt_by_day['proportion'] = df_transaction_cnt_by_day['cnt_today'] / df_transaction_cnt_by_day['cnt_today'].sum()
df_transaction_cnt_by_day['proportion'] = df_transaction_cnt_by_day['proportion'].apply(lambda x: format(float(x), '.2%')) 
df_transaction_cnt_by_day=df_transaction_cnt_by_day.loc[:,['index','cnt_today','proportion','ratio'] ]


# In[71]:


list_trans=df_transaction_cnt_by_day.head(10)['index'].values.tolist()
a='、'
aa=a.join(list_trans)
total=df_transaction_cnt_by_day['cnt_today'].sum()
top10_total=df_transaction_cnt_by_day.head(10)['cnt_today'].sum()
target_text3="当日，云闪付APP发生支付类交易{}万笔，其中".format(round(total/10000,2))+aa+"交易笔数排名前十，占到交易总量的{}%。".format(round(top10_total/total*100,2))                                       


# In[72]:


# 二维码交易情况 
df_qr_transaction_cnt_by_scene=dfs['raw_qr_transaction_cnt_by_scene']
df_qr_transaction_cnt_by_scene['proportion'] = df_qr_transaction_cnt_by_scene['cnt_today'] / df_qr_transaction_cnt_by_scene['cnt_today'].sum()
df_qr_transaction_cnt_by_scene['proportion'] = df_qr_transaction_cnt_by_scene['proportion'].apply(lambda x: format(float(x), '.2%'))
df_qr_transaction_cnt_by_scene['ratio'] = df_qr_transaction_cnt_by_scene['ratio'].apply(lambda x: format(float(x), '.2%'))
df_qr_transaction_cnt_by_scene_top100_in_city=dfs['raw_qr_transaction_cnt_by_scene_top100_in_city']
df_scece_new=pd.merge(df_qr_transaction_cnt_by_scene,df_qr_transaction_cnt_by_scene_top100_in_city,on='scene')
df_scece_new['proportion_xy'] = df_scece_new['cnt_today_y'] / df_scece_new['cnt_today_x']
df_scece_new['proportion_xy'] = df_scece_new['proportion_xy'].apply(lambda x: format(float(x), '.2%'))
df_scece_new['ratio_y'] = df_scece_new['ratio_y'].apply(lambda x: format(float(x), '.2%'))
df_scece_new=df_scece_new.head(11).loc[:,['scene','cnt_today_x','proportion','ratio_x','cnt_today_y',
                                                                      'ratio_y','proportion_xy'] ] 


# In[73]:


#二维码交易笔数
qr_code_cnt=df_overview['cnt_today'][df_overview['index']=='qr_code_cnt'].values[0]
qr_code_cnt_by_yesterday=df_overview['ratio_by_yesterday'][df_overview['index']=='qr_code_cnt'].values[0]
qr_code_cnt_by_last_year=df_overview['ration_by_last_year'][df_overview['index']=='qr_code_cnt'].values[0]

list_scene=df_scece_new.head(3)['scene'].values.tolist()
b='、'
bb=b.join(list_scene)

list_cnt=df_scece_new.head(3)['proportion'].values.tolist()
list_cnt=[str(i) for i in list_cnt]
e='、'
ee=e.join(list_cnt)
top100_mchnt=30292
target_text4="当日，二维码（含乘车码）交易笔数为{}万笔，环比增长{}%，同比增长{}%。其主要场景分布在".format(
    round(qr_code_cnt/10000,2),
    round(qr_code_cnt_by_yesterday*100,2),
    round(float(qr_code_cnt_by_last_year)*100,2))+bb+"场景，占比分别达"+ee+"。其中各城市TOP100商户交易笔数{}万笔，占当日二维码总交易笔数的{}%；交易商户{}万，占二维码交易商户数的{}%。".format(
    round(df_scece_new['cnt_today_y'].sum()/10000,2),
    round(df_scece_new['cnt_today_y'].sum()/qr_code_cnt*100,2),
    round(top100_mchnt/10000,2),
    round(top100_mchnt/qr_mchnt*100,2),
)


# In[74]:


#二维码TOP10分公司交易情况
df_qr_transaction_by_area_cd=dfs['raw_qr_transaction_by_area_cd']
df_qr_transaction_by_area_cd['proportion'] = df_qr_transaction_by_area_cd['cnt_today'] / df_qr_transaction_by_area_cd['cnt_today'].sum()
df_qr_transaction_by_area_cd['dis_proportion'] = df_qr_transaction_by_area_cd['dis_cnt_today'] / df_qr_transaction_by_area_cd['cnt_today']
df_qr_transaction_by_area_cd['proportion'] = df_qr_transaction_by_area_cd['proportion'].apply(lambda x: format(float(x), '.2%'))
df_qr_transaction_by_area_cd['ratio'] = df_qr_transaction_by_area_cd['ratio'].apply(lambda x: format(float(x), '.2%'))
df_qr_transaction_by_area_cd['dis_proportion'] = df_qr_transaction_by_area_cd['dis_proportion'].apply(lambda x: format(float(x), '.2%'))
df_qr_transaction_by_area_cd['dis_ratio'] = df_qr_transaction_by_area_cd['dis_ratio'].apply(lambda x: format(float(x), '.2%'))
df_qr_transaction_by_area_cd=df_qr_transaction_by_area_cd.head(10).loc[:,['branch','cnt_today','proportion','ratio','dis_cnt_today',
                                                                      'dis_proportion','dis_ratio'] ] 


# In[75]:


list_area=df_qr_transaction_by_area_cd['branch'].values.tolist()
b='、'
area=b.join(list_area)
target_text5 ="1、当日，"+area+"地区交易量排名前十。"


# In[76]:


# 二维码TOP10商户交易情况
df_qr_transaction_top10_merchant=dfs['raw_qr_transaction_top10_merchant']
df_qr_transaction_top10_merchant['dis_proportion'] = df_qr_transaction_top10_merchant['discnt_today'] / df_qr_transaction_top10_merchant['cnt_today']
df_qr_transaction_top10_merchant['cnt_ratio'] = df_qr_transaction_top10_merchant['cnt_ratio'].apply(lambda x: format(float(x), '.2%'))
df_qr_transaction_top10_merchant['dis_proportion'] = df_qr_transaction_top10_merchant['dis_proportion'].apply(lambda x: format(float(x), '.2%'))


# In[77]:


df_qr_transaction_top10_merchant=df_qr_transaction_top10_merchant.loc[:,['mchnt_nm','type1','scene','cnt_today','cnt_ratio',
                                                                      'discnt_today','dis_proportion'] ] 


# In[78]:


target_text6="2、交易笔数TOP10的商户以乘车码交易为主，优惠笔数占比为{}%。".format(
    round(df_qr_transaction_top10_merchant['discnt_today'].sum()/df_qr_transaction_top10_merchant['cnt_today'].sum()*100,2)
)


# In[79]:


# 二维码交易金额分布
df_qr_transaction_by_amount_of_money=dfs['raw_qr_transaction_by_amount_of_money']
df_qr_transaction_by_amount_of_money['proportion'] = df_qr_transaction_by_amount_of_money['cnt_today'] / df_qr_transaction_by_amount_of_money['cnt_today'].sum()
df_qr_transaction_by_amount_of_money['avg_cnt'] = df_qr_transaction_by_amount_of_money['cnt_today'] / df_qr_transaction_by_amount_of_money['mchnt_today']
#df_qr_transaction_by_amount_of_money['ratio'] = df_qr_transaction_by_amount_of_money['ratio'].apply(lambda x: format(float(x), '.2%'))
df_qr_transaction_by_amount_of_money['proportion'] = df_qr_transaction_by_amount_of_money['proportion'].apply(lambda x: format(float(x), '.2%'))
df_qr_transaction_by_amount_of_money=df_qr_transaction_by_amount_of_money.loc[:,['金额','cnt_today','proportion','ratio','mchnt_today',
                                                                      'avg_cnt'] ]


# In[80]:


lower10=df_qr_transaction_by_amount_of_money['proportion'][df_qr_transaction_by_amount_of_money['金额']=='10元以下'].values[0]

target_text7 = "3、交易金额整体偏低，交易金额在10元以下的占比达{}。".format(lower10)


# In[81]:


#手机支付控件TOP100商户交易情况
df_control_transaction_top10_merchant=dfs['raw_control_transaction_top10_merchant']
df_control_transaction_top10_merchant['dis_proportion'] = df_control_transaction_top10_merchant['dis_cnt_today'] / df_control_transaction_top10_merchant['cnt_today']
df_control_transaction_top10_merchant['ratio_by_yesterday'] = df_control_transaction_top10_merchant['ratio_by_yesterday'].apply(lambda x: format(float(x), '.2%'))
df_control_transaction_top10_merchant['dis_proportion'] = df_control_transaction_top10_merchant['dis_proportion'].apply(lambda x: format(float(x), '.2%'))
df_control_transaction_top10_merchant=df_control_transaction_top10_merchant.drop(1)


# In[82]:


target_text12="1、手机支付控件TOP10商户主要是信用卡还款业务、以内部商户为主，商户优惠交易占比仅为{}%。".format(
    round(df_control_transaction_top10_merchant['dis_cnt_today'].sum() / df_control_transaction_top10_merchant['cnt_today'].sum() *100,2)
)


# In[83]:


#手机外部支付控件TOP100商户交易情况
df_control_transaction_top10_merchant_out=dfs['raw_control_out_transaction_top10_merchant']
df_control_transaction_top10_merchant_out['dis_proportion'] = df_control_transaction_top10_merchant_out['dis_cnt_today'] / df_control_transaction_top10_merchant_out['cnt_today']
df_control_transaction_top10_merchant_out['ratio_by_yesterday'] = df_control_transaction_top10_merchant_out['ratio_by_yesterday'].apply(lambda x: format(float(x), '.2%'))
df_control_transaction_top10_merchant_out['dis_proportion'] = df_control_transaction_top10_merchant_out['dis_proportion'].apply(lambda x: format(float(x), '.2%'))


# In[84]:


#手机控件交易情况
control_cnt=df_overview['cnt_today'][df_overview['index']=='control_cnt'].values[0]
control_cnt_by_yesterday=df_overview['ratio_by_yesterday'][df_overview['index']=='control_cnt'].values[0]
control_cnt_by_last_year=df_overview['ration_by_last_year'][df_overview['index']=='control_cnt'].values[0]


control_out_cnt=df_overview['cnt_today'][df_overview['index']=='control_out_cnt'].values[0]
control_out_cnt_by_yesterday=df_overview['ratio_by_yesterday'][df_overview['index']=='control_out_cnt'].values[0]
control_out_cnt_by_last_year=df_overview['ration_by_last_year'][df_overview['index']=='control_out_cnt'].values[0]

top100_mchnt=12352

target_text8="当日，手机支付控件交易{}万笔，环比下降{}%，同比下降{}%。其中手机外部支付控件交易{}万笔，环比增长{}%，同比下降{}%，占总控件交易笔数的{}%。".format(
    round(control_cnt/10000,2),
    round(control_cnt_by_yesterday*100,2),
    round(float(control_cnt_by_last_year)*100,2),
    round(control_out_cnt/10000,2),
    round(control_out_cnt_by_yesterday*100,2),
    round(float(control_out_cnt_by_last_year)*100,2),
    round(control_out_cnt/control_cnt*100,2)
)


# In[85]:


# 外部控件商户侧归属地
df_control_out_by_area_cd=dfs['raw_control_out_by_area_cd']
df_control_out_by_area_cd['交易笔数占比'] = df_control_out_by_area_cd['交易笔数'] / df_control_out_by_area_cd['交易笔数'].sum()
df_control_out_by_area_cd['交易笔数环比'] = df_control_out_by_area_cd['交易笔数环比'].apply(lambda x: format(float(x), '.2%'))
df_control_out_by_area_cd['优惠笔数环比'] = df_control_out_by_area_cd['优惠笔数环比'].apply(lambda x: format(float(x), '.2%'))
df_control_out_by_area_cd['交易笔数占比'] = df_control_out_by_area_cd['交易笔数占比'].apply(lambda x: format(float(x), '.2%'))
df_control_out_by_area_cd['优惠笔数占比'] = df_control_out_by_area_cd['优惠交易笔数'] / df_control_out_by_area_cd['交易笔数']
df_control_out_by_area_cd['优惠笔数占比'] = df_control_out_by_area_cd['优惠笔数占比'].apply(lambda x: format(float(x), '.2%'))
df_control_out_by_area_cd=df_control_out_by_area_cd.head(10).loc[:,['pro','交易笔数','交易笔数占比','交易笔数环比','优惠交易笔数',
                                                                    '优惠笔数占比','优惠笔数环比'] ] 


# In[86]:


for idx in df_control_out_by_area_cd.index:
        if df_control_out_by_area_cd.iloc[idx]["pro"] == '其他':
            #print(idx)
            df_control_out_by_area_cd = df_control_out_by_area_cd.drop([idx])
            break


# In[87]:


list_area=df_control_out_by_area_cd['pro'].values.tolist()
b='、'
area=b.join(list_area)

target_text9 ="2、当日，从商户入网分公司来看，"+area+"地区交易量排名手机外部支付控件前十。"
target_text9


# In[88]:


# 外部控件用户侧归属地
df_control_out_by_user_gps=dfs['raw_control_out_by_user_gps'].sort_values(by="交易笔数" , ascending=False)
df_control_out_by_user_gps.dropna(axis=0, subset=["branch"], inplace=True)
df_control_out_by_user_gps['交易笔数占比'] = df_control_out_by_user_gps['交易笔数'] / df_control_out_by_area_cd['交易笔数'].sum()
df_control_out_by_user_gps['交易笔数环比'] = df_control_out_by_user_gps['交易笔数环比'].apply(lambda x: format(float(x), '.2%'))
df_control_out_by_user_gps['优惠笔数环比'] = df_control_out_by_user_gps['优惠笔数环比'].apply(lambda x: format(float(x), '.2%'))
df_control_out_by_user_gps['交易笔数占比'] = df_control_out_by_user_gps['交易笔数占比'].apply(lambda x: format(float(x), '.2%'))
df_control_out_by_user_gps['优惠笔数占比'] = df_control_out_by_user_gps['优惠交易笔数'] / df_control_out_by_area_cd['交易笔数']
df_control_out_by_user_gps['优惠笔数占比'] = df_control_out_by_user_gps['优惠笔数占比'].apply(lambda x: format(float(x), '.2%'))
df_control_out_by_user_gps=df_control_out_by_user_gps.head(10).loc[:,['branch','交易笔数','交易笔数占比','交易笔数环比','优惠交易笔数',
                                                                '优惠笔数占比','优惠笔数环比'] ] 


# In[89]:


list_area=df_control_out_by_user_gps['branch'].values.tolist()
b='、'
area=b.join(list_area)
target_text10 ="3、当日，从交易用户归属地来看，"+area+"地区交易量排名手机外部支付控件前十。"


# In[90]:


# 外部控件交易金额分布
control_out_mchnt=df_overview['cnt_today'][df_overview['index']=='control_out_mchnt'].values[0]


# In[91]:


df_control_out_transaction_by_amount_of_money=dfs['raw_control_out_transaction_by_amount_of_money']
df_control_out_transaction_by_amount_of_money['交易笔数占比'] = df_control_out_transaction_by_amount_of_money['交易笔数'] / df_control_out_transaction_by_amount_of_money['交易笔数'].sum()
df_control_out_transaction_by_amount_of_money['商户数占比'] = df_control_out_transaction_by_amount_of_money['商户数'] /control_out_mchnt
df_control_out_transaction_by_amount_of_money['商户日均交易笔数'] = df_control_out_transaction_by_amount_of_money['交易笔数'] / df_control_out_transaction_by_amount_of_money['商户数']
df_control_out_transaction_by_amount_of_money['交易笔数占比'] = df_control_out_transaction_by_amount_of_money['交易笔数占比'].apply(lambda x: format(float(x), '.2%'))
df_control_out_transaction_by_amount_of_money['商户数占比'] = df_control_out_transaction_by_amount_of_money['商户数占比'].apply(lambda x: format(float(x), '.2%'))
df_control_out_transaction_by_amount_of_money=df_control_out_transaction_by_amount_of_money.loc[:,['金额区间','交易笔数','交易笔数占比','商户数','商户数占比','商户日均交易笔数']]


# In[61]:


#手机控件交易情况

abc=df_control_out_transaction_by_amount_of_money['交易笔数占比'][df_control_out_transaction_by_amount_of_money['金额区间']=='0-10元'].values[0]
target_text11="4、交易金额整体偏低。交易金额在10元以下的交易笔数占比达{}。".format(abc)


# In[93]:


# 二维码交易明细

user_data = dfs['raw_qr_transaction_by_city']
trans_data = dfs['raw_qr_transaction_by_merchant']

# 预处理
# 1 user_data: 删除city=nan的值
user_data.dropna(axis=0, subset=["city"], inplace=True)

# 2 trans_data: 也是删除city=nan的值
trans_data.dropna(axis=0, subset=["city"], inplace=True)

merged_data = trans_data.merge(user_data, how="left")

merged_data['avg_at'] = merged_data['trans'] / merged_data['cnt']
merged_data['avg_dis_at'] = merged_data['utrans'] / merged_data['discnt']
merged_data['dis_cnt_proportion'] = merged_data['discnt'] / merged_data['cnt']
merged_data['dis_at_proportion'] = merged_data['utrans'] / merged_data['trans']
merged_data['user_proportion'] = merged_data['user'] / merged_data['user2']
merged_data['dis_cnt_proportion'] = merged_data['dis_cnt_proportion'].apply(lambda x: format(float(x), '.2%'))
merged_data['dis_at_proportion'] = merged_data['dis_at_proportion'].apply(lambda x: format(float(x), '.2%'))
merged_data['user_proportion'] = merged_data['user_proportion'].apply(lambda x: format(float(x), '.2%'))
merged_data=merged_data.loc[:,['branch','city','mchnt_cd','mchnt_nm','type1','scene','cnt','trans','avg_at','discnt','utrans','avg_dis_at','dis_cnt_proportion','dis_at_proportion','user','user2','user_proportion']]


# In[94]:


# 控件交易明细

control_data = dfs['raw_control_by_merchant_details']
control_data=control_data.drop(1)

control_data['笔均交易金额'] = control_data['交易金额'] / control_data['交易笔数']
control_data['优惠笔数占比'] = control_data['优惠交易笔数'] / control_data['交易笔数']
control_data['人均交易笔数'] = control_data['交易笔数'] / control_data['用户数']
control_data['人均交易金额'] = control_data['交易金额'] / control_data['用户数']

control_data['优惠笔数占比'] = control_data['优惠笔数占比'].apply(lambda x: format(float(x), '.2%'))
control_data=control_data.loc[:,['分公司','商户类型','商户号','商户名称','交易笔数','交易金额','笔均交易金额','优惠交易笔数','优惠笔数占比','用户数','人均交易笔数','人均交易金额']]


# In[95]:


# 文本输出

target_text=[target_text1,target_text2,target_text3,target_text4,target_text5,target_text6,target_text7,target_text8,target_text9,target_text10,target_text11,target_text12]
out_put_text=pd.DataFrame(target_text)


# In[98]:


#保存成excel

path="/Users/apple/Desktop/UP/daily_report/report/"
filename1="report_data.xlsx"


# 打开excel
writer = pd.ExcelWriter(path + filename1)
#sheets是要写入的excel工作簿名称列表

out_put_text.to_excel(writer,'输出文本')
df_transaction_cnt_by_day.to_excel(writer,'支付类交易')
df_scece_new.to_excel(writer,'主要场景交易')
df_qr_transaction_by_area_cd.to_excel(writer,'二维码TOP10分公司')
df_qr_transaction_top10_merchant.to_excel(writer,'二维码TOP10商户')
df_qr_transaction_by_amount_of_money.to_excel(writer,'二维码金额分布')
df_control_transaction_top10_merchant.to_excel(writer,'控件TOP10商户')
df_control_transaction_top10_merchant_out.to_excel(writer,'外部控件TOP10商户')
df_control_out_by_area_cd.to_excel(writer,'控件商户侧地区分布')
df_control_out_by_user_gps.to_excel(writer,'控件用户侧地区分布')
df_control_out_transaction_by_amount_of_money.to_excel(writer,'控件金额分布')


# 保存writer中的数据至excel
# 如果省略该语句，则数据不会写入到上边创建的excel文件中
writer.save()


filename_detail="detail_data.xlsx"

writer2 = pd.ExcelWriter(path + filename_detail)
merged_data.to_excel(writer2,'二维码交易按城市划分TOP100商户')
control_data.to_excel(writer2,'手机支付控件交易商户')
writer2.save()

