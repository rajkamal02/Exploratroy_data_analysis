#!/usr/bin/env python
# coding: utf-8

# # <center>EDA - Terrorim</center>
# ## Objective:
# #● Perform ‘Exploratory Data Analysis’ on dataset ‘Global Terrorism’
# 
# #● As a security/defense analyst, try to find out the hot zone of terrorism.
# 
# #● What all security issues and insights you can derive by EDA?

# In[25]:


import math
import warnings
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
import plotly.offline as py
import plotly.graph_objs as go
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore')

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


        


# In[26]:


terror = pd.read_csv("D:\Folder 1 mca\globalterrorismdb_0718dist.csv",encoding='ISO-8859-1')


# In[27]:


terror.head()


# In[28]:


terror.columns


# In[29]:


terror.rename(columns={'iyear':'Year','imonth':'Month','iday':'Day','country_txt':'Country','provstate':'state',
                       'region_txt':'Region','attacktype1_txt':'AttackType','target1':'Target','nkill':'Killed',
                       'nwound':'Wounded','summary':'Summary','gname':'Group','targtype1_txt':'Target_type',
                       'weaptype1_txt':'Weapon_type','motive':'Motive'},inplace=True)


# In[30]:


# I'm just take important data in whole dataset those I'm using further processing.
terror=terror[['Year','Month','Day','Country','state','Region','city','latitude','longitude','AttackType','Killed',
               'Wounded','Target','Summary','Group','Target_type','Weapon_type','Motive']]


# In[31]:


terror.isnull().sum()


# In[32]:


terror.info()


# In[33]:


print("Country with the most attacks:",terror['Country'].value_counts().idxmax())
print("City with the most attacks:",terror['city'].value_counts().index[1]) #as first entry is 'unknown'
print("Region with the most attacks:",terror['Region'].value_counts().idxmax())
print("Year with the most attacks:",terror['Year'].value_counts().idxmax())
print("Month with the most attacks:",terror['Month'].value_counts().idxmax())
print("Group with the most attacks:",terror['Group'].value_counts().index[1])
print("Most Attack Types:",terror['AttackType'].value_counts().idxmax())


# In[34]:


print("Country with the most attacks:",terror['Country'].value_counts().idxmax())
print("City with the most attacks:",terror['city'].value_counts().index[1]) #as first entry is 'unknown'
print("Region with the most attacks:",terror['Region'].value_counts().idxmax())
print("Year with the most attacks:",terror['Year'].value_counts().idxmax())
print("Month with the most attacks:",terror['Month'].value_counts().idxmax())
print("Group with the most attacks:",terror['Group'].value_counts().index[1])
print("Most Attack Types:",terror['AttackType'].value_counts().idxmax())


# In[35]:


terror['Year'].value_counts(dropna = False).sort_index()


# # DATA VISUALISATION
# ## Number of Terrorist Activities each Year
# 

# In[36]:


x_year = terror['Year'].unique()
y_count_years = terror['Year'].value_counts(dropna = False).sort_index()
plt.figure(figsize = (18,10))
sns.barplot(x = x_year,
           y = y_count_years,
           palette = 'rocket')
plt.xticks(rotation = 45)
plt.xlabel('Attack Year')
plt.ylabel('Number of Attacks each year')
plt.title('Attack_of_Years')
plt.show()


# In[37]:


pd.crosstab(terror.Year, terror.Region).plot(kind='area',figsize=(15,6))
plt.title('Terrorist Activities by Region in each Year')
plt.ylabel('Number of Attacks')
plt.show()


# In[38]:


terror['Wounded'] = terror['Wounded'].fillna(0).astype(int)
terror['Killed'] = terror['Killed'].fillna(0).astype(int)
terror['casualities'] = terror['Killed'] + terror['Wounded']


# In[39]:


terror1 = terror.sort_values(by='casualities',ascending=False)[:40]


# In[40]:


heat=terror1.pivot_table(index='Country',columns='Year',values='casualities')
heat.fillna(0,inplace=True)


# In[41]:


heat.head()


# In[42]:


