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
                uid CHAR(40)     NOT NULL,
                task CHAR(25)   NOT NULL,
                description CHAR(50)   NOT NULL,
                task_type CHAR(10)   NOT NULL,
                priority NUMERIC    NOT NULL,
                urgent NUMERIC  NOT NULL,
                status NUMERIC  NOT NULL DEFAULT(0),
                created_date INT    NOT NULL,
                FOREIGN KEY (uid)
                    REFERENCES users_data (uid)
            )
            """
        )
        
    except Exception as e :
        print("Error:",e)

def create_task_types() -> None:
    try:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS task_type_data(
                typeID INTEGER  PRIMARY KEY AUTOINCREMENT, 
                uid CHAR(40)     NOT NULL,
                task_title CHAR(25) NOT NULL,
                task_description CHAR(45) NOT NULL,
                task_type CHAR(15) NOT NULL,
                priority NUMERIC    NOT NULL,
                urgent NUMERIC  NOT NULL,
                created_date INT    NOT NULL,
                FOREIGN KEY (uid)
                    REFERENCES users_data (uid)
            )
            """
        )
        
    except Exception as e :
        print("Error:",e)

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

#---------------------task_list_data---------------------

def check_users_predefine(**kwargs) -> None:
    
    """
    uid (str) : userid.
    created_data (int): created_data.
    
    """
    
    try:
        cursor.execute("SELECT 1 FROM task_type_data WHERE uid = ? and t_type = 'daily",
                       (kwargs['uid'],))
        if cursor.fetchall():
            
            cursor.execute("SELECT uid,task_title,task_description, \
                           task_type,priority,urgent from task_type_data \
                           WHERE uid = ? AND task_type = 'daily' ",
                           (kwargs['uid'],))
            
            result = cursor.fetchall()
            
            status = 0
            
            for tt in result:
                tt + status + kwargs['created_date']
            # [ (uid,task,description,t_type,priority,urgent), 
            # (uid,task,description,t_type,priority,urgent), ]
            cursor.executemany("INSERT INTO task_data(uid,task,description,task_type,priority,urgent,created_date) \
                values(?,?,?,?,?,?,?)",result)
                
            return True
        
        return False
                 
        
    except Exception as e :
        print("Error:",e)
    
#---------------------task_data---------------------

def insert_task(**kwargs) -> bool:
    """
    parameter:
        uid (int): userid.
        date (int): created_date/task_date.
        task (str): task.
        description (str): description.
        task_type (str): task_type['once','daily','monthly','yearly']
        priority (bool): priority of task.  
        urgent (bool): urgency of task.  
    """
    create_taskdata()
    
    kwargs['priority'] = 1 if kwargs['priority'] else 0
    kwargs['urgent'] = 1 if kwargs['urgent'] else 0
     
    try:
      
        cursor.execute("SELECT 1 FROM task_type_data WHERE uid = ?  \
                       and task_title = ? and task_description = ? and task_type = 'daily' ",
                       (kwargs['uid'],kwargs['task'],kwargs['description'],))  
        
        result = cursor.fetchall()
        if not result:
            cursor.execute(" INSERT INTO task_type_data(uid,task_title, \
                           task_description,task_type,priority,urgent,created_date) values(?,?,?,?,?,?,?)",
                           (kwargs['uid'],kwargs['task'],kwargs['description'],kwargs['task_type'],
                            kwargs['priority'],kwargs['urgent'],kwargs['created_date'],))
        
        cursor.execute("INSERT INTO task_data(uid,created_date,task,description,task_type,priority,urgent) \
                values(?,?,?,?,?,?,?)",(kwargs['uid'],kwargs['created_date'],kwargs['task'],kwargs['description'],kwargs['task_type'],kwargs['priority'],kwargs['urgent']))
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
             
def get_today_task(**kwargs) -> tuple:
    """
    Get todays task only.
    parameter:
        uid (str): userid.
        task_type (str): task type ['once','daily','monthly','yearly'].
        created_date (int): timestamp of current day.
    """
    try:
        cursor.execute('SELECT tid,task,description,task_type,priority,urgent,status FROM task_data WHERE uid = ? AND created_date =? AND (task_type="once" OR task_type="daily") ',
                       (kwargs['uid'],kwargs['created_date'],))
        result : list[tuple] = cursor.fetchall()
        return result
                
    except Exception as e:
        print("Error:",e)
        return None
    
def update_task(**kwargs) -> bool:
    
    kwargs.update({
        kwargs['opt'] : kwargs['opt_val']
    })
    
    kwargs.pop("opt")
    kwargs.pop("opt_val")
    
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
        
    condition = f"tid={kwargs['tid']} and uid='{kwargs['uid']}'"
    
    
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

def get_list_type(**kwargs) -> dict:
    if kwargs['t_type'] == "once":
        statement = "SELECT tid,task,"
    

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
        
    cursor.execute("SELECT uid,username,password,dob FROM users_data WHERE username = ? OR email = ?",
                   (kwargs['userinput'],kwargs['userinput'],))
    result = cursor.fetchone()
    return result    


#---------------------startup---------------------
 
def startup() -> None:
    
    try:
        if cursor:
            create_users()
            create_taskdata()
            create_task_types()
        return {
            'status' : True,
            'message' : 'Connected'
        }
    except Exception as e:
        return {
            'status' : False,
            'mesaage' : e
        }
        
   
   
# create_task_types()
# if __name__ == '__name__':
# create_taskdata()
# TEST-CASES    
    # create_users()    
# create_database()
# dbdata_to_dict(uid=123)
# insert_task(uid=123, created_date=1456132541,task='go for a walk4',description='dadadawd dawdacsd',priority=0,urgent=1)
# update_task(tid=1,uid=123,task='go kill vasu',priority=True,urgent=True)
# delete_task(tid=123)
# specific_task(tid = 4,uid = 123)