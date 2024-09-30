import streamlit as st
import time

def logout_menu() -> None:
    
    st.title('Logout',anchor=False)
    st.divider()
   
    
    if not st.session_state.auth['authorization'] and \
    not st.session_state.auth['userid']:
   
        alert = st.empty()
        for i in range(10):
            time.sleep(0.5)
            alert.caption(f'Please login. Forwading to login page in {10-i}s')
        st.switch_page('Home.py')
    
    
    
    st.caption('Are you sure 😢?')
    blank_col, cancel_bttn, conf_bttn = st.columns([2,1,1])
    if cancel_bttn.button('cancel',use_container_width=True):
        st.switch_page('Home.py')
    
    if conf_bttn.button('confirm',use_container_width=True,type='primary'):
        st.session_state.auth = {
        'authorization' : False,
        'username' : None,
        'userid' : None
    }
        st.rerun()
    
if __name__ == '__main__':
    
    try:
        logout_menu()
    except:
        st.switch_page('Home.py')