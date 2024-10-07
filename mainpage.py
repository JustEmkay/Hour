import streamlit as st
from datetime import datetime
from forms import create_task_dialog,task_view
from http_req import load_todays_task,today_timestamp,get_streak_score

def being_alive(dob_stamp : int) -> list:
    
    alive_days = datetime.now() - datetime.fromtimestamp(dob_stamp)
    diff_month = (datetime.now().year - datetime.fromtimestamp(dob_stamp).year) * 12 + datetime.now().month - datetime.fromtimestamp(dob_stamp).month
    return [alive_days.days,diff_month]

def streak_counter(uid : str) -> dict:
    result : list = get_streak_score(uid)
    print("result:",result)
    
    filter_result : list[int] = [1 if x >= 50 else 0 for x in result['data']]
    
    count = 0
    streak_list : list = []
    for idx,i in enumerate(filter_result,start=1):
        if i:
            count +=1
        if not i:
            if count != 0:
                streak_list.append(count)
            count = 0
        if idx == len(filter_result):
            streak_list.append(count)
            count 
    
    return {
        'current_percentage' : result['data'][-1],
        'current_streak' : streak_list[-1],
        'max_streak' : max(streak_list),
    }


    
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

    year_counter = [0,0]
    with counter_col.container(border=True):
        result = streak_counter(st.session_state.auth['userid'])
        st.metric(label="Streak",
                        value=f" {result['current_streak']}🔥",
                        delta=f"{result['max_streak']}",
                        help="streak is added when you finish 50% of thats day's task")

    with counter_col.container(border=True):
        alive_counter = being_alive(st.session_state.auth['dob'])
        st.metric(label="Being Alive",
                        value=f"{alive_counter[0]} days",
                        delta=f"{alive_counter[1]} months")
    
    with counter_col.container(border=True):
        st.metric(label="MonthEnd",
                        value=f"{year_counter[0]} 📅",
                        )
  
    