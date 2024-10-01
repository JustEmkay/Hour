from db_actions import *
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import bcrypt

app = FastAPI()

# uvicorn test:app --reload
# tasklist /FI "IMAGENAME eq python.exe" <---- KILL CMD for uvicorn 
#taskkill /PID <PID> /F

now_date = datetime.now()


class UserRegister(BaseModel):
    userid : str
    username : str
    email : str
    dob : int
    password : str
    
class LoginInfo(BaseModel):
    userinput : str
    password : str
    
class taskData(BaseModel):
    task : str
    description : str
    priority : bool
    urgent : bool
    t_type : str
    status : bool
    task_date : int
    
    
@app.get("/")
async def test():
    return{
        'author' : 'emkay' 
    }    

@app.post("/register")
async def register_user(userdata : UserRegister):
    
    result = check_user(username=userdata.username,email=userdata.email)
    
    if result['email']:
        return {
            'status' : False,
            'message' : 'Email already in use , try recovering password.'
        }
    elif result['username']:
        return {
            'status' : False,
            'message' : 'username already in use.Type new username'
        }
    
    action : dict = insert_user(userdata.userid,userdata.username,
                                userdata.email,userdata.dob,
                                userdata.password,now_date)
    return action

@app.get("/login")
async def validate_user(loginInfo : LoginInfo):
    result = check_user(username = loginInfo.userinput, email = loginInfo.userinput)   
    if result['email'] or result['username']:
        val_data = get_userdata(userinput=loginInfo.userinput)
        
            
        user_hash = loginInfo.password.encode('utf-8')
        user_og_hash = val_data[2].encode()
        result : bool = bcrypt.checkpw(user_hash,user_og_hash)
        if result:
            return {
                'status':True,
                'message' : 'User found!',
                'user_data' : {
                    'userid' : val_data[0],
                    'username' : val_data[1],
                    'dob' : val_data[3]    ,
                    'authorization' : True
                }
            }
        else:
            return {
                'status':False,
                'message' : 'Wrong password',
            }
                        
    return {
        'status' : False,
        'message' : 'user not found'
    }
        
@app.post("/task/create/{uid}/")
async def create_task(uid : str ,tdata : taskData):
    
    if insert_task(uid=uid,created_date=tdata.task_date,
                   task=tdata.task,description=tdata.description,
                   task_type=tdata.t_type,priority=tdata.priority,urgent=tdata.urgent):
    
        return {
            'status' : True,
            'message' : 'task added succefully.'
        }
    return {
            'status' : False,
            'message' : 'Failed to create task.'
        }
    
@app.get("/task/today/{uid}/{created_date}")
async def todays_task(uid:str, created_date:int):
    result = get_today_task(uid=uid,created_date=created_date)
    