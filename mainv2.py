import streamlit as st
from datetime import datetime
import time

st.title("Task Manager")

# Create a list to store tasks in streamlit session_state
if "task" not in st.session_state: st.session_state.task=[]
if "task_count" not in st.session_state:st.session_state.task_count=[0,0]


current_time = datetime.now().strftime("%I:%M:%S")
current_timestamp = datetime.timestamp(datetime.now()) 


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
    col4,col5=st.columns(2)
    date_input=col4.date_input("Date",label_visibility="collapsed")
    add_task=col5.button("Add task",use_container_width=True)
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

    tab1,tab2,tab3=st.tabs(["▶️Today","⏪Past","⏩Future"])

    #This tab display only current task
    with tab1:
        for id,txt in enumerate(st.session_state.task):
            if datetime.fromtimestamp(txt['for_date']).date() == datetime.now().date():
                if txt['done'] == False or txt['done'] == "false":        
                    check=st.checkbox(f"Added on: :green[*{datetime.fromtimestamp(txt['added_date']).date()}*] | Task: :red[*{txt['dsptn']}*] | For: {datetime.fromtimestamp(txt['for_date']).date()} | Status: :gray[{txt['done']}]",key=id)
                    if check:
                        st.session_state.task[id]['done']=True
                        st.rerun()
                if txt['done'] == True or txt['done'] == "true":
                    uncheck=st.checkbox(f"~Task: :red[*{txt['dsptn']}*] | Status: :gray[{txt['done']}]~",value=True)
                    if not uncheck:
                        st.session_state.task[id]['done']=False
                        st.rerun()
    
    #This tab display pedding task from past :(
    with tab2:
        slct1=st.multiselect("Tasks From past:", ["milk", "apples", "potatoes"])
        
        if len(slct1)==0:
            st.write("Show all past tasks")
        else:
            slct1

    #This tab display task for Future :)
    with tab3:
        slct2=st.multiselect("Tasks From future:", ["milk", "apples", "potatoes"])
        if len(slct2)==0:
            st.write("Show all future tasks")
        else:
            slct2

    st.divider()
    clear_task=st.button("Clear all")
    if clear_task:
        st.session_state.task=[]
        st.session_state.task_count=[0,0]
        st.rerun()

    st.session_state


if __name__ == "__main__":
    main()