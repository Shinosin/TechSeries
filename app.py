from flask import Flask, render_template, request, session, redirect, url_for
import game

app = Flask(__name__)
app.secret_key = 'your_secret_key' # Required for signing cookies

@app.route('/')
def index():
    user = session.get('user')
    if user:
        ## give render some deets of user
        return render_template('home.html')
    
    return render_template('login.html') # You are not logged in

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        username, password = request.form['username'], request.form['password']
        print(username, password)
        # verify is user
        session['user'] = request.form['username'] # store session
        return redirect(url_for('index'))
    
    ## failed to login - give some error msg
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == "POST":
        username, password = request.form['username'], request.form['password']
        # store acct details in database
        # do some validation for valid input?? idk check if not alr in database
        # give them some kind of success page maybe? or redirect to login page
        return render_template('login.html', msg="Successfully Create Acct")
        
    #blank registartion page
    return render_template('new.html')

@app.route('/home')
def home():
    return redirect(url_for('index'))

@app.route('/profile')
def profile():
    # fetch profile details from database
    return render_template('profile.html')

@app.route('/game')
def game_page():
    return render_template('game.html')

@app.route('/start_pygame')
def start_pygame():
    game.main()
    ## Give user points + Display user points?
    return render_template('end.html')

if __name__ == "__main__":
    app.run()