#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
import pandas as pd
import numpy as np
import math
import re
import os


# In[ ]:





# In[2]:


analyst_df = pd.read_csv("E:\DesktopWindownFile\Xccelerate_FullTime_course\project_glassdoor\Main_Data_Frame.csv")
engineer_df = pd.read_csv("E:\DesktopWindownFile\Xccelerate_FullTime_course\project_glassdoor\Data_Engineer.csv")
scientist_df = pd.read_csv("E:\DesktopWindownFile\Xccelerate_FullTime_course\project_glassdoor\Data_Scientist_DataFrame.csv")


# In[3]:


print(analyst_df.shape)
print(engineer_df.shape)
print(scientist_df.shape)


# In[4]:


total_raw_rows = analyst_df.shape[0] + engineer_df.shape[0] + scientist_df.shape[0]
total_raw_rows


# In[5]:


analyst_df = analyst_df.rename(columns={'new_overall_score':'overall_score'})
analyst_df["Job_Category"] = "Data Analyst"
analyst_df.head()


# In[9]:


# engineer_df = engineer_df[['Unnamed: 0','company', 'title', 'location','EmpBasicInfo', 'employerStats', 'JobDescriptionContainer', 'salary','overall_score']]
engineer_df["Job_Category"] = "Data Engineer"
engineer_df["overall_score"] = engineer_df["employerStats"].apply(lambda x: re.findall('(\d\.\d)', x)[0] if type(x)==str else np.nan)
engineer_df.head()


# In[ ]:


# engineer_df = engineer_df[['Unnamed: 0','company', 'title', 'location','EmpBasicInfo', 'employerStats', 'JobDescriptionContainer', 'salary','overall_score','Job_Category']]


# In[10]:



scientist_df["Job_Category"] = "Data Scientist"
scientist_df["overall_score"] = scientist_df["employerStats"].apply(lambda x: re.findall('(\d\.\d)', x)[0] if type(x)==str else np.nan)
scientist_df.head()


# In[11]:


scientist_df = scientist_df[['Unnamed: 0','company', 'title', 'location','EmpBasicInfo', 'employerStats', 'JobDescriptionContainer', 'salary','overall_score','Job_Category']]
scientist_df.head()


# In[12]:


combined_df = pd.concat([analyst_df,engineer_df,scientist_df])
combined_df.shape


# In[13]:


combined_df.index


# In[14]:


combined_df = combined_df.reset_index()
combined_df.index


# In[15]:


combined_df.head()


# In[16]:


combined_df.columns


# In[17]:


combined_df = combined_df.drop(columns=["index","Unnamed: 0"])
combined_df.head()


# In[18]:


combined_df.shape


# In[19]:


combined_df = combined_df[combined_df["company"].notna()]
combined_df.shape


# In[20]:


combined_df["EmpBasicInfo"] = combined_df["EmpBasicInfo"].str.split("\n")
combined_df["EmpBasicInfo"] = combined_df["EmpBasicInfo"].apply(lambda x: x[1:] if type(x)==list else np.nan)
combined_df["EmpBasicInfo"] = combined_df["EmpBasicInfo"].apply(lambda x: {i:k for i,k in zip(x[0::2],x[1::2])} if type(x)==list else np.nan)

combined_df["EmpBasicInfo"]


# In[21]:


combined_df = combined_df.reset_index()
combined_df.head()


# In[22]:


temp_size_list = []
temp_year_list = []
temp_type_list = []
temp_industry_list = []
temp_sector_list = []


for i in range(len(combined_df)):
    if type(combined_df["EmpBasicInfo"][i])==dict:
        try:
            temp_size_list.append(combined_df["EmpBasicInfo"][i]["Size"])
        except:
            temp_size_list.append(np.nan)
        try:
            temp_year_list.append(combined_df["EmpBasicInfo"][i]["Founded"])
        except:
            temp_year_list.append(np.nan)
        try:
            temp_type_list.append(combined_df["EmpBasicInfo"][i]["Type"])
        except:
            temp_type_list.append(np.nan)
        try:
            temp_industry_list.append(combined_df["EmpBasicInfo"][i]["Industry"])
        except:
            temp_industry_list.append(np.nan)
        try:
            temp_sector_list.append(combined_df["EmpBasicInfo"][i]["Sector"])
        except:
            temp_sector_list.append(np.nan)
            
    else:
        temp_size_list.append(np.nan)
        temp_year_list.append(np.nan)
        temp_type_list.append(np.nan)
        temp_industry_list.append(np.nan)
        temp_sector_list.append(np.nan)

combined_df["Company_Size"] = pd.Series(temp_size_list)
combined_df["Found_Year"] = pd.Series(temp_year_list)
combined_df["Company_Type"] = pd.Series(temp_type_list)
combined_df["Industry"] = pd.Series(temp_industry_list)
combined_df["Sector"] = pd.Series(temp_sector_list)

combined_df.head()


# In[23]:


combined_df = combined_df.drop(columns=["index","EmpBasicInfo", "employerStats","JobDescriptionContainer"])
combined_df.head()


# In[24]:


combined_df["salary"] = combined_df["salary"].apply(lambda x: re.findall("([H].+[K])",x)[0] if type(x)==str else np.nan)
combined_df["Lower_salary"] = combined_df["salary"].apply(lambda x: re.findall("(\d+)",x)[0] if type(x)==str else np.nan)
combined_df["Upper_salary"] = combined_df["salary"].apply(lambda x: re.findall("(\d+)",x)[-1] if type(x)==str else np.nan)
combined_df.head()


# In[25]:


print(combined_df.shape)
print(combined_df.columns)


# In[26]:


combined_df = combined_df[['company', 'title','Job_Category', 'location', 'overall_score', 'Company_Size', 'Found_Year', 'Company_Type', 'Industry', 'Sector', 'salary', 'Lower_salary', 'Upper_salary']]
combined_df.head()


# In[27]:


print(combined_df.shape)
print()
print(combined_df.dtypes)


# In[28]:


combined_df.Job_Category.value_counts()


# In[59]:


combined_df = combined_df.drop_duplicates()
combined_df


# In[60]:


combined_df.shape


# In[64]:


combined_df.dtypes


# In[69]:


combined_df.overall_score= combined_df.overall_score.astype("float")
combined_df.dtypes


# In[79]:


combined_df.Upper_salary = combined_df.Upper_salary.astype("float")


# In[80]:


combined_df.Lower_salary = combined_df.Lower_salary.astype("float")


# In[82]:


combined_df.dtypes


# In[83]:


combined_df.head(10)


# # Data Analysis below:

# In[85]:


combined_df.to_csv("E:\DesktopWindownFile\Xccelerate_FullTime_course\project_glassdoor\combined_dataframe_revised.csv",encoding="utf_8_sig")


# In[ ]:





# In[ ]:




