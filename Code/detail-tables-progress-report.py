#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import sys
from os import walk
import datetime


# In[2]:


sys.path.insert(0, '../Code/utils')
import objects


# # Loading total number of cases scraped in master files

# In[3]:


folder = '../Outputs/'


# In[4]:


for _, _, f3 in walk(folder+'master'):
    files = f3


# In[5]:


master_files = []
for file in files:
    if file[:6] == 'master':
        master_files.append(file)


# In[6]:


df = pd.DataFrame()
for file in master_files:
    df_temp = pd.read_csv(folder+'master/'+file, encoding='latin1')
    df = df.append(df_temp)


# In[7]:


df = df.drop(columns=['Page'])


# In[8]:


df = df.drop_duplicates()


# In[9]:


len(df)


# # Loading details file

# In[10]:


for _, _, f3 in walk(folder+'details'):
    files = f3


# In[11]:


master_files = []
for file in files:
    if file[:7] == 'details':
        master_files.append(file)


# In[12]:


df2 = pd.DataFrame()
for file in master_files:
    df_temp = pd.read_csv(folder+'details/'+file, encoding='latin1')
    _, year, month, _ = file.split('_')
    df_temp['year'] = year
    df_temp['month'] = month
    df2 = df2.append(df_temp)


# In[13]:

df2['Tribunal'] = df2['Tribunal'].astype(str).apply(lambda x: x.replace('Âº', 'º'))
df2 = df2.drop_duplicates()


# In[14]:


df2['Rol'] = df2['ROL'].astype(str).apply(lambda x: x.split()[0])
dfa = df.merge(df2, how='outer', on=['Tribunal', 'Rol'], indicator=True)
perc = dfa['_merge'].value_counts().iloc[0].sum() / len(df) * 100
print('Percentage finished: '+str(round(perc, 1))+'%')
print('Current time: '+datetime.datetime.now().isoformat()[:16].replace('T', ' '))


# # Counting number of tribunals finished

# In[15]:


df2['total-details'] = 1


# In[16]:


df3 = df2[['year', 'month', 'Tribunal', 'total-details']].groupby(['year', 'month', 'Tribunal']).count().reset_index()


# In[17]:


df['month'] = df['Fecha'].apply(lambda x: x.split('/')[1])
df['year'] = df['Fecha'].apply(lambda x: x.split('/')[2])
df['total-master'] = 1


# In[18]:


months_dict = {
    '01': 'Enero',
    '02': 'Febrero',
    '2':  'Febrero',
    '03': 'Marzo',
    '04': 'Abril',
    '05': 'Mayo',
    '06': 'Junio',
    '07': 'Julio',
    '08': 'Agosto',
    '09': 'Septiembre',
    '10': 'Octubre',
    '11': 'Noviembre',
    '12': 'Diciembre'
}


# In[19]:


df['month'] = df['month'].map(months_dict)


# In[20]:


df4 = df[['year', 'month', 'Tribunal', 'total-master']].groupby(['year', 'month', 'Tribunal']).count().reset_index()


# In[21]:


total_df = df3.merge(df4, how='inner')


# In[22]:


total_df['finished'] = 0
total_df.loc[total_df['total-master'] - total_df['total-details'] <= 2, 'finished'] = 1


# In[29]:


total_df.to_csv('../Progress reports/progress_details data tables.csv', index=False, encoding='latin1')


# In[24]:


finished = total_df[total_df['total-details'] >= total_df['total-master']]


# In[28]:


print('Total number of tribunals finished: '+str(len(finished))+'/'+str(len(total_df)))
