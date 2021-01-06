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
level_Orig=Data_Orig[['level']].drop_duplicates().reset_index(drop=True)
level_Orig.reset_index(inplace=True)
level_Orig.columns=['Id_level','level']
level_Orig=pd.merge(level_Orig,Data_Orig[['school','level']].drop_duplicates(),how='left',on='level')
level_Orig.columns=['Id_level','level_name','Schools_name']
level_Orig=pd.merge(level_Orig,Schools,how='left',on='Schools_name')
del level_Orig['Schools_name']
level_Orig.to_csv(path+'Level_Base'+'.csv')

#-------------- Courses --------------------------
Courses=Data_Orig[['courses_names']].drop_duplicates().reset_index(drop=True)
Courses.reset_index(inplace=True)
Courses.columns=['Id_courses','courses_names']
Courses=pd.merge(Courses,Data_Orig[['courses_names','courses_links']].drop_duplicates(),how='left',on='courses_names')
Courses.to_csv(path+'Courses_Base'+'.csv')

Courses_level=Data_Orig[['courses_names','level']].drop_duplicates().reset_index(drop=True)
Courses_level=pd.merge(Courses_level,Courses,how='left',on='courses_names')
Courses_level=pd.merge(Courses_level,level_Orig,how='left',right_on='level_name',left_on='level')
Courses_level=Courses_level[['Id_courses','Id_level']]

Courses_level=Courses_level.drop_duplicates().reset_index(drop=True)
Courses_level.to_csv(path+'Courses_level'+'.csv')

#-------------- Concept --------------------------
Concept=Data_Orig[['courses_names','concept_name']].drop_duplicates().reset_index(drop=True)
Concept.reset_index(inplace=True)
Concept.columns=['Id_concept','courses_names','concept_name'] 
Concept=pd.merge(Concept,Courses,how='left',on='courses_names')
del Concept['courses_names']
del Concept['courses_links']
Concept.to_csv(path+'Concept'+'.csv')

#-------------- Content --------------------------
Content=Data_Orig[['content','time','concept_name','courses_names']].drop_duplicates().reset_index(drop=True)
Content.reset_index(inplace=True)
Content.columns=['Id_content','content_names','time_content','concept_name','courses_names']
Content=pd.merge(Content,Courses,how='left',on='courses_names')
del Content['courses_links']
del Content['courses_names']
Content=pd.merge(Content,Concept,how='left',on=['concept_name','Id_courses'])
del Content['concept_name']
del Content['Id_courses']

Content['time_content']=np.where(Content['time_content'].isnull(),60,Content['time_content'])
Content.to_csv(path+'Content'+'.csv')

#------------- Time Seen -----------------------
TS=pd.DataFrame(columns=['Id_content','time','date','start_h','end_h','note'])
TS.to_csv(path+'TS'+'.csv')













