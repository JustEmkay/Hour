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
    
    
@app.get("/")
def test():
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

@app.post("/login")
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
        
