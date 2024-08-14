import streamlit as st
from datetime import datetime
import json


if "d_time" not in st.session_state: st.session_state.d_time = 24
if "prgrs_time" not in st.session_state: st.session_state.prgrs_time = 100
if "time_management" not in st.session_state: st.session_state.time_management=[]

def  update_time(time_hr_min,title):
    if time_hr_min != 0 :
        prgrs_percntg= (time_hr_min/st.session_state.d_time)*100
        st.session_state.prgrs_time =  int(st.session_state.prgrs_time - prgrs_percntg)
        data={"Title":title,"mTime":time_hr_min}
        
        try: 
            st.session_state.time_management.append(data)
            st.rerun()
        except:
            print("Error.....")

def time_convert(t):
    if t!=0:
        time_hr_min= float(t/60)
        time_hr=int(time_hr_min)
        time_min=t%60
        return time_hr_min,time_hr,time_min,f"You selected {time_hr} Hr {time_min} Min"
    else:return 0,0,0,f"You selected 0 Hr 0 Min"

def main():
    if "time_management" not in st.session_state:
        st.session_state.time_management = []

    st.header("Time management ⌛")
    st.divider() #~~~~~~~~~~~~~~

    col1,col2=st.columns(2)

    col1.progress(value= st.session_state.prgrs_time,text=f"{100 - st.session_state.prgrs_time}% of time used, {st.session_state.prgrs_time}% Left ")
    col1.divider()#~~~~~~~~~~~~~~

    jitem=json.loads(st.session_state.time_management)
    print(jitem)

    for i,item in enumerate(st.session_state.time_management):
        # col1.progress(text=f"{st.session_state.time_management[i]['Title']}",value=st.session_state.time_management[i]['mTime'])
        col1.progress( text=f"{item}",value=50 )
    
    title=col2.text_input("Enter the title name")
    title
    t=col2.number_input("Select how much time you need to finish that task ( in minutes )",step=1,min_value=0)
    col2.info(time_convert(t)[3])

    bt1,bt2=col2.columns(2)
    if bt1.button("Reset all",use_container_width=True):
        st.session_state.prgrs_time = 100
        st.session_state.time_management = []
        st.rerun()

    if bt2.button("add",use_container_width=True):
        # update_time(time_convert(t)[0])
        if title and t:
            update_time(time_convert(t)[0],title)
        else: col2.error("fill all inputs!!")

    st.session_state

if __name__ == "__main__":
    main()
