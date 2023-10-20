import streamlit as st
from datetime import datetime
import time

url="https://www.linkedin.com/in/manukrishna-t-m/"

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


#past_date_validation
def past_val(past):
    if past[0]<=st.session_state.today[0]:
        if past[1]==st.session_state.today[1]:
            if past[2]<st.session_state.today[2]:
                return True
        if past[1]<st.session_state.today[1]:
            return True

#future_date_validation
def future_val(future):
    if future[0]>=st.session_state.today[0]:
        if future[1]==st.session_state.today[1]:
            if future[2]>st.session_state.today[2]:
                return True
        if future[1]>st.session_state.today[1]:
            return True
        
#tab information
def tab_info(tab_pass):
    if tab_pass[1] == 0:
        return ":green[***Look like you finsided All Your tasks 🎈👏***]"
    elif tab_pass[0] == 0 :
        return f":red[**Damn you'r super lazy!!🤦‍♀️**]"
    else:
        return f"💁‍♀️ :green[**{tab_pass[0]}**] Task completed 👏 :red[**{tab_pass[1]}**] More Left to be completed. "


def main():
    st.title("Literaly A Task Manager")
    with st.sidebar:
        st.title("Welcome To Weekly📅")
        st.markdown("Hello 🙋‍♂️ I'm [Manu](%s) weekly is a simple task manager web application \
                    written made using Streamlit."%url)
        st.caption("")

    #task counts
    total_task_count=len(st.session_state.task)
    dc,ndc=0,0
    for x in st.session_state.task:
        if x['done']==False:
            ndc=ndc+1

        if x['done']==True:
            dc=dc+1

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
    #Display Tasks in tabs
    tab1,tab2,tab3=st.tabs(["▶️Today","⏪Past","⏩Future"])
    
    cd,ncd=0,0 
    tab_pass=[0,0]
    #This tab display only current task
    with tab1:
        for id,txt in enumerate(st.session_state.task):
            today_date_check=datetime.isocalendar(datetime.fromtimestamp(txt['for_date']).date())
            # print(today_date_check)
            if today_date_check[0] == st.session_state.today[0] and today_date_check[1] == st.session_state.today[1] and today_date_check[2] == st.session_state.today[2]:
                if txt['done']==False:
                    ncd+=1
                    done=st.checkbox(f":green[{datetime.fromtimestamp(txt['for_date']).date()}] | **{txt['dsptn']}** ",help=f"Added on:{datetime.fromtimestamp(txt['for_date']).date()}")
                    if done:
                        st.session_state.task[id]['done']=True
                        st.rerun()
                if txt['done']==True:
                    cd+=1
                    not_done=st.checkbox(f"~:gray[{datetime.fromtimestamp(txt['for_date']).date()} | {txt['dsptn']}]~",help=f"Added on:{datetime.fromtimestamp(txt['for_date']).date()}",value=True)
                    if not not_done:
                        st.session_state.task[id]['done']=False
                        st.rerun()
            tab_pass[0]=cd
            tab_pass[1]=ncd
        st.caption(f"{tab_info(tab_pass)}")
        tab_pass=[0,0]
        cd,ncd=0,0
        
    #This tab display pedding task from past :(
    with tab2:
        for id1,txt1 in enumerate(st.session_state.task):
            past_date_check=datetime.isocalendar(datetime.fromtimestamp(txt1['for_date']).date())
            if past_val(past_date_check):
                if txt1['done']==False:
                    ncd+=1
                    done1=st.checkbox(f":green[{datetime.fromtimestamp(txt1['for_date']).date()}] | **{txt1['dsptn']}** ",help=f"Added on:{datetime.fromtimestamp(txt1['for_date']).date()}")
                    if done1:
                        st.session_state.task[id1]['done']=True
                        st.rerun()
                if txt1['done']==True:
                    cd+=1
                    not_done1=st.checkbox(f"~:gray[{datetime.fromtimestamp(txt1['for_date']).date()} | {txt1['dsptn']}]~",help=f"Added on:{datetime.fromtimestamp(txt1['for_date']).date()}",value=True)
                    if not not_done1:
                        st.session_state.task[id1]['done']=False
                        st.rerun()
            tab_pass[0],tab_pass[1]=cd,ncd
        st.caption(f"{tab_info(tab_pass)}")
        tab_pass=[0,0]
        cd,ncd=0,0

    #This tab display task for Future :)
    with tab3:
        for id2,txt2 in enumerate(st.session_state.task):
            future_date_check=datetime.isocalendar(datetime.fromtimestamp(txt2['for_date']).date())
            if future_val(future_date_check):
                if txt2['done']==False:
                    done2=st.checkbox(f":green[{datetime.fromtimestamp(txt2['for_date']).date()}] | **{txt2['dsptn']}**",help=f"added on :red[{datetime.fromtimestamp(txt2['added_date']).date()}]")
                    ncd+=1
                    if done2:
                        st.session_state.task[id2]['done']=True
                        st.rerun()
                if txt2['done']==True:
                    not_done2=st.checkbox(f"~:gray[{datetime.fromtimestamp(txt2['for_date']).date()} | {txt2['dsptn']}]~",help=f"added on :red[{datetime.fromtimestamp(txt2['added_date']).date()}]",value=True)
                    cd+=1
                    if not not_done2:
                        st.session_state.task[id2]['done']=False
                        st.rerun()
            tab_pass[0]=cd
            tab_pass[1]=ncd
        st.caption(f"{tab_info(tab_pass)}")
        tab_pass=[0,0]
        cd,ncd=0,0    
    
    st.divider()
    

    cd,ncd=0,0  
    # clear all task button
    clear_task=st.button("Clear all")
    if clear_task:
        st.session_state.task=[]
        st.session_state.task_count=[0,0]
        st.rerun()

    # st.session_state


if __name__ == "__main__":
    main()