import streamlit as st
from datetime import datetime
import time

st.title("Task Manager")

# Create a list to store tasks in streamlit session_state
if "task" not in st.session_state: st.session_state.task=[]
if "task_count" not in st.session_state:st.session_state.task_count=[0,0]
if "today" not in st.session_state:st.session_state.today=[0,0,0]

# Getting Today's Year,Week,Weekday to variable and session_tate_today
st.session_state.today[0]=y=datetime.isocalendar(datetime.now())[0]
st.session_state.today[1]=w=datetime.isocalendar(datetime.now())[1]
st.session_state.today[2]=wd=datetime.isocalendar(datetime.now())[2]
# print(y,w,wd)

current_time = datetime.now().strftime("%I:%M:%S")
current_timestamp = datetime.timestamp(datetime.now())
cyear,cmonth,cday=datetime.now().year,datetime.now().month,datetime.now().day


def main():
    #task counts
    total_task_count=len(st.session_state.task)
    dc,ndc=0,0
    for x in st.session_state.task:
        if x['done']==False:
            ndc=ndc+1

        if x['done']==True:
            dc=dc+1

    # Display the current time
    st.info(f"Current Time: {current_time} | Current Timestamp: {current_timestamp}") 
    col1,col2,col3=st.columns(3)
    col1.info(f"_Total Task:_ {total_task_count}",icon="📝")
    col2.info(f"_Completed:_ {dc}",icon="✔️")
    col3.info(f"_Not-Compeleted:_ {ndc}",icon="❌")
    st.divider()

    task_input=st.text_input("Write here:")
    if task_input:
        disable=False
    else:
        disable=True
    col4,col5=st.columns(2)
    date_input=col4.date_input("Date",label_visibility="collapsed")
    add_task=col5.button("Add task",use_container_width=True,disabled=disable)
    if add_task:
        add={'dsptn':task_input,'done':False,'for_date':datetime.timestamp(datetime(date_input.year,date_input.month,date_input.day)),'added_date':int(datetime.timestamp(datetime.now()))}
        try:
            st.session_state.task.append(add)
            print("Added...")
        except:
            print("something wrong")
        finally:
            st.rerun()


    st.divider()
    # st.session_state
    tab1,tab2,tab3=st.tabs(["▶️Today","⏪Past","⏩Future"])

    
    #This tab display only current task
    with tab1:
        st.write("today list")
        for id,txt in enumerate(st.session_state.task):
            done=st.checkbox(txt['dsptn'])


    #This tab display pedding task from past :(
    with tab2:
        st.write("Show all past tasks.")

    #This tab display task for Future :)
    with tab3:
        st.write("Show all future tasks")


    st.divider()
    clear_task=st.button("Clear all")
    if clear_task:
        st.session_state.task=[]
        st.session_state.task_count=[0,0]
        st.rerun()

    st.session_state


if __name__ == "__main__":
    main()