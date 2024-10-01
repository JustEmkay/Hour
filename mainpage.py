import streamlit as st
from datetime import datetime,date
from forms import create_task_dialog
import requests
from Home import API_URL

today_timestamp : int = int(datetime(datetime.now().year,datetime.now().month,
                                     datetime.now().day,0,0,0).timestamp())

@st.cache_data(ttl='1d')
def being_alive(dob_stamp) -> list:
    
    alive_days = datetime.now() - datetime.fromtimestamp(dob_stamp)
    diff_month = (datetime.now().year - datetime.fromtimestamp(dob_stamp).year) * 12 + datetime.now().month - datetime.fromtimestamp(dob_stamp).month
    return [alive_days,diff_month]


def load_todays_task(uid) -> dict:
    req = requests.get(API_URL + f'task/today/{uid}/{today_timestamp}')
    res = req.status_code
    if res == 200:
        return req.json()

    
def mainpage() -> None:
    
    result = load_todays_task(st.session_state.auth['userid'])
    
    title_col, counter_col = st.columns([0.7,0.3],vertical_alignment='top')
    title_col.title(f"Welcome {st.session_state.auth['username']} !",
             anchor=False)
    title_col.divider()
    
    with title_col.container(border=True,height=400):
        st.caption("today's tasks:")
        st.write('--Empty--')
        if st.button('create task'):
            create_task_dialog()
    
    
    alive_counter = being_alive(st.session_state.auth['dob'])
    counter_col.metric(label="Being Alive",
                       value=f"{alive_counter[0]} days",
                       delta=f"{alive_counter[1]} months")
    
    year_counter = [0,0]
    counter_col.metric(label="Streak",
                    value=f"Streak: {year_counter[0]} 🔥",
                    label_visibility='collapsed')
  
    