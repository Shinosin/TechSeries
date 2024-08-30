from flask import Flask, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

users = {
    "admin": generate_password_hash("password123")
}

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and check_password_hash(users[username], password):
            return render_template("index.html")
        else:
            error = 'Invalid credentials. Please try again.'

    return render_template('login.html', error=error)

@app.route('/index')
def index():
    '''Home Page'''
    return render_template('index.html')


#add new users
# password = "newuserpassword"
# hashed_password = generate_password_hash(password)
# print(hashed_password)

if __name__ == "__main__":
    app.run()
