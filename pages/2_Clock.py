import streamlit as st 
from datetime import datetime
import requests,time
from creds import API_URL
from http_req import today_timestamp


def show_clock() -> None:
    
    if not st.session_state.auth['authorization'] and \
    not st.session_state.auth['userid']:
   
        alert = st.empty()
        for i in range(10):
            time.sleep(0.5)
            alert.caption(f'Please login. Forwading to login page in {10-i}s')
        st.switch_page('Home.py')
    
    clock = st.empty()
    
    col1, col2 = st.columns([6,4])
    with col1.container(border=True,height=500):
        st.subheader("Today's tasks⤵️",anchor=False)
        
        for idx,col in enumerate(st.session_state.task_data[str(today_timestamp)],start=1):
            if col['status']:
                with st.expander(f":grey[{idx}.{col['task']}]"):
                    st.caption(f"Description: :blue[{col['description']}]")
                    
            if not col['status']:
                with st.expander(f":red[{idx}. {col['task']}]"):
                    st.caption(f"Description: :blue[{col['description']}]")
            
                    
                
    with col2.container(border=True,height=240):
        st.subheader('Monthly📆',anchor=False)

    with col2.container(border=True,height=240):
        st.subheader('Yearly📅',anchor=False)
    
    while 1:
        clock.title(datetime.now().strftime("%A, %B %d, %Y %I:%M:%S %p"),
                    anchor=False)
        time.sleep(1)
    
    
if __name__ == '__main__':
    show_clock()