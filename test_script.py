import sqlite3
from pathlib import Path
import random as r

def generate_phone_number():
    phone = []
    phone.append(r.randint(6, 9))

    for i in range(1, 10): 
        phone.append(r.randint(0, 9)) 
    
    phone_number = str()
    for i in phone:
        phone_number = phone_number + str(i)

    return phone_number

def generate_user_id():
    user_type = ['admin', 'owner', 'manager', 'staff']
    return f"{user_type[r.randint(0,3)]}-{r.randint(0,100)}"

def generate_user_type():
    user_type = ['SYSTEM_ADMIN', 'CAFE_OWNER', 'CAFE_MANAGER', 'CAFE_STAFF']
    return user_type[r.randint(0,3)]

def generate_user_role():
    user_type = ['CHEF', 'WAITER', 'CASHIER']
    return user_type[r.randint(0,2)]

conn = sqlite3.connect(Path("./instance/newdatabase.db"))

cur = conn.cursor()

user_data = []
for i in range(1, 101):
    user_data.append(('User', f"Name{i}", generate_phone_number(), generate_user_id(), "123", generate_user_type()))

query = '''
        INSERT INTO User (first_name, last_name, phone, user_id, password, user_type) VALUES (?, ?, ?, ?, ?, ?)
    '''

print(user_data)

cur.executemany(query, user_data)

conn.commit()