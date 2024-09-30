import sqlite3

conn = sqlite3.connect("../database/manager.db",check_same_thread=False)
conn.isolation_level = None
cursor = conn.cursor()

def create_taskdata() -> None:
    try:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS task_data(
                tid INTEGER     PRIMARY KEY AUTOINCREMENT,
                uid INT     NOT NULL,
                created_date INT    NOT NULL,
                task CHAR(40)   NOT NULL,
                priority NUMERIC    NOT NULL,
                urgent NUMERIC  NOT NULL,
                status NUMERIC  NOT NULL DEFAULT(0) 
            )
            """
        )
        
    except Exception as e :
        print("Error:",e)

def insert_task(**kwargs) -> bool:
    """
    parameter:
        uid (int): userid.
        date (int): created_date/task_date.
        task (str): task.
        priority (bool): priority of task.  
        urgent (bool): urgency of task.  
    """
    
    kwargs['priority'] = 1 if kwargs['priority'] else 0
    kwargs['urgent'] = 1 if kwargs['urgent'] else 0
     
    try:
        cursor.execute("INSERT INTO task_data(uid,created_date,task,priority,urgent) \
                values(?,?,?,?,?)",(kwargs['uid'],kwargs['created_date'],kwargs['task'],kwargs['priority'],kwargs['urgent']))
        conn.commit()
        return True
        
    except Exception as e :
        print("Error:",e)
        return False

def delete_task(**kwargs) -> bool:
    try:
        cursor.execute("DELETE FROM task_data WHERE tid = ?",(kwargs['tid'],))
        conn.commit()
        return True
    
    except Exception as e :
        print("Error:",e)
        cursor.execute("ROLLBACK")
        return False
    
def get_all_task(**kwargs) -> list:
    
    try:
        cursor.execute('SELECT * FROM task_data WHERE uid = ?',(kwargs['uid'],))
        
        result : list[tuple] = cursor.fetchall()
        # print("All data:",result)
        return result
        
                
    except Exception as e:
        print("Error:",e)
        cursor.execute("ROLLBACK")
        return None
             
def specific_task(**kwargs) -> tuple:
    try:
        cursor.execute('SELECT * FROM task_data WHERE tid = ? AND uid = ?',(kwargs['tid'],kwargs['uid'],))
        
        result : list[tuple] = cursor.fetchone()
        # print("Specific task:",result)
        
        return result
                
    except Exception as e:
        print("Error:",e)
        
        return None
    
def update_task(**kwargs) -> bool:
    
    if 'priority' in kwargs:
        kwargs['priority'] = 1 if kwargs['priority'] else 0
    
    if 'urgent' in kwargs:
        kwargs['urgent'] = 1 if kwargs['urgent'] else 0
    
    if 'status' in kwargs:
        kwargs['status'] = 1 if kwargs['status'] else 0

    
    update_cols : list = [i for i in kwargs if i not in ['uid','tid']]
    
    update : str = ''
    for indx,col in enumerate(update_cols,start=1):
        temp_str : str = f"{col} = '{kwargs[col]}'"
        if len(update_cols) > 1 and indx != len(update_cols):
            temp_str = temp_str + ","
        update = update + temp_str
        
    condition = f"tid={kwargs['tid']} and uid={kwargs['uid']}"
    
    try:
        cursor.execute(f'UPDATE task_data SET {update} WHERE {condition}')
        conn.commit()
        return True
        
    except Exception as e:
        print("Error:",e)
        return False

def dbdata_to_dict(**kwargs) -> dict:
    
    dbdata = get_all_task(uid=kwargs['uid'])
    tasks_data : dict = {}
    all_timestamps : list[int] = []

    for data in dbdata:
        if data[2] not in all_timestamps:
            all_timestamps.append(data[2])


    print('all timestamp:',all_timestamps)
    
    for timestamp in all_timestamps:
        for data in dbdata:
            if timestamp == data[2]:
                if timestamp not in tasks_data:
                    print('running this')
                    tasks_data.update(
                        {
                            timestamp : [ 
                                    {
                                        'tid' : data[0],
                                        'task' : data[3],
                                        'priority' : data[4],
                                        'urgent' : data[5],
                                        'status' : data[6]
                                    }
                                ]
                        }
                    )
                else:
                    tasks_data[timestamp].append(
                                    {
                                        'tid' : data[0],
                                        'task' : data[3],
                                        'priority' : data[4],
                                        'urgent' : data[5],
                                        'status' : data[6]
                                    }
                    )
    
    return tasks_data

def create_users() -> None:
    try:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users_data(
                uid CHAR(40)     PRIMARY KEY,
                username CHAR(10)   NOT NULL,
                email CHAR(20)    NOT NULL,
                dob INTEGER  NOT NULL,
                password CHAR(20)  NOT NULL, 
                otp CHAR(20)    DEFAULT None, 
                created_date INT    NOT NULL
            )
            """
        )
        
    except Exception as e :
        print("Error:",e)



#---------------------user_data---------------------
    
def insert_user(*args) -> bool:
    
    try:
        cursor.execute("INSERT INTO users_data(uid,username,email,dob,password,created_date) VALUES(?,?,?,?,?,?)",args)      
        conn.commit()
        
        return {
            'status' : True,
            'message' : 'Account created Successfully.'
        }
    
    except Exception as e:
        print("Error:",e)
        return {
            'status' : False,
            'message' : e
        }

def check_user(**kwargs) -> dict:

    cursor.execute("SELECT 1 from users_data WHERE username = ?",(kwargs['username'],))      
    if cursor.fetchall():
        nstatus : bool = True
    else:
        nstatus : bool = False
    
    cursor.execute("SELECT 1 from users_data WHERE email = ?",(kwargs['email'],))      
    if cursor.fetchall():
        estatus : bool = True
    else:
        estatus : bool = False
                    
    return {
        'username' : nstatus,
        'email' : estatus,
    }
            
def get_userdata(**kwargs) -> dict:
        
    cursor.execute("SELECT uid,username,password FROM users_data WHERE username = ? OR email = ?",(kwargs['userinput'],kwargs['userinput'],))
    result = cursor.fetchone()
    
    return result    
    
    
    


# if __name__ == '__name__':
# TEST-CASES    
    # create_users()    
# create_database()
# dbdata_to_dict(uid=123)
# insert_task(uid=123, created_date=1456132541,task='go for a walk4',priority=0,urgent=1)
# update_task(tid=1,uid=123,task='go kill vasu',priority=True,urgent=True)
# delete_task(tid=123)
# specific_task(tid = 4,uid = 123)