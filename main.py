import streamlit as st
from datetime import datetime,time
import time
import calendar


if "task" not in st.session_state:st.session_state.task=[]
if "week_time_have" not in st.session_state:st.session_state.week_time_have=10080
if "current_week" not in st.session_state:st.session_state.current_week=datetime.now().isocalendar()[1]
if "current_weekday" not in st.session_state:st.session_state.current_weekday=datetime.now().isocalendar()[2]

def experiment():
    print("experiment function working.")

def unixtodate():
    print("convert to date")

def unixtotime(ut):
    dt_object = datetime.fromtimestamp(ut)
    formatted_time = dt_object.strftime(' %I:%M:%S')
    return formatted_time

def min_notify():
    print("notify working")
    if st.session_state.selected_min >= 1440:
        st.toast(":red[**Selected Time is over 24hr!!**] ",icon='⚠️')

def main():
    with st.sidebar:
        st.header("Welcome To Weekly 🕐.")
        st.caption("Here you can assisgn your tasks based on Time you have")
        progrs=int(((st.session_state.week_time_have/60)/168)*100)        
        day_progrs=00
        tbar=st.progress(progrs,text=f"This Week : {(st.session_state.week_time_have//60)}Hr Left Out of 168Hr")
        daybar=st.progress(day_progrs,text=f"Today : {day_progrs}Hr/24Hr")

        st.session_state.week_time_have//60
        for x in st.session_state.task:
            x['minutes']//60
    
    st.header("Write your weekly tasks !")
    tbp=int((st.session_state.week_time_have/10080)*100)
    time_bar=st.progress(tbp,text=f"**Time Left:** :red[{st.session_state.week_time_have}] Out of :green[10080] Minutes")
    st.info(f"Date : {datetime.now().date()} | Week : {datetime.now().isocalendar()[1]} | Weekday : {datetime.now().isocalendar()[2]}")
    st.divider()
    text=st.text_input("Write here:",key="exptext",on_change=experiment)
    col1,col2=st.columns(2)
    date_selected=col1.date_input("Select Date:",help=":gray[Cannot Select past months.]",format="DD/MM/YYYY",value="today")
    total_time=st.session_state.week_time_have
    # time_slider=col2.slider("Select time needed to finish the task:",max_value=total_time,step=5)
    

    time_input=col2.number_input(f"Select how much time needed to finish this task{()}:",max_value=total_time,on_change=min_notify,key="selected_min",value='min')
    
    
    if date_selected:
        print(date_selected,date_selected.isocalendar())
        selected_date=datetime(date_selected.year,date_selected.month,date_selected.day)
        print(selected_date)
        to_timestamp=datetime.timestamp(selected_date)
        if date_selected == datetime.now().date():
            print("same date")

        else: 
            print("something wrong")
            t=datetime.now() 
            st.write(t.date())
            
        # print("today",datetime.now())
        # this conditon not working?? i dont know why!!
        # if st.session_state.current_week >= date_selected.isocalendar()[1] and date_selected.isocalendar()[2] >= st.session_state.current_weekday : dt_val = True
        # else: dt_val=False
        if int(st.session_state.current_week) <= date_selected.isocalendar()[1]:
            dt_val=True
        else: dt_val=False

    #button disable & Error 
    if text and dt_val:activate,hactivate=False,"Press to add task."
    else: activate,hactivate=True,":red[Error? Maybe you tried to add a blank task OR Tried to add task from past!]"
    addtask=st.button("Add Task.",use_container_width=True,disabled=activate,help=hactivate)
    
    if addtask: #Add task
        dict={"description":text,"done":False,"minutes":time_input,"for":to_timestamp,"added_on":int(datetime.timestamp(datetime.now()))}
        try:
            st.session_state.task.append(dict)
            st.session_state.week_time_have=10080-int(time_input)
            if date_selected == datetime.now().date:
                print("same date")
            print("Added data")
        except:print("Some type of error.")
        finally:st.rerun()
    
    if not st.session_state.task:st.info("List is Empty.")
    
    st.divider()
    

    #display tasks
    st.subheader("Tasks Pending:")
    st.caption("Thses are the tasks you have to finish you Lazy")
    for j,tasks in enumerate(st.session_state.task):
        if tasks["done"]==False or tasks["done"]=="false":
            done_task=st.checkbox(f"Added on: :green[{unixtotime(tasks['added_on'])}] | ***{tasks['description']}***",key=j,help=":red[Dude stop procrastinating and do your work.]🤦‍♀️")
            if done_task:
                st.session_state.task[j]["done"]=True
                st.rerun()

        if tasks["done"]==True or tasks["done"]=="true":
            undone_task=st.checkbox(f":gray[Added on: :green[{unixtotime(tasks['added_on'])}] | ~***{tasks['description']}***~]",value=True)
            if not undone_task:
                st.session_state.task[j]["done"]=False
                st.rerun()
    
    st.divider()
    clear=st.button("Clear All")
    if clear:
        st.session_state.task=[]
        st.session_state.week_time_have=10080
        st.rerun()

    st.session_state
    # print((calendar.monthcalendar(datetime.now().year,datetime.now().month)))

if __name__ == "__main__":
    main()