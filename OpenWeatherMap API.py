#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd
import statistics
import requests
from datetime import datetime

dt = datetime.now()  # Get today's date and time
day = dt.day
month = dt.month
max_temp_list = list()
min_temp_list = list()
max_dict = {}
min_dict = {}
location = ['Anchorage, USA', 'Buenos Aires, Argentina', 'Sao Jose dos Campos, Brazil',
            'San Jose, Costa Rica', 'Nanaimo, Canada', 'Ningbo, China', 'Giza, Egypt',
            'Mannheim, Germany', 'Hyderabad, India', 'Tehran, Iran', 'Bishkek, Kyrgyzstan',
            'Riga, Latvia', 'Quetta, Pakistan', 'Warsaw, Poland', 'Dhahran, Saudia Arabia',
            'Madrid, Spain', 'Oldham, England']
output_direct = '/filepath/filename.csv'

for city in location:
    api_key = 'insertapikey'
    URL = 'https://api.openweathermap.org/data/2.5/forecast?'
    
    if city.count(' ') == 1:
        URL = URL + 'q=' + city.replace(', ', ',') + '&APPID=' + api_key + '&units=metric'
    
    else:
        city1 = city.replace(' ', '+')
        URL = URL + 'q=' + city1.replace(',+', ',') + '&APPID=' + api_key + '&units=metric'
    response = requests.get(URL)
    
    if response.status_code == 200:  # Success
        data = response.json()
        day_count = 1
        if dt.day == 28 and month == 2:
            day = 1
            day0 = 28
        elif dt.day == 30 and month in (9, 11, 4, 6):
            day = 1
            day0 = 30
        elif dt.day == 31 and month in (10, 12, 1, 3, 5, 7, 8):
            day = 1
            day0 = 31
        else:
            day = dt.day + 1
            day0 = dt.day
        max_dict[city] = {}
        min_dict[city] = {}
        min_temp_list = []
        max_temp_list = []
        
        for i in range(0, len(data['list'])):  # Loop over all the YYYY-mm-dd HH:MM:SS in the block list
            dt_tm = data['list'][i]["dt_txt"].split(' ')  # Split the current block into a list [ YY-mm-dd, HH:MM:SS ]
            yr_mth_day = dt_tm[0].split('-')  # Split the YYYY-mm-dd string into a list [ YYYY, mm, dd ]
            cur_day = int(yr_mth_day[2])  # Extract the block's month & day from the [ YYYY, mm, dd ] list as an integer
            
            if cur_day == (day - 1):
                continue
                
            elif cur_day == day0 + 6:
                break
                
            elif day != cur_day:  # If the block's day isn't the same as today's day
                day_count = day_count + 1
                day = cur_day
                min_temp_list = []
                max_temp_list = []
                max_t = float(data['list'][i]["main"]["temp_max"])
                min_t = float(data['list'][i]["main"]["temp_min"])
                max_temp_list.append(max_t)
                min_temp_list.append(min_t)
                max_temp = max(max_temp_list)
                min_temp = min(min_temp_list)
                max_dict[city].update({'Max ' + str(day_count): max_temp})
                min_dict[city].update({'Min ' + str(day_count): min_temp})

            else:
                max_t = float(data['list'][i]["main"]["temp_max"])
                min_t = float(data['list'][i]["main"]["temp_min"])
                max_temp_list.append(max_t)
                min_temp_list.append(min_t)
                max_temp = max(max_temp_list)
                min_temp = min(min_temp_list)
                max_dict[city].update({'Max ' + str(day_count): max_temp})
                min_dict[city].update({'Min ' + str(day_count): min_temp})

final_dict = {}
    
for c in min_dict:
    final_dict[c] = {}
    for i in min_dict[c]:
        for k in max_dict[c]:
            if i[-1] == k[-1]:
                final_dict[c].update({'Min ' + i[-1]: min_dict[c][i]})
                final_dict[c].update({'Max ' + i[-1]: max_dict[c][k]})
            else:
                continue

for i in final_dict:
    final_dict[i].update({'Min Avg': statistics.mean(min_dict[i].values())})
    final_dict[i].update({'Max Avg': statistics.mean(max_dict[i].values())})
print(final_dict)
    
df = pd.DataFrame.from_dict(final_dict, orient='index')
df.index.name = 'city'
df = df.reset_index()
df.to_csv(output_direct, float_format='%.2f', index=False)
