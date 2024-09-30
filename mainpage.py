import streamlit as st
from datetime import datetime


def being_alive(dob_stamp) -> list:

    return [123,45]
    
def mainpage() -> None:
    
    title_col, counter_col = st.columns([0.7,0.3],vertical_alignment='top')
    title_col.title(f"Welcome {st.session_state.auth['username']}",
             anchor=False)
    
    alive_counter = being_alive(st.session_state.auth['dob'])
    counter_col.metric(label="Being Alive",
                       value=f"{alive_counter[0]} days",
                       delta=f"{alive_counter[1]} months")
    
    st.divider()