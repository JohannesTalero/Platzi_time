# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 19:06:07 2021

@author: asus
"""
import pandas as pd
from datetime import datetime
from datetime import timedelta

path='D:/2020-02/Platzi/Meta/'
#Filter table 
def filter_table_by(TS_Fil,Data,ID_G,ID_ob):
    Max=Data[[ID_ob,ID_G]].groupby(ID_G).max().reset_index()
    Max.columns=[ID_G,ID_ob+'_max']
    Filter_TS_=TS_Fil[[ID_ob,ID_G]].groupby(ID_G).max().reset_index()
    Filter_TS_=pd.merge(Filter_TS_,Max,how='left',on=[ID_G])
    Filter_TS_=Filter_TS_[Filter_TS_[ID_ob]!=Filter_TS_[ID_ob+'_max']]
    return(Filter_TS_)

#Create state dataframe
def init_state():
    data=pd.DataFrame(columns=['date','Id_School','state','Last_id','Coef','2_Weeks'])
    data.to_csv(path+'state'+'.csv')

#get state 
def def_state(Id_School,TS):
    # Valid state:
    #   1. unfinished_concept
    #   2. unfinished_course
    #   3. unfinished_level
    #   4. unfinished_schools
    
    level_Orig=pd.read_csv(path+'Level_Base'+'.csv', index_col=0)    
    Courses_level=pd.read_csv(path+'Courses_level'+'.csv', index_col=0)
    Concept=pd.read_csv(path+'Concept'+'.csv', index_col=0)
    Content=pd.read_csv(path+'Content'+'.csv', index_col=0)

    TS=pd.read_csv(path+'TS'+'.csv',index_col=0)   
    #----------
    TS=pd.merge(TS,Content[['Id_content','Id_concept']],how='left',on='Id_content')
    TS=pd.merge(TS,Concept[['Id_courses','Id_concept']],how='left',on='Id_concept')
    TS=pd.merge(TS,Courses_level,how='left',on='Id_courses')
    TS=pd.merge(TS,level_Orig,how='left',on='Id_level')
    
    #-------------
    Filter_TS=TS[TS['Id_School']==Id_School]
    if len(Filter_TS)!=0:
        Filter_TS_Concept=filter_table_by(Filter_TS,Content,'Id_concept','Id_content')
        if len(Filter_TS_Concept)>0:
            Filter_TS_Concept.reset_index(inplace=True)
            return(1,Filter_TS_Concept.loc[0]['Id_content'])
        else:
            Filter_TS_courses=filter_table_by(Filter_TS,Concept,'Id_courses','Id_concept')
            if len(Filter_TS_courses)>0:
                Filter_TS_courses.reset_index(inplace=True)
                return(2,Filter_TS_courses.loc[0]['Id_concept'])
            else:
                Filter_TS_level=filter_table_by(Filter_TS,Courses_level,'Id_level','Id_courses')
                if len(Filter_TS_level)>0:
                    Filter_TS_level.reset_index(inplace=True)
                    return(3,Filter_TS_level.loc[0]['Id_courses'])
                else:
                    Filter_TS_sh=filter_table_by(Filter_TS,level_Orig,'Id_School','Id_level')
                    return(4,Filter_TS_sh.loc[0]['Id_level'])
    else:
        return(4,-1)
        

#Update status
def Update_status():
    data=pd.read_csv(path+'state'+'.csv', index_col=0)
    
    School_Base=pd.read_csv(path+'School_Base'+'.csv', index_col=0)   
    level_Orig=pd.read_csv(path+'Level_Base'+'.csv', index_col=0)    
    Courses_level=pd.read_csv(path+'Courses_level'+'.csv', index_col=0)
    Concept=pd.read_csv(path+'Concept'+'.csv', index_col=0)
    Content=pd.read_csv(path+'Content'+'.csv', index_col=0)

    TS=pd.read_csv(path+'TS'+'.csv',index_col=0)   
    #----------
    TS=pd.merge(TS,Content[['Id_content','Id_concept']],how='left',on='Id_content')
    TS=pd.merge(TS,Concept[['Id_courses','Id_concept']],how='left',on='Id_concept')
    TS=pd.merge(TS,Courses_level,how='left',on='Id_courses')
    TS=pd.merge(TS,level_Orig,how='left',on='Id_level')

    lim_concept=pd.merge(Content[['Id_content','Id_concept']].groupby('Id_concept').min().reset_index(),
             Content[['Id_content','Id_concept']].groupby('Id_concept').max().reset_index(),
             how='left',on='Id_concept')
    lim_concept.columns=['Id_concept','Min_Id_content','Max_Id_content']
 
    #--------------------------
    Flag=TS.date.apply(lambda x: datetime.strptime(x, "%Y-%m-%d"))>datetime.today()-timedelta(days=20)
    TS_F=TS[Flag]  
    TS_F=TS_F[['Id_School','time']].groupby('Id_School').sum().reset_index()
    TS_F['time']=TS_F['time']/sum(TS_F['time'])
    for si in School_Base.Id_School.unique():
        print(si)
        temp_dict=dict()
        temp_dict.update({'date':[datetime.today()]})
        temp_dict.update({'Id_School':[si]})
        state_R=def_state(si,TS)
        temp_dict.update({'state':[state_R[0]]})
        temp_dict.update({'Last_id':[state_R[1]]})
        
        #Time and number Course
        Grup_SC=Content[['Id_concept','time_content']].groupby('Id_concept').sum().reset_index()
        Grup_SC=pd.merge(Grup_SC ,Concept[['Id_courses','Id_concept']],how='left',on='Id_concept')
        Grup_SC=pd.merge(Grup_SC ,Courses_level,how='left',on='Id_courses')
        Grup_SC=pd.merge(Grup_SC ,level_Orig[['Id_level','Id_School']],how='left',on='Id_level')
        Grup_SC=Grup_SC[Grup_SC['Id_School']==si]
        time=Grup_SC.time_content.sum()
        Num_Course=len(Grup_SC.Id_courses.unique())
        temp_dict.update({'Coef':[time/Num_Course]})
        try:
            temp_dict.update({'2_Weeks':[TS_F[TS_F['Id_School']==si].time.reset_index(drop=True)[0]]})        
        except:
            temp_dict.update({'2_Weeks':[0]})        
            
        print(temp_dict)
        temp=pd.DataFrame(temp_dict)
        data=data.append(temp).reset_index(drop=True)
    data.to_csv(path+'state'+'.csv')
    return(data)
