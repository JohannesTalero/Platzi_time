# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 20:51:04 2020

@author: asus
"""
import pandas as pd
import numpy as np

path='D:/2020-02/Platzi/Meta/'
Data_Orig=pd.read_csv(path+'End_scrapping.csv')
# From big to small
del Data_Orig['Unnamed: 0']
#-------------- School --------------------------
Schools=Data_Orig[['school']].drop_duplicates().reset_index(drop=True)
Schools.reset_index(inplace=True)
Schools.columns=['Id_School','Schools_name']
Schools.to_csv(path+'School_Base'+'.csv')

#-------------- Level --------------------------
level_Orig=Data_Orig[['school','level']].drop_duplicates().reset_index(drop=True)
level_Orig.reset_index(inplace=True)
level_Orig.columns=['Id_level','Schools_name','level_name']
level_Orig=pd.merge(level_Orig,Schools,how='left',on='Schools_name')
del level_Orig['Schools_name']
level_Orig.to_csv(path+'Level_Base'+'.csv')

#-------------- Courses --------------------------
Courses=Data_Orig[['level','courses_names','courses_links']].drop_duplicates().reset_index(drop=True)
level_Orig.reset_index(inplace=True)
level_Orig.columns=['Id_level','Schools_name','level_name']
level_Orig=pd.merge(level_Orig,Schools,how='left',on='Schools_name')
del level_Orig['Schools_name']
level_Orig.to_csv(path+'Level_Base'+'.csv')








