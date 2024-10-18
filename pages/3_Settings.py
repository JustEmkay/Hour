import streamlit as st
import time,json
from http_req import get_all_task,get_pre_task,get_userdata,password_reset,delete_user_req
from forms import age_calc,user_verification_login,logout_function
from datetime import datetime



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


def validate_import(data_keys : list):
    
    if ['predefined', 'task_data'] == data_keys:
        return True
    return False


def list_to_hash(each_pretask : list) -> dict:
    
    
    print(each_pretask)
    return hash(frozenset(each_pretask))



@st.dialog("Delete account")
def delete_account_dialog():
    result = user_verification_login("delete")
    if result:
        with st.status("Sending request to server...", expanded=True) as status:
            time.sleep(2)
            status.update(
                label="Deleting user data", state="running", expanded=False
            )
            time.sleep(1)
            
            result = delete_user_req(st.session_state.auth['userid'],userinput=st.session_state.auth['username'])
                
            if result['status']:
                status.update(
                    label="Deleted user data", state="running", expanded=False
                )
                time.sleep(2)
                
                logout_function()
                status.update(
                    label="Clearing all sessions", state="running", expanded=False
                )
                time.sleep(2)
                status.update(
                    label="Exiting account", state="complete", expanded=False
                )
                st.rerun()
                
            else:
                status.update(
                    label=f"{result['status']}", state="error", expanded=False
                )
                
              
@st.dialog("Verify & Download")
def export_dialog():
    result = user_verification_login("export")
    alert = st.empty()
    if result:
        export_task_data = get_all_task(st.session_state.auth['userid'])
        export_type_data = get_pre_task(st.session_state.auth['userid'])
        
        if export_task_data and export_type_data:
            
            export_user_data = create_export_json(export_task_data,export_type_data)
            json_data : json = json.dumps(export_user_data,indent=11)
            
            st.download_button(
                label="Download JSON 📩",
                file_name="data.json",
                mime="application/json",
                data=json_data,
                use_container_width=True,
                type='primary'
            )

@st.dialog("change password",width='large')
def change_password():
    
    verify_col, pass_col2 = st.columns(2)
    placeholder = verify_col.empty()
    with placeholder.container(border=True):
        result = user_verification_login("change_password")
    
    password = pass_col2.text_input("Enter new password:",
                                    disabled=not result,
                                    type='password')
    rpassword = pass_col2.text_input("Re-Enter new password:",
                                     disabled=not result,
                                     type='password')

    if pass_col2.button('change password',use_container_width=True,
                        disabled=not result):    
        if password == rpassword:
            result = password_reset(st.session_state.auth['userid'],password)
            if result:
                if result['status']:
                    st.success(result['message'],icon="✅")
                    time.sleep(2)
                    
                    
                    
                    
                    
                    
                else:
                    st.error(result['message'],icon="❌")
                    
    
    

def settings_page() -> None:
    
    try:
    
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


            # _______________PROFILE MENU_______________
            with st.expander("User Profile",expanded=True):
                with st.container(border=True):
                    
                    udata = get_userdata(st.session_state.auth['userid'],
                                st.session_state.auth['username'],'all')
                    if udata['status']:
                    
                        st.write(f"Username: {udata['data']['username']}")
                        st.write(f"Email: {udata['data']['email']}")
                        st.write(f"Date of birth: {datetime.fromtimestamp(udata['data']['dob']).strftime('%d/%m/%Y')} \
                                | {age_calc(datetime.fromtimestamp(udata['data']['dob']).date())}" )
            
                        t_obj =  datetime.strptime(udata['data']['created_date'], "%Y-%m-%d %H:%M:%S.%f")
                        st.write(f'Account created on: {t_obj.strftime("%d/%m/%Y %I:%M:%S %p")}')
                        
                        blnk_col1, bttn_col2 = st.columns([3,1])
                        
                        if bttn_col2.button('Delete Account',use_container_width=True):
            
                            delete_account_dialog()

                    
                    else:
                        st.error(udata['message'])
                        
            # _______________IMPORT MENU_______________
            with st.expander("Import",expanded=False):
                st.info("Pardon me. I'm bit lazy to code import function")
                # upload_file = st.file_uploader("choose your Back-up file",type=['json'])
                # if upload_file is not None:
                #     # st.write(upload_file)
                
                #     str_upload_file = upload_file.read().decode('utf-8').replace("'", '"')
                #     backup_data = json.loads(str_upload_file)

                    
                #     if validate_import([i for i in backup_data]):
                        
                #         with st.container(border=True):
                #             st.write(backup_data['predefined'])
                            
                #             predefined = [[x['typeID'],x['task_title'],x["task_description"],
                #                             x["task_type"],x["priority"],x["urgent"],
                #                             x["created_date"]] for x in backup_data['predefined']]
                #             st.write(predefined)
                #             if st.button("upload"):
                #                 upload_task_data(st.session_state.auth['userid'],'pre',predefined)
                                
                                
                                
                        
                #         with st.container(border=True):
                #             st.write(backup_data['task_data'])
                    
                #     else:
                #         st.warning('invalid backup file',icon='⚠')
                            
            # _______________EXPORT MENU_______________
            with st.expander("Export",expanded=False):
                
                st.caption("Export all your task_data as JSON")
                export_alert_col, export_bttn_col = st.columns([3,1],vertical_alignment='center')
                exp_alert = export_alert_col.empty()
                exp_alert.info("user should verify before to download backup",icon="👮‍♂️")
                if export_bttn_col.button('Verify & Download',key="export_bttn",
                                       use_container_width=True):
                    export_dialog()    
                
                
                
                
                # username = st.text_input("Enter username/email")
                # password = st.text_input("Enter password",type='password')
                
                # val_alert_col, verify_bttn = st.columns([0.7,0.3],vertical_alignment='center')
                # val_alert = val_alert_col.empty()
                
                # if verify_bttn.button("Verify user",type='primary',
                #                     use_container_width=True):
                #     val = validate_user(userinput=username,password=password)
                #     # st.write(val)
                #     if val['status']:
                #         if st.session_state.auth['userid'] == val['user_data']['userid']:
                            
                #             val_alert.success("user verified",icon="✅")
                #             export_task_data = get_all_task(val['user_data']['userid'])
                #             export_type_data = get_pre_task(val['user_data']['userid'])
                            
                            
                #             if export_task_data and export_type_data:
                                
                #                 export_user_data = create_export_json(export_task_data,export_type_data)
                #                 json_data : json = json.dumps(export_user_data,indent=11)
                                
                #                 st.download_button(
                #                     label="Download JSON",
                #                     file_name="data.json",
                #                     mime="application/json",
                #                     data=json_data,
                #                 )
                
            # _______________Security_______________
            with st.expander("Security/Password",expanded=False):
                if st.button('chnage pass'):
                    change_password()
                
    except Exception as e:
        print("Error:",e)        
                     
    
if __name__ == '__main__' :
    
    try:
        settings_page()
    except:
        st.switch_page('Home.py')