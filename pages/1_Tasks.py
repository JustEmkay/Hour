import streamlit as st
import time
from datetime import datetime
from forms import create_task_dialog,delete_task_dialog,timestamp_to_date,edit_task
from http_req import get_all_task,today_timestamp


def filter_task_data(option:str, data:list) -> list:
    result : list[list] = []

    if option == 'current':
        for x in data:
            if x[9] == today_timestamp:
                result.append(x)
        return result
        
    elif option == 'all':
        return data
    
    else:    
        for x in data:
            if x[5] == option:
                result.append(x)
        return result

def task_page() -> None:
    
    allTask = get_all_task(st.session_state.auth['userid'])
    
    st.header('Task Manager',anchor=False,divider=True)
    
    if not st.session_state.auth['authorization'] and \
    not st.session_state.auth['userid']:
   
        alert = st.empty()
        for i in range(10):
            time.sleep(0.5)
            alert.caption(f'Please login. Forwading to login page in {10-i}s')
        st.switch_page('Home.py')
    
    else:    
        alert_col, bttn_col1, bttn_col2 = st.columns([2,1,1])
        
        filter_opt : str = alert_col.selectbox('filter',['all','current','once','daily','monthly','yearly'],
                            label_visibility='collapsed')
         
        filtered_task : list = filter_task_data(filter_opt,allTask['data'])
        
        ImpUrg : list = []
        ImpNUrg : list = []
        NImpNUrg: list = []
        NImpUrg : list = []
        
        for i in filtered_task:
            # index 7 is priority , index 8 is urgent   
            if i[6] and i[7]: # filter ids of important urgent
                ImpUrg.append(i[0])
            elif i[6] and not i[7]: # filter ids of important not urgent
                ImpNUrg.append(i[0])
            elif not i[6] and not i[7]: # filter ids of not important not urgent
                NImpNUrg.append(i[0])
            elif not i[6] and i[7]: # filter ids of not important urgent
                NImpUrg.append(i[0])
        
    
        
        if bttn_col1.button('delete',use_container_width=True):
            delete_task_dialog()
        
        if bttn_col2.button('create',use_container_width=True):
            create_task_dialog()    
        
        col1, col2 = st.columns([0.3,0.7])
        
        
        with col1.container(border=True,height=105):
            st.metric(':green[important urgent]',
                      value=len(ImpUrg),
                      help='Task is both important and urgent')
            
        with col1.container(border=True,height=105):
            st.metric(':green[important] :red[urgent]',
                      value=len(ImpNUrg),
                      help='Task is important but not urgent')
        
        with col1.container(border=True,height=105):
            st.metric(':red[important] :green[urgent]',
                      value=len(NImpUrg),
                      help='Task is not important but urgent')
        
        with col1.container(border=True,height=105):
            st.metric(':red[important urgent]',
                      value=len(NImpNUrg),
                      help='Task is both not important and not usrgent')
        
        with col2.container(border=True,height=470):
        
    
            filtered_date : list[int] = []
            for x in filtered_task:
                if x[9] not in filtered_date:
                    filtered_date.append(x[9])


            for y in filtered_date:
                
                with st.container(border=True):
                    
                    if y == today_timestamp:
                        str_date = f'**:green[| {timestamp_to_date(y)}]** ⤵️'
                    else:
                        str_date = f':grey[| {timestamp_to_date(y)}] ⤵️'
                        
                    st.write(str_date)  
                    for z in filtered_task:
                        if z[9] == y:
                            
                            title = f'{z[3]}'
                            if z[8]:          
                                title = f'~~:grey[{z[3]}]~~'
                            if st.checkbox(title,key=z[0]): #diplay option: [edit,delete]
                                st.write(f'| :grey[descr:] {z[4]} ')
                                blnk, edt_bttn, del_bttn = st.columns([2,1,1])
                                del_bttn.button('delete',key=f'{z[0]}d',
                                                use_container_width=True)
                                if edt_bttn.button('edit',key=f'{z[0]}e',
                                                use_container_width=True):
                                    edit_task(z)
                        
                
                
    
    
if __name__ == '__main__' :
    
    try:
        task_page()
    except:
        st.switch_page('Home.py')