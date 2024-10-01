import streamlit as st
import time,requests
from datetime import datetime
from forms import create_task_dialog
from Home import API_URL



def task_page() -> None:
    
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
        
        alert_col.info(f"Today: {datetime.today().date()}")
        bttn_col1.button('delete',use_container_width=True)
        if bttn_col2.button('create',use_container_width=True):
            create_task_dialog()    
        
        col1, col2 = st.columns([0.3,0.7])
        
        
        with col1.container(border=True,height=105):
            st.metric(':green[important urgent]',
                      value=45,
                      help='Task is both important and urgent')
        with col1.container(border=True,height=105):
            st.metric(':green[important] :red[urgent]',
                      value=45,
                      help='Task is important but not urgent')
        with col1.container(border=True,height=105):
            st.metric(':red[important] :green[urgent]',
                      value=45,
                      help='Task is not important but urgent')
        with col1.container(border=True,height=105):
            st.metric(':red[important urgent]',
                      value=45,
                      help='Task is both not important and not usrgent')
        
        with col2.container(border=True,height=470):
            ...
        

    
if __name__ == '__main__' :
    
    try:
        task_page()
    except:
        st.switch_page('Home.py')