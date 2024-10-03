import streamlit as st 
from datetime import datetime
from forms import login_form
from mainpage import *
from http_req import test_connection
import streamlit.components.v1 as components


if 'auth' not in st.session_state :
    st.session_state.auth = {
        'authorization' : False,
        'username' : None,
        'userid' : None,
        'dob' : None
    }
    if 'task_data' not in st.session_state :
        st.session_state.task_data = {}
    
@st.cache_data
def on_start_connection():  
    test_connection()

def main() -> None:
    
    on_start_connection()
    
    if not st.session_state.auth['authorization'] and \
    not st.session_state.auth['userid']:
        login_form()
    elif st.session_state.auth['authorization'] and \
    st.session_state.auth['userid']:
        mainpage()
        
if __name__ == '__main__':
    
    st.set_page_config(
        page_title="Tracker",
        page_icon="⏱",
        layout="centered",
        initial_sidebar_state="collapsed",
                    )
    
    main()
    
    components.html("""
    <script>
    window.onbeforeunload = function() {
        return 'Are you sure you want to leave? You might lose unsaved data.';
    };
    </script>
    """, height=0)
    