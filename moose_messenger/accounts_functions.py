from moose_messenger import USERS
import os
import json
import uuid

sessions_keys = set()

def check_user_access(email, password):
    users = os.listdir(USERS)
    if email+".json" in users:
        with open(f"{USERS}{email}.json") as file:
            user_data = json.load(file)
            if user_data["password"] != password:
                return False
        user_data["last_session"] = str(uuid.uuid4())
        with open(f"{USERS}{email}.json", "w") as file:
            json.dump(user_data, file)
        sessions_keys.add(user_data["last_session"])
        return((user_data["username"], user_data["last_session"]))            
    return False

def create_user_account(email, password, username):
    users = os.listdir(USERS)
    if email+".json" in users:
        return (False, "Аккаунт с такой почтой уже существует")
    
    if len(username)>15:
        return (False, "Слишком длинный ник")
    elif len(username)<3:
        return (False, "Слишком короткий ник")
    
    with open(f"{USERS}{email}.json", "w") as file:
        session_key = str(uuid.uuid4())
        user_data = {"username": username, "password": password, "last_session": session_key}
        json.dump(user_data, file)
        sessions_keys.add(session_key)
    return (True, session_key)