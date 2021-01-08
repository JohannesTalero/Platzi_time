# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 19:06:07 2021

@author: asus
"""
import pandas as pd
import numpy as np
from datetime import datetime


path='D:/2020-02/Platzi/Meta/'
#Create state dataframe
def init_state():
    data=pd.DataFrame(columns=['date','Id_School','state','Coef','lasts_content'])
    data.to_csv(path+'state'+'.csv')
#Update status
def Update_status():
    data=pd.read_csv(path+'state'+'.csv', index_col=0)
    
    School_Base=pd.read_csv(path+'School_Base'+'.csv', index_col=0)
    School_Base=pd.read_csv(path+'School_Base'+'.csv', index_col=0)
    TS=pd.read_csv('D:/2020-02/Platzi/Meta/'+'TS'+'.csv',index_col=0)   
    
    level_Orig=pd.read_csv(path+'Level_Base'+'.csv', index_col=0)
    Courses_level=pd.read_csv(path+'Courses_level'+'.csv', index_col=0)
    Concept=pd.read_csv(path+'Concept'+'.csv', index_col=0)
    Content=pd.read_csv(path+'Content'+'.csv', index_col=0)


    lim_concept=pd.merge(Content[['Id_content','Id_concept']].groupby('Id_concept').min().reset_index(),
             Content[['Id_content','Id_concept']].groupby('Id_concept').max().reset_index(),
             how='left',on='Id_concept')
    sdlim_concept.columns=['Id_concept','Min_Id_content','Max_Id_content']
    
    
    for i in School_Base.Id_School.unique():    
        temp_dict=dict()
        temp_dict.update({'date':[datetime.today()]})
        temp_dict.update({'Id_School':[i]})
        temp_dict.update({'State':[i]})





    