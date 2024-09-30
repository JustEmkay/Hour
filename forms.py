import streamlit as st 
from datetime import datetime
import re,requests,time
from models import UserRegister
from Home import API_URL

def age_calc(dob : datetime.date ) -> dict:
    today : datetime.date = datetime.today()
    return today.year - dob.year - ((today.month,today.day) < (dob.month,dob.day))

def validate_email(email):  
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):  
        return True  
    return False

def create_account(**userdata) -> dict:
    req = requests.post(API_URL + "register",json=userdata)
    resp = req.status_code
    if resp == 200:
        return req.json()
    
def validate_user(**userinputs) -> None:
    req = requests.post(API_URL + "login",json=userinputs)
    resp = req.status_code
    if resp == 200:
        return req.json()
    

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
    
    user_input : str = st.text_input('Enter username/email:',value='1234')
    user_password : str = st.text_input('Enter password:',type='password',value='12345678')
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
            
            