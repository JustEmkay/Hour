import requests
from creds import API_URL
from datetime import datetime
from models import pass_hashing

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

def verify_user(uid,**userinputs) -> None:
    req = requests.get(API_URL + f"verify/{uid}",json=userinputs)
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
    print(taskIDs)
    req = requests.delete(API_URL + f"task/delete/selected/{uid}",json=taskIDs)
    res = req.status_code
    if res == 200:
        return req.json() 
    
def get_all_task(uid:str) -> dict:
    req = requests.get(API_URL + f"task/all/{uid}")
    res = req.status_code
    if res == 200:
        return req.json() 
    return []

def get_pre_task(uid:str) -> dict:
    req = requests.get(API_URL + f"task/all/predefined/{uid}")
    res = req.status_code
    if res == 200:
        return req.json() 
    return []

def update_specific_task(uid:str,applyAll:bool,**task_data) -> bool:
    req = requests.put(API_URL + f'task/update/{uid}?applyAll={applyAll}',json=task_data)
    res = req.status_code
    if res == 200:
        return req.json()
       
def get_userdata(uid:str, username:str, option:str) -> dict:
    req = requests.get(API_URL + f'user/{uid}/{username}?option={option}')
    res = req.status_code
    if res == 200:
        return req.json()
    
def password_reset(uid:str,password:str) -> dict:
    
    req = requests.put(API_URL + f"password/{uid}",json={"password":pass_hashing(password)})
    res = req.status_code
    if res == 200:
        return req.json()
     
def delete_user_req(uid:str,**userinputs) -> dict:
    
    req = requests.delete(API_URL + f"user/delete/{uid}",json=userinputs)
    res = req.status_code
    if res == 200:
        return req.json()    
    
    

 
# def upload_task_data( uid:str, option:str, backup_task_data:list[list] ) -> bool:
#     req = requests.put(API_URL + f"task/upload/{uid}?db={option}",json=backup_task_data )
#     res = req.status_code
#     if res == 200:
#         return req.json()