import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup


#Schools and careers
pg_web_platzi='https://platzi.com'
schools={'Data_science':'/datos/',
         'Startups':'/startups/',
         'Web_development':'/web/',
         'English_School':'/english-school/',
         'Marketing':'/data-marketing/'}

Data_platzi_goals=pd.DataFrame()

for k in schools.keys():
    pag=requests.get(pg_web_platzi+schools[k])
    
    s=BeautifulSoup(pag.text,'lxml')
    levels=s.find_all('div',attrs={'class':'RoutesList'})
    
    data_school=pd.DataFrame()
    for l in levels:
        level_name=l.find('h3').text  
        courses_name=[c.text for c in l.find_all('h4')]          
        courses=[c.get('href') for c in l.find_all('a')]    
        
        if len(courses_name)>len(courses):
            courses=courses+['']    
            
        data_level=pd.DataFrame({'courses_names':courses_name
                                 ,'courses_links':courses})
        data_level['level']=level_name
        data_school=data_school.append(data_level)
    
    data_school['school']=k
    Data_platzi_goals=Data_platzi_goals.append(data_school)

Data_platzi_goals.reset_index(drop=True,inplace=True)

Data_platzi_goals.to_csv('H:/2020-02/Platzi/Meta/Data_platzi_goals.csv')