import plotly.offline as py
py.init_notebook_mode(connected=True)
import plotly.graph_objs as go
colorscale = [[0, '#edf8fb'], [.3, '#00BFFF'],  [.6, '#8856a7'],  [1, '#810f7c']]
heatmap = go.Heatmap(z=heat.values, x=heat.columns, y=heat.index, colorscale=colorscale)
data = [heatmap]
layout = go.Layout(
    title='Top 40 Worst Terror Attacks in History from 1982 to 2016',
    xaxis = dict(ticks='', nticks=20),
    yaxis = dict(ticks='')
)
fig = go.Figure(data=data, layout=layout)
py.iplot(fig, filename='heatmap',show_link=False)


# In[43]:


terror.Country.value_counts()[:15]


# # Top Countries affected by Terror Attacks

# In[44]:


plt.subplots(figsize=(15, 6))
sns.barplot(x=terror['Country'].value_counts()[:15].index, y=terror['Country'].value_counts()[:15].values, palette='Blues_d')
plt.title('Top Countries Affected')
plt.xlabel('Countries')
plt.ylabel('Count')
plt.xticks(rotation=90)
plt.show()


# # ANALYSIS ON CUSTOMIZED DATA
# ## Terrorist Attacks of a Particular year and their Locations
# 
# Let's look at the terrorist acts in the world over a certain year.

# In[48]:


import folium
from folium.plugins import MarkerCluster 
filterYear = terror['Year'] == 1970


# In[53]:


# Filtered data ke liye filterData variable
filterData = terror[filterYear]

# Filtered data ka info dekhne ke liye
# filterData.info()

# Required fields ko extract karne ke liye reqFilterData variable
reqFilterData = filterData.loc[:, 'city':'longitude']

# Latitude aur longitude mein NaN values ko drop karne ke liye
reqFilterData = reqFilterData.dropna()

# reqFilterData ko list mein convert karne ke liye
reqFilterDataList = reqFilterData.values.tolist()

# reqFilterDataList                  # ish code ko bhi


# In[54]:


# Map banayein
map = folium.Map(location=[0, 30], tiles='CartoDB positron', zoom_start=2)

# Marker Cluster banayein
markerCluster = folium.plugins.MarkerCluster().add_to(map)

# For loop se markers ko add karein
for point in range(0, len(reqFilterDataList)):
    folium.Marker(
        location=[reqFilterDataList[point][1], reqFilterDataList[point][2]],
        popup=reqFilterDataList[point][0]
    ).add_to(markerCluster)

# Map ko return karein
map

#Aapko har step ko comment mein samajhne mein madad milegi aur aapko code ki samajh mein bhi aasani hogi.


# # **1970 mein, 84% terrorist hamle American continent par hue the. 1970 mein, Middle East aur North Africa, jahan abhi wars aur terrorist hamle ka kendr hai, sirf ek terrorist hamla ka saamna kiya.**

# # Ab dekhte hain ki kaun-kaun se terrorist sangathan ne har desh mein apne operations carry out kiye hain. Ek value count hume woh terrorist sangathan dega jo sabse adhik hamle kiye hain. Humne 1 se indexing kiya hai 'Unknown' ke value ko negate karne ke liye.

# In[55]:


terror.Group.value_counts()[1:15]


# # 'Shining Path (SL)', 'Taliban', aur 'Islamic State of Iraq and the Levant (ISIL)' terrorist sangathanon ke operations dekhne ke liye

# In[56]:



test = terror[terror.Group.isin(['Shining Path (SL)', 'Taliban', 'Islamic State of Iraq and the Levant (ISIL)'])]


# In[57]:


test.Country.unique()


# In[59]:


# NaN values wale rows ko latitude aur longitude ke basis par hatane ke liye
terror_df_group = terror.dropna(subset=['latitude','longitude'])

# Duplicate rows ko 'Country' aur 'Group' ke basis par hatane ke liye
terror_df_group = terror_df_group.drop_duplicates(subset=['Country', 'Group'])

# Top 7 terrorist groups ko select karne ke liye
terrorist_groups = terror.Group.value_counts()[1:8].index.tolist()

# Select ki gayi terrorist groups ko filter karne ke liye
terror_df_group = terror_df_group.loc[terror_df_group.Group.isin(terrorist_groups)]

# Unique terrorist groups print karne ke liye
print(terror_df_group.Group.unique())


# In[60]:


# Map banayein
map = folium.Map(location=[20, 0], tiles="CartoDB positron", zoom_start=2)

# Marker Cluster banayein
markerCluster = folium.plugins.MarkerCluster().add_to(map)

