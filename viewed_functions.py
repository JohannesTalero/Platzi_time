 # -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 13:00:52 2020
@author: 
"""

import pandas as pd
from datetime import datetime
from datetime import timedelta

# viewed_content
def viewed_content(Id_content, timen, time_i, note=''):
    """
    Parameters
    ----------
    Id_content : Int
        ID contetent.
    timen : Int
        Number of seconds of content.
    time_i : Int
        Number of seconds sice beginning.
    note : str, optional
        Additional comment. The default is ''.

    Returns
    -------
    None.
    Add content to the viewed list 

    """
    try:        
        TS=pd.read_csv('D:/2020-02/Platzi/Meta/'+'TS'+'.csv',index_col=0)   
             
        temp=pd.DataFrame({'Id_content':[Id_content],'time':[timen],'date':[datetime.today().strftime('%Y-%m-%d')],
                          'start_h':[(datetime.today()-(timedelta(seconds=time_i))).strftime('%H:%M:%S')],
                          'end_h':[(datetime.today()-(timedelta(seconds=time_i))+(timedelta(seconds=timen))).strftime('%H:%M:%S')],'note':[note]})
        TS=TS.append(temp)
        TS.reset_index(drop=True,inplace=True)
        TS.to_csv('D:/2020-02/Platzi/Meta/'+'TS'+'.csv')
    except:
        print('Could not save the view named '+Id_content)
    
    
def viewed_content_multiple(Ids_content, timesn, notes):
    """
    Parameters
    ----------
    Ids_content : Array 
        IDs contetent.
    timesn : Array
        Number of seconds of content.
    notes : Array, optional
        Additional comment. The default is ''.

    Returns
    -------
    None.
    Add content to the viewed list 

    """
    Final_Time=sum(timesn)
    for i in range(len(Ids_content)):
        Final_Time
        viewed_content(Ids_content[i], timesn[i], Final_Time, note=notes[i])
        Final_Time=Final_Time-timesn[i]
        
        
def viewed_Concept(Id_concept, note_g=''):
    """
    Parameters
    ----------
    Id_concept : Int
        ID Concept.
    note_g : str, optional
        Additional comment. The default is ''.

    Returns
    -------
    None.
    Add concept to the viewed list 

    """
    Content=pd.read_csv('D:/2020-02/Platzi/Meta/'+'Content'+'.csv',index_col=0)   
    Content_Fil=Content[Content['Id_concept']==Id_concept]
    
    Ids_contents=list(Content_Fil.Id_content)
    timesn=list(Content_Fil.time_content)
    notes=[note_g]*len(timesn)
    viewed_content_multiple(Ids_contents, timesn, notes)
        
def viewed_Courses(Id_courses, note_g=''):
    """
    Parameters
    ----------
    Id_courses : Int
        ID Courses.
    note_g : str, optional
        Additional comment. The default is ''.

    Returns
    -------
    None.
    Add Courses to the viewed list 

    """
    Concept=pd.read_csv('D:/2020-02/Platzi/Meta/'+'Concept'+'.csv',index_col=0)   
    Concept_Fil=Concept[Concept['Id_courses']==Id_courses]
    for i in Concept_Fil.Id_concept.unique():
        viewed_Concept(i, note_g)


def input_validate(message, valid_answers,v_quit=False):
    inappropriate_Answer=True
    while inappropriate_Answer:
        try:
            clic=int(input(message+': '))
            if (clic in valid_answers):
                inappropriate_Answer=False
            else:
                print('Please select a valid value')
        except:
             print('Please select a valid value')
    return(clic)

def add_view_Content(Id_concept):
    Content=pd.read_csv('D:/2020-02/Platzi/Meta/'+'Content'+'.csv',index_col=0)   
    Content=Content[Content['Id_concept']==Id_concept]
    print(f"""
#################### Please select the Id_content ####################
{Content[['Id_content','content_names']]} 
-1. Back to general menu          
              """)

    valid=list(Content.Id_content.unique())
    valid.append(-1)

    inappropriate_Answer=True
    while inappropriate_Answer:
        try:
            clic=input('Id_content: ')
            clic=clic.split(',')
            clic=[int(x) for x in clic]
            
            if (len(set(clic).intersection(set(valid)))==len(set(clic))):
                inappropriate_Answer=False
            else:
                print('Please select a valid value')
        except:
             print('Please select a valid value')
  
    if clic==[-1]:
       add_view_GM()
    else:
        clic=[c for c in clic if c!=-1]
        times=[]
        for c in clic:
            times.append(Content[Content['Id_content']==c].reset_index(drop=True)['time_content'][0]) 
        note=input('Add note: ')     
        viewed_content_multiple(clic, times, note*len(clic))
        print('Successfully added')

def add_view_Concept(Id_courses):
    Concepts=pd.read_csv('D:/2020-02/Platzi/Meta/'+'Concept'+'.csv',index_col=0)   
    Concepts=Concepts[Concepts['Id_courses']==Id_courses]

    print(f"""
