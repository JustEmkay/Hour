from datetime import datetime
import bcrypt,uuid


today_stamp = int(datetime(datetime.now().year,datetime.now().month,datetime.now().day,0,0,0).timestamp())

def pass_hashing(password : str) -> str:
    bytes = password.encode('utf-8') 
    hash = bcrypt.hashpw(bytes, bcrypt.gensalt()) 
    return hash.decode('utf-8')

def idgen() -> str:
    unique_id : str = uuid.uuid4()
    return unique_id

def date_to_tstamp(slctd_date) -> int:
    """Convert datetime.date obect to timestamp
    """
    time_stamp : int = int( datetime(slctd_date.year,slctd_date.month,slctd_date.day,0,0,0).timestamp())
    return time_stamp 


class Todo:
    
    def __init__(self, task:str, priority : bool , urgent:bool,
                 status:bool = None ,task_date : int = None) -> None:
         
         self.task = task
         self.priority = priority
         self.urgent = urgent
         self.status = status if status is not None else False
         self.task_date = task_date if task_date is not None else int(today_stamp)
         
    def __str__(self) -> str:
          return f'{datetime.fromtimestamp(self.task_date).strftime("%d-%m-%Y")} : {self.task} | priority:{self.priority} | usrgent:{self.urgent} | status: {self.status}'
      

    def task_toDict(self) -> dict:
        
        result : dict = {
            'task' : self.task,
            'priority' : self.priority,
            'urgent' : self.urgent,
            'status' : self.status
        }
        
        return result 
    

class UserRegister:
    
    def __init__(self,username : str,
                 email : str, dob : datetime.date,
                 password : str, userid : str = None) -> None:
        
                
        self.username : str = username
        self.email : str = email
        self.dob : int = date_to_tstamp(dob)
        self.password : str = pass_hashing(password)
        self.userid : str = userid if userid is not None else str(idgen())
         
    def __str__(self) -> str:
          return f'userid:{self.userid}, usename: {self.username}, email: {self.email}, date of birth: {self.dob}, password: {self.password}'
     