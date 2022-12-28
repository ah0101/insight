#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import getpass
user = getpass.getuser()
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


# In[3]:


pd.__version__


# Customer Segmentation

# In[4]:


address = 'C://Users//'+user+'//Downloads//C_S_Dataset.xlsx'

df = pd.ExcelFile(address)
sheet = df.sheet_names 

df.sheet_names  # see all sheet names


# In[5]:


session = df.parse(sheet[0])

trans = df.parse(sheet[1])


# In[6]:


session.head(1)


# In[7]:


trans.head(1)


# In[8]:


session.columns.to_list()


# In[9]:


trans.columns.to_list()


# In[10]:


#rename column anmes
trans.rename(columns={'member_Id':'memberId'}, inplace=True)


# In[11]:


trans.columns.to_list()


# In[12]:


session.isnull().sum()
# finds where there are nan values we have them in orderID


# In[13]:


trans.isnull().sum()
#finds where we have some nan values for gross_revenue_before_discount


# In[14]:


trans.head(2)


# In[15]:


import matplotlib.pyplot as plt
from datetime import datetime as dt


def chart_month(a):
    a.groupby(a["date"].dt.month).count().plot(kind="bar", y='memberId')
    plt.show()
    
chart_month(trans)


# In[16]:


def chart_area(a):
    a.groupby(a["country_from_ip"]).count().plot(kind="bar", y='memberId')
    plt.show()
    
chart_area(session)


# In[17]:


#timebound for transaction

def time (a):
    print(str(a["date"].min()) + ' is the min date')
    print(str(a["date"].max()) + ' is the max date')
    print (str(a["date"].max() - a["date"].min() ) + ' is the differences')
    
    name =[x for x in globals() if globals()[x] is a][0]
    return 'is was pulled from ' +  str(name)

time(trans)


# In[18]:


time(session)


# In[19]:


#extract the timebound we want
time = '2020-12-31'
trans_2021 = trans[trans.date > time]


# In[20]:


trans_2021.head(1)


# In[21]:


# time(trans_2021)

print(trans_2021["date"].min())
print(trans_2021["date"].max())
print("The data is from 0.5 year transaction")


# In[22]:


# do left merge from session to transaction as all_df

all_df = pd.merge(trans_2021,session,how = 'outer', on = "memberId")


# In[23]:


all_df.isnull().sum()


# In[24]:


all_df.nunique()


# Exploratory Data Analysis

# 1a) Revenue per member in US, Canada and Others

# In[25]:


all_df.head(2)


# In[26]:


Q1a = all_df[['memberId','gross_revenue','country_from_ip']]
Q1a = Q1a.drop_duplicates()


# In[27]:


Q1a_1 = Q1a.groupby('country_from_ip').agg(
    {'memberId':pd.Series.nunique,'gross_revenue':np.sum})


# In[28]:


Q1a_1


# In[29]:


revenue_per_member = Q1a_1.gross_revenue/Q1a_1.memberId
revenue_per_member


# In[30]:


revenue_per_member.plot.bar()


# 1b) sessions per visitor in US, Canada and Others

# In[31]:


all_df.columns.to_list()


# In[32]:


Q1b = all_df[['visitId','sum_pdp_menswear_views','sum_pdp_womenswear_views','sum_pdp_everythingelse_views','country_from_ip']]
Q1b.head(10)


# In[33]:


Q1b['session_men'] = Q1b.sum_pdp_menswear_views > 0
Q1b['session_women'] = Q1b.sum_pdp_womenswear_views > 0
Q1b['session_everything'] = Q1b.sum_pdp_everythingelse_views > 0


# In[34]:


Q1b.head(1)


# In[35]:


Q1b['session_men'] = Q1b['session_men'].astype(int)
Q1b['session_women'] = Q1b['session_women'].astype(int)
Q1b['session_everything'] = Q1b['session_everything'].astype(int)


# In[36]:


Q1b.head(1)


# In[37]:


Q1b['session_no'] = Q1b.session_men+Q1b.session_women+Q1b.session_everything


# In[38]:


Q1b.head(1)


# In[39]:


Q1b_1 = Q1b.groupby('country_from_ip').agg(
            {'visitId':pd.Series.nunique,'session_no':np.sum})


# In[40]:


Q1b_1.head(3)


# In[41]:


sessions_per_visitor = Q1b_1.session_no/Q1b_1.visitId
sessions_per_visitor


# In[42]:


sessions_per_visitor.plot.bar()


# 1c) Average order value (AOV) in US, Canada and Others

# In[43]:


#average order value (AOV) = revenue / # of order
Q1c = all_df[['orderId_x','gross_revenue','country_from_ip']]
Q1c = Q1c.drop_duplicates()
Q1c.head(1)


# In[44]:


AOV = Q1c.groupby('country_from_ip').agg(
    {'orderId_x': pd.Series.nunique, 'gross_revenue':np.sum})
AOV.head(3)


# In[45]:


Q1c_1 = AOV.gross_revenue/AOV.orderId_x
Q1c_1


# In[46]:


Q1c_1.plot.bar()


# 1d) Traffic in US, Canada and Others

# In[47]:


#traffic is the number of visit times between 1/1/2021 and 31/5/2021
Q1d = all_df[['visitId','country_from_ip']]
Q1d_1 = Q1d.groupby('country_from_ip').visitId.count()
Q1d_1


# In[48]:


Q1d_1.plot.bar()


# 1e) visit per visitor in US, Canada and Others
# 
# 

# In[49]:


#visit per visitor
Q1e = all_df[['visitId','country_from_ip']]
Q1e_1 = Q1e['visitId'].value_counts()
Q1e_1.head(3)


