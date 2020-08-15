import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup

path='H:/2020-02/Platzi/Meta/'

pg_web_platzi='https://platzi.com'

goals_platzi_time=pd.read_csv(path+'Data_platzi_goals.csv')
del goals_platzi_time['Unnamed: 0']
goals_platzi_time['courses_links']=goals_platzi_time['courses_links'].str.replace('cursos','clases')

data_course=pd.DataFrame()
for a in range(len(goals_platzi_time)):
    link=goals_platzi_time.iloc[a].courses_links
    if link is np.nan:
        pass
    else:
        pag=requests.get(pg_web_platzi+link)
        s=BeautifulSoup(pag.text,'lxml')
        levels=s.find_all('div',attrs={'class':'Material-concept'})
        
        for l in levels:
            concept_name=l.find('h3').text
            content=l.find_all('div',attrs={'class':'MaterialItem-content'})
            
            for c in content:
                content_name=c.find('p',attrs={'class':'MaterialItem-copy-title'}).text      
                try:
                    content_time=c.find('p',attrs={'class':'MaterialItem-copy-time'}).text
                    content_time=int(content_time.split(' ')[0].split(':')[0])*60+int(content_time.split(' ')[0].split(':')[1])
                except:
                   content_time=np.nan
                data_t=pd.DataFrame({'level':[content_name],
                                     'time':[content_time]})
                data_t['courses_links']=link           
                data_course=data_course.append(data_t)
    if a%10==0:
        print(f'%{100*round(a/len(goals_platzi_time),2)}')
    
data_course.reset_index(drop=True,inplace=True)

goals_platzi_time=goals_platzi_time.merge(data_course,how='left',on=['courses_links'])
goals_platzi_time.to_csv(path+'End_scrapping.csv')

