import streamlit as st 
from datetime import datetime
from forms import *
from mainpage import *
import streamlit.components.v1 as components

API_URL = 'http://127.0.0.1:8000/'

if 'auth' not in st.session_state :
    st.session_state.auth = {
        'authorization' : False,
        'username' : None,
        'userid' : None,
        'dob' : None
    }

def main() -> None:
    
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
    