# In[50]:


Q1e_1 = Q1e_1.to_frame(name = 'time_of_visiting')
Q1e_1.head(3)


# In[51]:


Q1e_1 = Q1e_1.reset_index()
Q1e_1.head(3)


# In[52]:


Q1e_1 = Q1e_1.rename(columns={'index': 'visitId'})
Q1e_2 = pd.merge(Q1e_1,Q1e,how='left', on = 'visitId')
Q1e_2.head(3)


# In[53]:


Q1e_3 = Q1e_2.groupby('country_from_ip').agg(
    {'time_of_visiting': np.sum, 'visitId': pd.Series.count
    }
)
Q1e_3.head(3)


# In[54]:


visit_per_visitor = Q1e_3.time_of_visiting/Q1e_3.visitId
visit_per_visitor


# In[55]:


visit_per_visitor.plot.bar()


# 1f(i) Add to cart rate in US, Canada and Others
# 
# 

# In[56]:


#Add to cart rate by countries
Q1f = all_df[['memberId','country_from_ip','newsletter_gender_communication_preference','sum_addtocart_menswear','sum_addtocart_womenswear','sum_addtocart_everythingelse']]
Q1f['addtocart_times'] = Q1f.sum_addtocart_menswear+Q1f.sum_addtocart_womenswear+Q1f.sum_addtocart_everythingelse
Q1f['add_to_cart_morethan1'] = Q1f.addtocart_times > 0
Q1f['add_to_cart_morethan1'] = Q1f['add_to_cart_morethan1'].astype(int)
Q1f_1 = Q1f.groupby('country_from_ip').agg(
    {'add_to_cart_morethan1':np.sum ,'memberId':pd.Series.count }
)
ATC_rate_country = Q1f_1.add_to_cart_morethan1/Q1f_1.memberId*100
ATC_rate_country


# In[57]:


ATC_rate_country.plot.bar()


# 1f(ii) Add to cart rate in predict genders
# 
# 

# In[58]:


#Add to cart rate by gender
Q1f_2 = Q1f.groupby('newsletter_gender_communication_preference').agg(
    {'add_to_cart_morethan1':np.sum ,'memberId':pd.Series.count }
)
ATC_rate_gender = Q1f_2.add_to_cart_morethan1/Q1f_2.memberId*100
ATC_rate_gender


# In[59]:


all_df.info()


# RFM Analysis
# Recency Frequency Monetary (RFM)
# 
# RFM analysis allows you to segment customers by the frequency and value of purchases and identify those customers who spend the most money.
# 
# Recency — how long it’s been since a customer bought something from us.
# 
# Frequency — how often a customer buys from us.
# 
# Monetary value — the total value of purchases a customer has made.

# In[65]:


import datetime as dt


# In[66]:


trans_2021.head()


# In[68]:


NOW = dt.date(2021,5,31) 
trans_2021['date'] = pd.DatetimeIndex(trans_2021.date).date


# In[72]:


#Recency

df_recency = trans_2021.groupby(['memberId'],as_index=False)['date'].max()
df_recency.columns = ['memberId','Last_Purchase_Date']
df_recency.head()


# In[73]:


df_recency['Recency'] = df_recency.Last_Purchase_Date.apply(lambda x:(NOW - x).days)
#df_recency.drop(columns=['Last_Purchase_Date'],inplace=True)
df_recency.head()


# In[76]:


#Frequency - Monetarty

FM_Table = trans_2021.groupby('memberId').agg({'orderId'   : pd.Series.count,
                                         'gross_revenue'  : np.sum })
FM_Table.head()


# In[77]:


FM_Table.rename(columns = {'orderId' :'Frequency',
                           'gross_revenue':'Monetary'},inplace= True)
FM_Table.head()


# In[78]:


RFM_Table = df_recency.merge(FM_Table,left_on='memberId',right_on='memberId')
RFM_Table.head()


# In[80]:


#Heatmap check
import seaborn as sns

sns.heatmap(RFM_Table.corr(), annot=True)


# A highlight in the above chart is customers with high frequency to the website tends to spend more money.
# 
# 

# Modeling Data: RFM Quantiles
# 
#     Now we split the metrics into segments using quantiles.
# We will assign a score from 1 to 4 to each Recency, Frequency and Monetary respectively.
# 1 is the highest value, and 4 is the lowest value.
# A final RFM score (Overall Value) is calculated simply by combining individual RFM score numbers.

# In[81]:


quantiles = RFM_Table.quantile(q=[0.25,0.50,0.75])
quantiles = quantiles.to_dict()


# In[82]:


segmented_rfm = RFM_Table.copy()


# In[83]:


def RScore(x,p,d):
    if x <= d[p][0.25]:
        return 1
    elif x <= d[p][0.50]:
        return 2
    elif x <= d[p][0.75]: 
        return 3
    else:
        return 4
    
def FMScore(x,p,d):
    if x <= d[p][0.25]:
        return 4
    elif x <= d[p][0.50]:
        return 3
    elif x <= d[p][0.75]: 
        return 2
    else:
        return 1


# In[85]:


RScore([1])


# In[86]:


segmented_rfm['R_quartile'] = segmented_rfm['Recency'].apply(RScore, args=('Recency',quantiles))
segmented_rfm['F_quartile'] = segmented_rfm['Frequency'].apply(FMScore, args=('Frequency',quantiles))
segmented_rfm['M_quartile'] = segmented_rfm['Monetary'].apply(FMScore, args=('Monetary',quantiles))
segmented_rfm.head()


# In[ ]:




