import streamlit as st
from datetime import datetime
from forms import create_task_dialog,task_view
from http_req import load_todays_task

def being_alive(dob_stamp) -> list:
    
    alive_days = datetime.now() - datetime.fromtimestamp(dob_stamp)
    diff_month = (datetime.now().year - datetime.fromtimestamp(dob_stamp).year) * 12 + datetime.now().month - datetime.fromtimestamp(dob_stamp).month
    return [alive_days.days,diff_month]
    
def mainpage() -> None:
    if not st.session_state.task_data:
        result = load_todays_task(st.session_state.auth['userid'])
        st.session_state.task_data = result['data']
    
    st.title(f"Welcome {st.session_state.auth['username']} !",
             anchor=False)
    title_col, counter_col = st.columns([0.7,0.3],vertical_alignment='top')
    
    with title_col.container(border=True,height=400):
        col1, col2 = st.columns([0.7,0.3])
        col1.caption("today's tasks:")
        if col2.button('add task',use_container_width=True):
            create_task_dialog()
            
        if st.session_state.task_data:
            task_view()
        else:
            st.write('--Empty--')
    
    alive_counter = being_alive(st.session_state.auth['dob'])
    counter_col.metric(label="Being Alive",
                       value=f"{alive_counter[0]} days",
                       delta=f"{alive_counter[1]} months")
    
    year_counter = [0,0]
    counter_col.metric(label="Streak",
                    value=f"Streak: {year_counter[0]} 🔥",
                    label_visibility='collapsed')
  
    