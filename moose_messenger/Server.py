from datetime import datetime
import json
from flask import Flask, render_template, request
from moose_messenger.accounts_functions import check_user_access, create_user_account

app = Flask(__name__)

@app.route('/')
def index():
   return render_template("login.html", context = {"message": ""})

@app.route('/Access_checking',  methods=['POST'])
def check_access():
    email = request.form['email']
    password = request.form['password']
    access = check_user_access(email, password)
    if access:
        return render_template("main_page.html", context={"username": access})
    else:
        return render_template("login.html", context = {"message": "Неверный логин или пароль"})
        

@app.route('/Create_account',  methods=['POST'])
def a():
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    ans = create_user_account(email, password, username)
    if ans:
        return render_template("main_page.html", context={"username": username} )
    else:
        return render_template("register.html", context = {"message": "Учётная запись с таким логином уже существует"})
        
@app.route('/Send_message',  methods=['POST'])
def b():
    mes = json.loads(request.data.decode(encoding="utf-8"))
    with open ("message_hystory.json") as file:
        messages = json.load(file)
    now = datetime.now()
    messages.append({"username": mes["username"], "time": f"{now.hour}:{now.minute}:{now.second}", "content": mes["message"]})
    with open ("message_hystory.json", "w") as file:
        json.dump(messages, file,
                  sort_keys=False,
                indent=4,
                ensure_ascii=False,
                separators=(",", ": "))
    return("f")

@app.route('/Get_messages',  methods=['POST'])
def get_messages():
    try:
        with open("message_hystory.json") as file:
            messages = json.load(file)
            return messages
    except:
        return []

@app.route('/register',  methods=['GET'])
def success():
   if request.method == 'GET':
       return render_template('register.html', context = {"message": ""})
   
if __name__ == "__main__":
   app.run(host="0.0.0.0", port="5000")