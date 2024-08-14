import streamlit as st 
from datetime import datetime
from functions.time_stuffs import Time_stuffs


def main():
    ts = Time_stuffs()
    ts.balance_time_percentage() #<<-- hour left progress bar
    

    
if __name__ == '__main__':
    main()