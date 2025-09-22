from flask import Blueprint
from flask import jsonify
from flask import request
import json

from models.connection import db
from models.model import User



app = Blueprint('api', __name__) 

@app.route('/invert/<string>')
def invert(string):
    response = {
        'original_string':string,
        'inverted':string[::-1] 
    }
    return jsonify(response), 200

@app.route('/upper/<string>')
def upper(string):
    response = {
        'original_string':string,
        'inverted':string.upper() 
    }
    return jsonify(response), 200

@app.route('/save',methods=['POST'])
def save():
    response = {
        'request_data' : request.json
    }

    #metodo vecchio
    # fh = open("output.txt", "a")
    # fh.write(response)
    # svuota buffer e forza scrittura
    # fh.flush() 
    # fh.close()

    #metodo nuovo
    json_str = json.dumps(response)
    with open("output.txt", "a") as f:
         f.write(json_str + '\n')
    return jsonify(response), 200

@app.route('/adduser',methods=['POST'])
def add_user():
  response = {
      'request_data' : request.json
  }

  # Creazione di un nuovo utente con una password criptata
  user = User(username=request.json.get('username'), email=request.json.get('email'))
  user.set_password(request.json.get('password'))

  # Aggiunta dell'utente al database
  db.session.add(user)
  db.session.commit()

  risposta = {
      "id" : user.id,
      "email" : user.email
  }

  return jsonify(risposta), 200

