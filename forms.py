import streamlit as st 
from datetime import datetime
import re,requests,time
from models import UserRegister,Task
from creds import API_URL
from http_req import *

def age_calc(dob : datetime.date ) -> dict:
    today : datetime.date = datetime.today()
    return today.year - dob.year - ((today.month,today.day) < (dob.month,dob.day))

def validate_email(email):  
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):  
        return True  
    return False


@st.dialog("Register Form")
def register_form() -> None:
    placeholder = st.empty()
    loading_placeholder = st.empty()
    
    with placeholder.container():
        username : str = st.text_input("Enter your username:")
        username_alert = st.empty()
        
        email : str = st.text_input("Enter your email:")
        email_alert = st.empty()
        
        dob_col,age_col = st.columns([0.6,0.4],vertical_alignment='bottom')
        dob : datetime.date = dob_col.date_input("Select you date of birth:",
                                                 min_value=datetime(1940, 1, 1))
        if dob:
            age = age_calc(dob)
            if age < 8:
                age_col.error(f'Year old: {age}',icon='⚠')
            else:
                age_col.success(f'Year old: {age}',icon='✔')
           
        pas_col, repas_col = st.columns(2)        
        password : str = pas_col.text_input("create a password:",type='password')
        repassword : str = repas_col.text_input("re-enter password:",type='password')
        pswd_alert = st.empty()
            
        if email and not validate_email(email):
            email_alert.warning('Email entered not valid',icon='⚠')
        
        if password and repassword and (password != repassword):
            pswd_alert.warning('Both are Note equal .Re-enter the password',icon='⚠')
        
        if username and email and (age > 8) and (password == repassword):
            reg_bttn_status : bool = False
            reg_bttn_help : str = 'Click to register your account'
        else:
            reg_bttn_status : bool = True
            reg_bttn_help : str = 'Fill all forms please!'

        if st.button('Register user',use_container_width=True,
                     type='primary',disabled=reg_bttn_status,
                     help=reg_bttn_help):
            
            ur = UserRegister(username, email,
                             dob, password)
            
            result = create_account(userid=ur.userid,
                           username=ur.username,
                           email=ur.email,
                           password=ur.password,
                           dob=ur.dob,
                           )
            
            if not result['status']:
                pswd_alert.error(result['message'],icon='⚠')
                        
def login_form() -> dict:
    
    st.title('login',anchor=False)
    st.divider()
    
    user_input : str = st.text_input('Enter username/email:')
    user_password : str = st.text_input('Enter password:',type='password')
    alert_col, frgt_bttn, login_bttn = st.columns([2,1,1])
    
    alert = alert_col.empty()
    with frgt_bttn.popover('options',
                        use_container_width=True):
        if st.button('register',use_container_width=True):
            register_form()
        
        st.button('forgot password',use_container_width=True)
    if login_bttn.button('login',use_container_width=True,
                    type='primary'):
        val_response = validate_user(userinput=user_input,password=user_password)
        if val_response['status']:
            alert.success(val_response['message'],icon='✅')
            with st.spinner('Forwarding to Homepage...'):
                time.sleep(5)
                try:
                    st.session_state.auth.update(val_response['user_data'])
                    st.rerun()
                except Exception as e:
                    alert.error(f'Error:{e}')
        else:
            alert.warning(val_response['message'],icon='🤦‍♂️')
            
@st.dialog('create task',width='large')
def create_task_dialog():

    edit_col, preview_col  = st.columns(2)
    
    with edit_col.container():
    
        title = st.text_input('Enter the task title:',placeholder='Example: go for walk')
        description = st.text_area('Enter description of task:',placeholder='Example: from BOT to edakochi')
        p_col, u_col = st.columns(2)
        priority = p_col.radio("Task Priority",[True,False])
        urgent = u_col.radio("Task Urgency",[True,False])
        t_type = st.selectbox('select task type:',['once','daily','monthly','yearly'])

    with preview_col.container(border=True,height=300):
        st.subheader('Preview')
        if title and description and t_type:
            st.write(f':grey[Title:] ***{title}***')
            st.write(f':grey[Description]: ***{description}***')
            st.write(f":grey[Priority:] ***{'important' if priority else 'not important'}***")
            st.write(f":grey[Urgency:] ***{'important' if urgent else 'not important'}***")
            st.write(f':grey[Task Type]: ***{t_type}***')
            
        else:
            st.text("--Fill all inputs to get preview--")
        
    alert = preview_col.empty()
    
    if preview_col.button("submit",use_container_width=True,type='primary'):
        t = Task(title,description,priority,urgent,t_type)
        result : dict = create_task(st.session_state.auth['userid'],task=t.task,description=t.description,
                                    priority=t.priority,urgent=t.urgent,
                                    t_type=t.t_type,status=t.status,
                                    task_date=t.task_date)
        
        if result['status']:
            alert.success(result['message'])
            time.sleep(0.8)
            st.session_state.todays_task=load_todays_task(st.session_state.auth['userid'])
            st.rerun()

@st.dialog('Delete task',width='small')
def delete_task_dialog():
    
    
    
    t_type = st.selectbox('select task type',
                           ['once','daily','monthly','yearly'],
                           index=None)

    
    with st.container(height=300):
        if t_type:
            get_type_tasklist(st.session_state.auth['userid'],t_type)
            
 
def task_view() -> None:
    
    for idx,task in enumerate(st.session_state.task_data[f'{today_timestamp}'],start=1):
        if not task['status']:
            if st.checkbox(f"{task['task']}",value=False,key=task['tid']):
                update_result = task_completed(st.session_state.auth['userid'],task['tid'],'status',True)
                if update_result['status']:
                    st.toast(f":green-background[{update_result['message']}]")
                    result = load_todays_task(st.session_state.auth['userid'])
                    st.session_state.task_data = result['data']
                    time.sleep(2)
                    st.rerun()
                if not update_result['status']:
                    st.toast(f":red-background[{update_result['message']}]")
        else:
            if not st.checkbox(f"~~:grey[{task['task']}]~~",value=True,key=task['tid']):
                update_result = task_completed(st.session_state.auth['userid'],task['tid'],'status',False)
                if update_result['status']:
                    st.toast(f":green-background[{update_result['message']}]")
                    result = load_todays_task(st.session_state.auth['userid'])
                    st.session_state.task_data = result['data']
                    time.sleep(2)
                    st.rerun()
                if not update_result['status']:
                    st.toast(f":red-background[{update_result['message']}]")