# Loop ke through markers ko add karein
for i in range(0, len(terror_df_group)):
    folium.Marker(
        [terror_df_group.iloc[i]['latitude'], terror_df_group.iloc[i]['longitude']],
        popup='Group: {}<br>Country: {}'.format(terror_df_group.iloc[i]['Group'], terror_df_group.iloc[i]['Country'])
    ).add_to(map)

# Map return karein
map


# # **Upar wala map vyavasthit dikh raha hai, hata ki isse Country ko dekhne ke liye zoom-in kiya ja sakta hai. Isliye agle chart mein, maine Folium ke Marker Cluster ka istemal kiya hai in icons ko cluster karne ke liye. Isse dekhne mein aakarshan hota hai aur yeh behad interactive banta hai.**

# In[66]:


import folium
from folium.plugins import MarkerCluster

# Map banayein
m1 = folium.Map(location=[20, 0], tiles="CartoDB positron", zoom_start=2)

# Marker Cluster banayein
marker_cluster = MarkerCluster(
    name='clustered icons',
    overlay=True,
    control=False,
    icon_create_function=None
)

# Loop ke through markers ko add karein
for i in range(0, len(terror_df_group)):
    marker = folium.Marker([terror_df_group.iloc[i]['latitude'], terror_df_group.iloc[i]['longitude']])
    
    popup = 'Group: {}<br>Country: {}'.format(terror_df_group.iloc[i]['Group'], terror_df_group.iloc[i]['Country'])
    folium.Popup(popup).add_to(marker)
    
    marker_cluster.add_child(marker)

# Marker Cluster ko map mein add karein
marker_cluster.add_to(m1)

# OpenStreetMap layer add karein (with attribution)
folium.TileLayer(
    tiles='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    attr='Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors'
).add_to(m1)

# CartoDB Dark Matter layer add karein
folium.TileLayer('cartodbdark_matter').add_to(m1)

# Stamen Toner layer add karein
folium.TileLayer('stamentoner').add_to(m1)

# LayerControl add karein
folium.LayerControl().add_to(m1)

# Map ko display karein
m1


# In[67]:


terror.head()


# In[68]:


# Calculate the total number of people killed in terror attacks
killData = terror.loc[:, 'Killed']
total_killed = int(sum(killData.dropna()))  # Drop the NaN values
print('Number of people killed by terror attacks:', total_killed)


# In[70]:


# Extract the types of attacks associated with the deaths
attackData = terror.loc[:, 'AttackType']
# attackData

# Combine attack type and kill data
typeKillData = pd.concat([attackData, killData], axis=1)

typeKillData.head()


# In[72]:


# Create a pivot table to format the data with attack types and corresponding total killed
typeKillFormatData = typeKillData.pivot_table(columns='AttackType', values='Killed', aggfunc='sum')
typeKillFormatData


# In[73]:


typeKillFormatData.info()


# In[76]:


# Convert the column labels to a list
labels = typeKillFormatData.columns.tolist()

# Transpose the pivot table
transposed_data = typeKillFormatData.T

# Convert the transposed data to a 1D list
values = transposed_data.values.flatten().tolist()

# Create a pie chart
fig, ax = plt.subplots(figsize=(20, 20), subplot_kw=dict(aspect="equal"))
plt.pie(values, labels=labels, startangle=90, autopct='%.2f%%')
plt.title('Types of terrorist attacks that cause deaths')

# Add legend to the plot
plt.legend(labels, loc='upper right', bbox_to_anchor=(1.3, 0.9), fontsize=15)

# Display the pie chart
plt.show()


# # **<center>Hathiyar se hamle aur bharat/visphot 77% mauton ka karan hai is hamlo me. Is unchai dar wajah hai ki ye hamle aksar aatankwad ke karyakramo me baar-baar istemal hote hain. Isse spasht hota hai ki duniya ke liye hathiyar aur visphotak kitni khatarnak ho sakte hain.</center>**

# In[78]:


# Extract the countries and corresponding number of killed in terrorist attacks
countryData = terror.loc[:, 'Country']
# countyData

# Combine country data and kill data
countryKillData = pd.concat([countryData, killData], axis=1)  # Combining data for analysis


countryKillFormatData = countryKillData.pivot_table(columns='Country', values='Killed', aggfunc='sum')
countryKillFormatData


