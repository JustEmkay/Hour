import streamlit as st 
from datetime import datetime,timedelta,time
from functions.time_stuffs import Time_stuffs


def main():
    header_C , refresh_c = st.columns([5,1])
    header_C.header('Create your time',anchor=False,divider='gray')
    if refresh_c.button('Refresh ♻',use_container_width=True):
        st.rerun()
        
    ts = Time_stuffs()
    ts.balance_time_percentage() #<<-- hour left progress bar
    



if __name__ == '__main__':
    main()