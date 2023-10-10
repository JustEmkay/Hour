import streamlit as st
from datetime import datetime,date,time


if "task" not in st.session_state:st.session_state.task=[]
if "time_have" not in st.session_state:st.session_state.time_have=10080
if "current_week" not in st.session_state:st.session_state.current_week=datetime.now().isocalendar()[1]
if "current_weekday" not in st.session_state:st.session_state.current_weekday=datetime.now().isocalendar()[2]

def experiment():
    print("experiment function working.")

def unixtodate():
    print("convert to date")

def unixtotime(ut):
    dt_object = datetime.fromtimestamp(ut)
    formatted_time = dt_object.strftime(' %d:%M:%S')
    # print(f"{formatted_date} convert to time")
    return formatted_time

def main():
    with st.sidebar:
        st.header("Welcome To Hourly 🕐.")
        st.caption("Here you can assisgn your tasks based on Hours you have")
        progrs,day_progrs=0,0
        tbar=st.progress(progrs,text=f"{progrs}Hr/168Hr")
        daybar=st.progress(day_progrs,text=f"{day_progrs}Hr/24Hr")
    
    st.header("Write your weekly tasks !")
    tbp=int((st.session_state.time_have/10080)*100)
    time_bar=st.progress(tbp,text=f"**Time Left:** :red[{st.session_state.time_have}] Out of :green[10080] Minutes")
    st.divider()
    text=st.text_input("write here:",key="exptext",on_change=experiment)
    
    col1,col2=st.columns(2)
    date_selected=col1.date_input("Select Date",help="",format="DD/MM/YYYY",value="today")
    total_time=st.session_state.time_have
    # time_slider=col2.slider("Select time needed to finish the task:",max_value=total_time,step=5)
    time_input=col2.number_input("Select how much time needed to finish this task:",max_value=total_time)
    if date_selected:
        print(date_selected.isocalendar())
        dt_obj=datetime.combine(date_selected,time())
        unix_time=datetime.timestamp(dt_obj)
        unix_time
        print("today",datetime.now())
        # this conditon not working?? i dont know why!!
        # if st.session_state.current_week >= date_selected.isocalendar()[1] and date_selected.isocalendar()[2] >= st.session_state.current_weekday : dt_val = True
        # else: dt_val=False
        if int(st.session_state.current_week) <= date_selected.isocalendar()[1]:
            dt_val=True
        else: dt_val=False



    if text and dt_val:activate,hactivate=False,"Press to add task."
    else: activate,hactivate=True,":red[Error? Maybe you tried to add a blank task OR Tried to add task from past!]"
    addtask=st.button("Add Task.",use_container_width=True,disabled=activate,help=hactivate)
    if addtask:
        dict={"description":text,"done":False,"minutes":time_input,"for":unix_time,"added_on":int(datetime.timestamp(datetime.now()))}
        try:
            st.session_state.task.append(dict)
            st.session_state.time_have=10080-int(time_input)
            print("Added data")
        except:print("Some type of error.")
        finally:st.rerun()
    
    if not st.session_state.task:st.info("List is Empty.")
    
    st.divider()
    st.session_state

    #display tasks
    for j,tasks in enumerate(st.session_state.task):
        if tasks["done"]==False or tasks["done"]=="false":
            st.write(f"Added on: :green[{unixtotime(tasks['added_on'])}] | ***{tasks['description']}***")
    st.divider()
    clear=st.button("Clear")
    if clear:
        st.session_state.task=[]
        st.session_state.time_have=10080
        st.rerun()




if __name__ == "__main__":
    main()