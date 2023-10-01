from moose_messenger import USERS
import os
import json

def check_user_access(email, password):
    users = os.listdir(USERS)
    if email+".json" in users:
        with open(f"{USERS}{email}.json") as file:
            user_data = json.load(file)
            if user_data["password"] == password:
                return user_data["username"]
            return False
    return False

def create_user_account(email, password, username):
    users = os.listdir(USERS)
    if email+".json" in users:
        return False
    
    with open(f"{USERS}{email}.json", "w") as file:
        user_data = {"username": username, "password": password}
        json.dump(user_data, file)
    return True