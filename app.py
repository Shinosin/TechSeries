from flask import Flask, jsonify, render_template
import game

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return 

@app.route('/start_pygame')
def start_pygame():
    game.main()
    return render_template('end.html')


if __name__ == "__main__":
    app.run()