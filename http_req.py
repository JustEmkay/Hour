import requests
from creds import API_URL
from datetime import datetime

today_timestamp : int = int(datetime(datetime.now().year,datetime.now().month,
                                     datetime.now().day,0,0,0).timestamp())



def get_streak_score(uid : str) -> int:
    req = requests.get(API_URL + f"streaks/{uid}")
    res = req.status_code
    if res == 200:
        return req.json()

def test_connection() -> dict:
    req = requests.get(API_URL + "connection")
    res = req.status_code
    if res == 200:
        return req.json()

def create_account(**userdata) -> dict:
    req = requests.post(API_URL + "register",json=userdata)
    resp = req.status_code
    if resp == 200:
        return req.json()
    
def validate_user(**userinputs) -> None:
    req = requests.get(API_URL + "login",json=userinputs)
    resp = req.status_code
    if resp == 200:
        return req.json()

def load_todays_task(uid) -> dict:
    req = requests.get(API_URL + f'task/today/{uid}/{today_timestamp}')
    res = req.status_code
    if res == 200:
        return req.json()
    
def create_task(uid,**task_data) -> dict:
    req = requests.post(API_URL + f"task/create/{uid}/",
                        json=task_data)
    res = req.status_code
    if res == 200:
        return req.json()
    else:
        return {
            'status' : False,
            'message' : 'Connecting to server failed'
        }
       
def task_completed(uid:str,tid:int,opt:str,opt_val:bool) -> bool:
    req = requests.put(API_URL + f"update/{uid}/{tid}?opt={opt}&opt_val={opt_val}")
    res = req.status_code
    if res == 200:
        return req.json()
    
def get_type_tasklist(uid:str,t_type:str) -> dict:
    req = requests.get(API_URL + f"task/type/{uid}?t_type={t_type}")
    res = req.status_code
    if res == 200:
        return req.json()
    
def delete_task(uid:str,**taskIDs) -> dict:
    req = requests.get(API_URL + f"task/delete/selected/{uid}",json=taskIDs)
    res = req.status_code
    if res == 200:
        return req.json() 