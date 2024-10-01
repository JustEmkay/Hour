import streamlit as st
import time

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
    
    
if __name__ == '__main__' :
    
    try:
        settings_page()
    except:
        st.switch_page('Home.py')