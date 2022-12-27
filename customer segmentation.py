#!/usr/bin/env python
# coding: utf-8

# In[37]:


import pandas as pd
import numpy as np
import getpass
user = getpass.getuser()
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


# In[15]:


pd.__version__


# Customer Segmentation

# In[16]:


address = 'C://Users//'+user+'//Downloads//C_S_Dataset.xlsx'

df = pd.ExcelFile(address)
sheet = df.sheet_names 

df.sheet_names  # see all sheet names


# In[17]:


session = df.parse(sheet[0])

trans = df.parse(sheet[1])


# In[5]:


session.head(1)


# In[6]:


trans.head(1)


# In[7]:


session.columns.to_list()


# In[8]:


trans.columns.to_list()


# In[20]:


#rename column anmes
trans.rename(columns={'member_Id':'memberId'}, inplace=True)


# In[21]:


trans.columns.to_list()


# In[22]:


session.isnull().sum()
# finds where there are nan values we have them in orderID


# In[23]:


trans.isnull().sum()
#finds where we have some nan values for gross_revenue_before_discount


# In[24]:


trans.head(2)


# In[25]:


import matplotlib.pyplot as plt
from datetime import datetime as dt


def chart_month(a):
    a.groupby(a["date"].dt.month).count().plot(kind="bar", y='memberId')
    plt.show()
    
chart_month(trans)


# In[120]:


def chart_area(a):
    a.groupby(a["country_from_ip"]).count().plot(kind="bar", y='memberId')
    plt.show()
    
chart_area(session)


# In[26]:


#timebound for transaction

def time (a):
    print(str(a["date"].min()) + ' is the min date')
    print(str(a["date"].max()) + ' is the max date')
    print (str(a["date"].max() - a["date"].min() ) + ' is the differences')
    
    name =[x for x in globals() if globals()[x] is a][0]
    return 'is was pulled from ' +  str(name)

time(trans)


# In[27]:


time(session)


# In[28]:


#extract the timebound we want
time = '2020-12-31'
trans_2021 = trans[trans.date > time]


# In[29]:


trans_2021.head(1)


# In[32]:


# time(trans_2021)

print(trans_2021["date"].min())
print(trans_2021["date"].max())
print("The data is from 0.5 year transaction")


# In[33]:


# do left merge from session to transaction as all_df

all_df = pd.merge(trans_2021,session,how = 'outer', on = "memberId")


# In[34]:


all_df.isnull().sum()


# In[35]:


all_df.nunique()


# Exploratory Data Analysis

# 1a) Revenue per member in US, Canada and Others

# In[38]:


all_df.head(2)


# In[39]:


Q1a = all_df[['memberId','gross_revenue','country_from_ip']]
Q1a = Q1a.drop_duplicates()


# In[44]:


Q1a_1 = Q1a.groupby('country_from_ip').agg(
    {'memberId':pd.Series.nunique,'gross_revenue':np.sum})


# In[42]:


Q1a_1


# In[45]:


revenue_per_member = Q1a_1.gross_revenue/Q1a_1.memberId
revenue_per_member


# In[46]:


revenue_per_member.plot.bar()


# 1b) sessions per visitor in US, Canada and Others

# In[47]:


all_df.columns.to_list()


# In[50]:


Q1b = all_df[['visitId','sum_pdp_menswear_views','sum_pdp_womenswear_views','sum_pdp_everythingelse_views','country_from_ip']]
Q1b.head(10)


# In[53]:


Q1b['session_men'] = Q1b.sum_pdp_menswear_views > 0
Q1b['session_women'] = Q1b.sum_pdp_womenswear_views > 0
Q1b['session_everything'] = Q1b.sum_pdp_everythingelse_views > 0


# In[54]:


Q1b.head(1)


# In[55]:


Q1b['session_men'] = Q1b['session_men'].astype(int)
Q1b['session_women'] = Q1b['session_women'].astype(int)
Q1b['session_everything'] = Q1b['session_everything'].astype(int)


# In[56]:


Q1b.head(1)


# In[57]:


Q1b['session_no'] = Q1b.session_men+Q1b.session_women+Q1b.session_everything


# In[58]:


Q1b.head(1)


# In[59]:


Q1b_1 = Q1b.groupby('country_from_ip').agg(
            {'visitId':pd.Series.nunique,'session_no':np.sum})


# In[61]:


Q1b_1.head(3)


# In[62]:


sessions_per_visitor = Q1b_1.session_no/Q1b_1.visitId
sessions_per_visitor


# In[63]:


sessions_per_visitor.plot.bar()


# 1c) Average order value (AOV) in US, Canada and Others

# In[65]:


#average order value (AOV) = revenue / # of order
Q1c = all_df[['orderId_x','gross_revenue','country_from_ip']]
Q1c = Q1c.drop_duplicates()
Q1c.head(1)


# In[66]:


AOV = Q1c.groupby('country_from_ip').agg(
    {'orderId_x': pd.Series.nunique, 'gross_revenue':np.sum})
AOV.head(3)


# In[67]:


Q1c_1 = AOV.gross_revenue/AOV.orderId_x
Q1c_1


# In[68]:


Q1c_1.plot.bar()


# 1d) Traffic in US, Canada and Others

# In[70]:


#traffic is the number of visit times between 1/1/2021 and 31/5/2021
Q1d = all_df[['visitId','country_from_ip']]
Q1d_1 = Q1d.groupby('country_from_ip').visitId.count()
Q1d_1


# In[71]:


Q1d_1.plot.bar()


# 1e) visit per visitor in US, Canada and Others
# 
# 

# In[81]:


#visit per visitor
Q1e = all_df[['visitId','country_from_ip']]
Q1e_1 = Q1e['visitId'].value_counts()
Q1e_1.head(3)


# In[82]:


Q1e_1 = Q1e_1.to_frame(name = 'time_of_visiting')
Q1e_1.head(3)


# In[83]:


Q1e_1 = Q1e_1.reset_index()
Q1e_1.head(3)


# In[85]:


Q1e_1 = Q1e_1.rename(columns={'index': 'visitId'})
Q1e_2 = pd.merge(Q1e_1,Q1e,how='left', on = 'visitId')
Q1e_2.head(3)


# In[86]:


Q1e_3 = Q1e_2.groupby('country_from_ip').agg(
    {'time_of_visiting': np.sum, 'visitId': pd.Series.count
    }
)
Q1e_3.head(3)


# In[87]:


visit_per_visitor = Q1e_3.time_of_visiting/Q1e_3.visitId
visit_per_visitor


# In[88]:


visit_per_visitor.plot.bar()


# 1f(i) Add to cart rate in US, Canada and Others
# 
# 

# In[90]:


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


# In[92]:


ATC_rate_country.plot.bar()


# 1f(ii) Add to cart rate in predict genders
# 
# 

# In[93]:


#Add to cart rate by gender
Q1f_2 = Q1f.groupby('newsletter_gender_communication_preference').agg(
    {'add_to_cart_morethan1':np.sum ,'memberId':pd.Series.count }
)
ATC_rate_gender = Q1f_2.add_to_cart_morethan1/Q1f_2.memberId*100
ATC_rate_gender


# In[94]:


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

# In[96]:


#https://github.com/TiffanyLaw325/Customer_segmentation/blob/main/data.ipynb


# In[ ]:




