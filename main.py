from dataclasses import dataclass
from flask import Flask, jsonify, request, render_template, redirect, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = 'my_secret_key'

db = SQLAlchemy(app)

@dataclass
class Player(db.Model):
    id: int
    username: str
    password: str

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f'<Player {self.username}>'
    
    def check_password(self, password):
        return self.password == password

@dataclass
class Game(db.Model):
    id: int
    player_id: int
    player2_id: int
    num_players: int

    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, primary_key=True)
    player2_id = db.Column(db.Integer, primary_key=True)
    num_players = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Game {self.id}>'
    

with app.app_context():
    db.create_all()

@app.route('/')
def menu():
    return render_template('menu.html')

@app.route('/SignUp')
def signup():
    return render_template('signup.html')

@app.route('/LogIn')
def login():
    return render_template('login.html')

@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/players', methods=['GET'])
def route_get_players():
    return get_players()

@app.route('/players/<player_id>', methods=['GET'])
def route_get_player(player_id):
    return get_player_by_id(player_id)

@app.route('/players/add',  methods = ['POST'])
def route_add_player():
    data = request.get_json()
    username = data['username']
    password = data['password']
    player = Player(username=username, password=password)
    db.session.add(player)
    db.session.commit()
    return 'SUCCESS'

@app.route('/players/delete', methods=['POST', 'DELETE'])
def route_delete_player():
    data = request.get_json()
    player_id = data['player_id']
    player = Player.query.get(player_id)
    if player is None:
        error_message = f"No player with ID {player_id} found."
        return render_template('menu.html', error_message=error_message)
    db.session.delete(player)
    db.session.commit()
    return redirect('/')

@app.route('/login', methods=['POST'])
def login2():
    data = request.get_json()
    player = Player.query.filter_by(username=data["username"]).first()
    if player and player.check_password(data["password"]):
        return redirect('/game')
    else:
        flash('Invalid username or password')
        return redirect('/LogIn')


@app.route('/players/delete/<player_id>', methods=['GET','DELETE'])
def route_delete_player2(player_id):
    return delete_player(player_id)

@app.route('/players/list', methods=['GET'])
def route_list_players():
    players = Player.query.all()
    return render_template('menu.html', players=players)

@app.route('/players/create', methods=['POST'])
def route_create_player():
    player = request.get_json()
    new_player = Player(username = player['username'], password = player['password'])
    db.session.add(new_player)
    db.session.commit()
    return jsonify(new_player)

def get_players():
    players = Player.query.all()
    return jsonify(players)

def get_player_by_id(player_id):
    player = Player.query.get(player_id)
    return jsonify(player)

def insert_player(username, password):
    new_player = Player(name=username, age=password)
    db.session.add(new_player)
    db.session.commit()
    return new_player.id

def delete_player(player_id):
    player = Player.query.get(player_id)
    if player is None:
        return f"No player with ID {player_id} found."
    db.session.delete(player)
    db.session.commit()
    return f"Player with ID {player_id} has been deleted."