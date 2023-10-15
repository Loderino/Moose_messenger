from datetime import datetime
import json
from flask import Flask, render_template, request, redirect, url_for, session
from moose_messenger.accounts_functions import check_user_access, create_user_account, sessions_keys

app = Flask(__name__)
app.secret_key = '73870e7f-634d-433b-946a-8d20132bafac'

@app.route('/')
def index():
   return render_template("login.html", context = {"message": ""})

@app.route('/chatting')
def chatting():
    return render_template("main_page.html", context=session.get("data"))

@app.route('/Access_checking',  methods=['POST'])
def Access_checking():
    email = request.form['email']
    password = request.form['password']
    access = check_user_access(email, password)
    if access:
        session['data'] = {"username": access[0], "session": access[1]}
        return redirect(url_for('chatting'))
    else:
        return render_template("login.html", context = {"message": "Неверный логин или пароль"})
        

@app.route('/Create_account',  methods=['POST'])
def Create_account():
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    ans, desc = create_user_account(email, password, username)
    if ans:
        session['data'] = {"username": username, "session": desc}
        return redirect(url_for('chatting'))
    else:
        return render_template("register.html", context = {"message": desc})
        
@app.route('/Send_message',  methods=['POST'])
def Send_message():
    mes = json.loads(request.data.decode(encoding="utf-8"))
    if mes["session"] not in sessions_keys:
        return ("nahuy otsuda, blyat")
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
def Get_messages():
    try:
        with open("message_hystory.json") as file:
            messages = json.load(file)
            return messages
    except:
        return []

@app.route('/register',  methods=['GET'])
def register():
   if request.method == 'GET':
       return render_template('register.html', context = {"message": ""})
   
if __name__ == "__main__":
   app.run(host="0.0.0.0", port="5000")