# In[79]:


fig_size = plt.rcParams["figure.figsize"]
fig_size[0]=25
fig_size[1]=25
plt.rcParams["figure.figsize"] = fig_size


# In[81]:


labels = countryKillFormatData.columns.tolist()
labels = labels[:50] # 50 bars provide a nice view
index = np.arange(len(labels))
transpoze = countryKillFormatData.T
values = transpoze.values.tolist()
values = values[:50]
values = [int(i[0]) for i in values] # Convert float to integer
colors = ['red', 'green', 'blue', 'purple', 'yellow', 'brown', 'black', 'gray', 'magenta', 'orange'] # Bar chart colors
fig, ax = plt.subplots(1, 1)

# Add horizontal grid lines to the plot
ax.yaxis.grid(True)

# Set figure size for the plot
fig_size = plt.rcParams["figure.figsize"]
fig_size[0] = 25
fig_size[1] = 25
plt.rcParams["figure.figsize"] = fig_size

# Create a bar chart
plt.bar(index, values, color=colors, width=0.9)
plt.ylabel('Killed People', fontsize=20)
plt.xlabel('Countries', fontsize=20)
plt.xticks(index, labels, fontsize=18, rotation=90)
plt.title('Number of people killed by countries', fontsize=20)

# Display the plot
plt.show()


# In[82]:


labels = countryKillFormatData.columns.tolist()
labels = labels[50:101] # Select labels for the second batch of countries
index = np.arange(len(labels))
transpoze = countryKillFormatData.T
values = transpoze.values.tolist()
values = values[50:101] # Select values for the second batch of countries
values = [int(i[0]) for i in values] # Convert float values to integers
colors = ['red', 'green', 'blue', 'purple', 'yellow', 'brown', 'black', 'gray', 'magenta', 'orange'] # Bar chart colors
fig, ax = plt.subplots(1, 1)

# Add horizontal grid lines to the plot
ax.yaxis.grid(True)

# Set figure size for the plot
fig_size = plt.rcParams["figure.figsize"]
fig_size[0] = 20
fig_size[1] = 20
plt.rcParams["figure.figsize"] = fig_size

# Create a bar chart
plt.bar(index, values, color=colors, width=0.9)
plt.ylabel('Killed People', fontsize=20)
plt.xlabel('Countries', fontsize=20)
plt.xticks(index, labels, fontsize=18, rotation=90)
plt.title('Number of people killed by countries', fontsize=20)

# Display the plot
plt.show()


# In[83]:


labels = countryKillFormatData.columns.tolist()
labels = labels[152:206]
index = np.arange(len(labels))
transpoze = countryKillFormatData.T
values = transpoze.values.tolist()
values = values[152:206]
values = [int(i[0]) for i in values]
colors = ['red', 'green', 'blue', 'purple', 'yellow', 'brown', 'black', 'gray', 'magenta', 'orange']
fig, ax = plt.subplots(1, 1)
ax.yaxis.grid(True)
fig_size = plt.rcParams["figure.figsize"]
fig_size[0]=25
fig_size[1]=25
plt.rcParams["figure.figsize"] = fig_size
plt.bar(index, values, color = colors, width = 0.9)
plt.ylabel('Killed People', fontsize=20)
plt.xlabel('Countries', fontsize = 20)
plt.xticks(index, labels, fontsize=18, rotation=90)
plt.title('Number of people killed by countries', fontsize = 20)
plt.show()


# # **<center><b>Madhye Poorv aur Uttar Afrika mein aatankvaadi hamle ke prabhaav ghatak hote hain. Madhye Poorv aur Uttar Afrika ko gambheer aatankvaadi hamlon ke sthal ke roop mein dekha jaata hai. Iske alawa, haalaanki ek dharaana hai ki Musalmaan aatankvaad ke samarthak hote hain, lekin Musalmaan log hi voh vyakti hote hain jinhon ne sabse adhik nuksaan uthaaya hai aatankvaadi hamlon ke kaaran. Graphics ko dekhte hue yeh saabit hota hai ki Iraq, Afghanistan aur Pakistan hi voh desh hain jinme sabse adhik nuksaan hua hai. Yeh saare desh Musalmaan desh hain.</b></center>**

# # **<center>Upvoted Thank you.</center>**

# In[ ]:




