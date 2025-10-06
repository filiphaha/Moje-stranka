from flask import Flask, render_template, request, redirect, url_for, session
import json, os
app = Flask(__name__)
app.secret_key = "nějaký_silný_tajný_řetězec"
USERS_FILE = "users.json"
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f)
# "Databáze na zkoušku"
def load_users():
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
    
def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('user')
        pwd = request.form.get('password')

        users = load_users()
        if user in users and users[user] == pwd:
            session['username'] = user
            return redirect(url_for('success'))
        else:
            return render_template('login.html', error="Špatné jméno nebo heslo.")
    
    return render_template('login.html', error=None)

@app.route('/')
def home():
    return redirect( url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('user')
        password = request.form.get('password')
        users = load_users()

        if username in users:
            return render_template('register.html', error="Uživatel už existuje!")
        
        users[username] = password
        save_users(users)

        return redirect(url_for('login'))
    return render_template('register.html', error=None)

    
@app.route('/success')
def success():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    original_name = session['username']
    vocative_name = vocative(original_name)
    return render_template(
       'success.html',
        username=original_name,
        username_voc=vocative_name      
    )
    
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))
    

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/zivotopis')
def zivotopis():
    return render_template('zivotopis.html')

@app.route('/devlog')
def devlog():
    return render_template('devlog.html')
    
    
    


def vocative(username):
    if username.endswith("a"):
        return username[:-1] + "o"
    elif username.endswith("p"):
        return username + "e"
    elif username.endswith("r"):
        return username + "e"
    elif username.endswith("r"):
        return username + "e"
    elif username.endswith("l"):
        return username + "e"
    elif username.endswith("m"):
        return username + "e"
    elif username.endswith("n"):
        return username + "e"
    elif username.endswith("š"):
        return username + "i"
    else:
        return username

if __name__ == '__main__':
    app.run(debug=True)

   


