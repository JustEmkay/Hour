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

class del_taskIDs(BaseModel):
    taskID : dict
    preID : dict
   
    
@app.get("/")
async def test():
    return{
        'author' : 'emkay' 
    }    

@app.get("/connection")
async def testing_db():
    
    result = startup()
    print(result['message'])
    return result
       
@app.post("/register")
async def register_user(userdata : UserRegister):
    
    result = check_user(username=userdata.username,email=userdata.email)
    
    if result['email']:
        return {
            'status' : False,
            'message' : 'Email already in use , try recovering password.'
        }
    if result['username']:
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

def unpack_list_to_dict(data:list[tuple], created_date:int, dict_keys:list[str]) -> dict:

    temp_tasks : dict = {}
    temp_task_list : list[dict] = []
    temp_task : dict = {}

    for task in data:
        for idx,col in enumerate(task):
            temp_task.update(
                {
                    dict_keys[idx] : col
                }
                ) 
        print("temp_task:",temp_task) 
        temp_task_list.append(temp_task)
        temp_task = {}
        
    if created_date not in temp_tasks:
        temp_tasks.update({
            created_date : temp_task_list 
        })
    
    
    return temp_tasks
  
@app.get("/task/today/{uid}/{created_date}")
async def todays_task(uid:str, created_date:int):
    
    if check_users_predefine(uid=uid,created_date=created_date):
       
        result = get_today_task(uid=uid,created_date=created_date)
        if len(result) >= 1:
            return {
                'status' : True,
                'message' : f'found {len(result)} tasks',
                'data' : unpack_list_to_dict(result,created_date,
                                            ['tid','task',
                                            'description','task_type',
                                            'priority','urgent','status'])
            }
          
        
    return {
    'status' : False,
    'message' : f'empty task list',
    'data' : {}
}
    
@app.put("/update/{uid}/{tid}")
async def update_task_status(uid : str , tid : int, opt : str, opt_val: bool):
    print(f"uid:{uid}\ntid:{tid}\noption:{opt}\noption val:{opt_val}")
    if update_task(uid=str(uid),tid=tid,opt=opt,opt_val=opt_val):
        return {
            'status' : True,
            'message' : "updated task successfully"
        }
    return {
        'status' : False,
        'message' : "updatation failed"
    }
    
@app.get("/task/type/{uid}")
async def get_type_tasklist(uid:str,t_type:str):
    result = get_list_type(uid=uid, t_type=t_type)
    
    return result
    
@app.get("/streaks/{uid}")
async def streakList(uid:str):
    
    result = get_streakList(uid=uid)
    
    return {
        'status' : True,
        'message' : 'accessed streaks.',
        'data' : result
    }
    
@app.delete("/task/delete/selected/{uid}")
async def delete_tasks(uid : str, taskIDs : del_taskIDs):
    print(uid,taskIDs)