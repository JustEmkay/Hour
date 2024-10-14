import streamlit as st
import time,json
from http_req import validate_user,get_all_task,get_pre_task


def create_export_json(export_task_data,export_type_data) -> dict:
    temp_task : dict = {}
    temp_task_data : list[dict] = []

    for data in export_task_data['data']:
        temp_task = {
            "type_id" : data[2],
            "title" : data[3],
            "description":data[4],
            "type" : data[5],
            "priority": data[6],
            "urgent" : data[7],
            "status" : data[8],
            "created_date": data[9]
        }
        
        temp_task_data.append(temp_task)
        
    temp_task_type_data : list[dict] = []
    for data in export_type_data['data']:
        temp_task = {
            "typeID" : data[0],
            "task_title" : data[2],
            "task_description":data[3],
            "task_type" : data[4],
            "priority": data[5],
            "urgent" : data[6],
            "created_date": data[7]
        }
        
        temp_task_type_data.append(temp_task)
        
    return {
        "predefined" : temp_task_type_data,
        "task_data" : temp_task_data
    }


def settings_page() -> None:
    
    st.title('Settings',anchor=False)
    st.divider()
    
    if not st.session_state.auth['authorization'] and \
    not st.session_state.auth['userid']:
   
        alert = st.empty()
        for i in range(10):
            time.sleep(0.5)
            alert.caption(f'Please login. Forwading to login page in {10-i}s')
        st.switch_page('Home.py')
    
    elif st.session_state.auth['authorization'] and \
    st.session_state.auth['userid']:

        with st.expander("Import",expanded=True):
            ...
    

        with st.expander("Export",expanded=True):
            username = st.text_input("Enter username/email")
            password = st.text_input("Enter password",type='password')
            
            val_alert_col, verify_bttn = st.columns([0.7,0.3],vertical_alignment='center')
            val_alert = val_alert_col.empty()
            
            if verify_bttn.button("Verify user",type='primary',
                                  use_container_width=True):
                val = validate_user(userinput=username,password=password)
                # st.write(val)
                if val['status']:
                    if st.session_state.auth['userid'] == val['user_data']['userid']:
                        val_alert.success("user verified",icon="✅")
                        export_task_data = get_all_task(val['user_data']['userid'])
                        export_type_data = get_pre_task(val['user_data']['userid'])
                        
                        
                        if export_task_data and export_type_data:
                            
                            export_user_data = create_export_json(export_task_data,export_type_data)
                            

                        
                            json_data : json = json.dumps(export_user_data,indent=11)
                            
                            st.download_button(
                                label="Download JSON",
                                file_name="data.json",
                                mime="application/json",
                                data=json_data,
                            )
                     
    
if __name__ == '__main__' :
    
    try:
        settings_page()
    except:
        st.switch_page('Home.py')