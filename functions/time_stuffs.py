import streamlit as st 
from datetime import datetime,timedelta,time

class Time_stuffs:
    def __init__(self) -> None:
        self.today = datetime.combine(datetime.now(), time.min).timestamp()
        self.now = datetime.now().timestamp()
        tomorrow = datetime.combine(datetime.now(), time.min) + timedelta(days=1)
        self.tomorrow = tomorrow.timestamp()
        
    
    def check_all(self) -> float:
        print('\ntoday->',self.today)
        print('now->',self.now)
        print('tomorrow->',self.tomorrow)
        print('\nseconds->',self.tomorrow-self.now)
        
        
    def balance_time_percentage(self) -> int:
        percentage = ((self.tomorrow - self.now)/86400) * 100 
        second = (self.tomorrow - self.now)
        # return st.progress(int(percentage), text=f'{round(second/3600,3)} hours left')
        with st.container(border=True): 
            st.progress(int(percentage), text=f':green[{round(second/3600,3)} hours left]')