#################### Please select the Id_Concepts ####################
{Concepts[['Id_concept','concept_name']]} 
-1. Back to general menu          
              """)
    valid=list(Concepts.Id_concept.unique())
    valid.append(-1)
    Id_concept=input_validate('Id_concept', valid)
    if Id_concept==-1:
       add_view_GM()
    print(f"""
#################### do you want to add view ####################          
1. All the concept {Concepts[Concepts['Id_concept']==Id_concept].reset_index(drop=True)['concept_name'][0]}
2. Just a part
              """)
    valid=[1,2]
    action2=input_validate('Action', valid)
    if action2==1:
        note=input('Add note: ')     
        viewed_Concept(Id_concept, note)
        print('Successfully added')
    else:
        add_view_Content(Id_concept)
    

def add_view_course(level_id):
    Courses_level=pd.read_csv('D:/2020-02/Platzi/Meta/'+'Courses_level'+'.csv',index_col=0)   
    Courses_level=Courses_level[Courses_level['Id_level']==level_id]
    del Courses_level['Id_level']
    Courses=pd.read_csv('D:/2020-02/Platzi/Meta/'+'Courses_Base'+'.csv',index_col=0)   
    Courses=pd.merge(Courses_level,Courses)
    print(f"""
#################### Please select the Id_courses ####################
{Courses[['Id_courses','courses_names']]} 
-1. Back to general menu          
              """)
    valid=list(Courses.Id_courses.unique())
    valid.append(-1)
    Id_courses=input_validate('Id_courses', valid)
    if Id_courses==-1:
       add_view_GM()
    print(f"""
#################### do you want to add view ####################          
1. All the course {Courses[Courses['Id_courses']==Id_courses].reset_index(drop=True)['courses_names'][0]}
2. Just a part
              """)
    valid=[1,2]
    action2=input_validate('Action', valid)
    if action2==1:
        note=input('Add note: ')     
        viewed_Courses(Id_courses,note)
        print('Successfully added')
    else:
        add_view_Concept(Id_courses)


def multiple_one_courses(Id_level):
    print("""
######################### please select  ########################
Select:
    -1. If you want to go out
    1. If you want to add multiple courses
    2. If you want to add more specific content.
          """)
    action1=input_validate('Action ', [-1,1,2])
    if action1==-1:
        raise SystemExit
    elif  action1==2:
        add_view_course(Id_level)
    else:
        Courses_level=pd.read_csv('D:/2020-02/Platzi/Meta/'+'Courses_level'+'.csv',index_col=0)   
        Courses_level=Courses_level[Courses_level['Id_level']==Id_level]
        del Courses_level['Id_level']
        Courses=pd.read_csv('D:/2020-02/Platzi/Meta/'+'Courses_Base'+'.csv',index_col=0)   
        Courses=pd.merge(Courses_level,Courses)
        print(f"""
#################### Please select the Id_courses ####################
{Courses[['Id_courses','courses_names']]} 
-1. Back to general menu          
          """)
        valid=list(Courses.Id_courses.unique())
        valid.append(-1)

        inappropriate_Answer=True
        while inappropriate_Answer:
            try:
                clic=input('Id_courses: ')
                clic=clic.split(',')
                clic=[int(x) for x in clic]
                 
                if (len(set(clic).intersection(set(valid)))==len(set(clic))):
                    inappropriate_Answer=False
                else:
                    print('Please select a valid value')
            except:
                 print('Please select a valid value')
                 
        if clic==[-1]:
            add_view_GM()
        else:
            clic=[c for c in clic if c!=-1]
            note=input('Add note: ')
            for c in clic:
                viewed_Courses(c,note)
                            
    
def add_view_GM():
    
    print("""
######################### Welcom to add view ########################
Select:
    -1. If you want to go out
    1. If you want to add new content
          """)
    action1=input_validate('Action ', [-1,1])
    if action1==-1:
        raise SystemExit
    School=pd.read_csv('D:/2020-02/Platzi/Meta/'+'School_Base'+'.csv',index_col=0)   
    print(f"""
#################### Please select the id_School ####################
{School} 
-1. Exit         
          """)
    valid=list(School.Id_School.unique())
    valid.append(-1)
    school_id=input_validate('Id_School', valid)
    if school_id==-1:
        raise SystemExit
    del School
    level_Orig=pd.read_csv('D:/2020-02/Platzi/Meta/'+'Level_Base'+'.csv',index_col=0)   
    level_Orig=level_Orig[level_Orig['Id_School']==school_id]
    print(f"""
#################### Please select the Id_level ####################
{level_Orig} 
-1. Exit          
              """)
    valid=list(level_Orig.Id_level.unique())
    valid.append(-1)
    Id_level=input_validate('Id_level', valid)
    if Id_level ==-1:
        raise SystemExit
    multiple_one_courses(Id_level)
 

