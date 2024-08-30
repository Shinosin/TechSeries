from flask import Flask, jsonify, render_template
import pygame
import threading
import game

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_pygame')
def start_pygame():
    game.main()
    return render_template('end.html')


@app.route('/stop_pygame')
def stop_pygame():
    global pygame_running
    if pygame_running:
        pygame_running = False
        return jsonify({"status": "Pygame stopped"})
    else:
        return jsonify({"status": "Pygame not running"})

if __name__ == "__main__":
    app.run()