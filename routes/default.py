from flask import Blueprint
from flask import render_template
from flask import jsonify
from flask import request

from models.connection import db
from models.model import User
from models.model import Umore


app = Blueprint('default', __name__) 

@app.route('/')
def home():
    return render_template('base.html')

# decoratore funzione che prende come input la funzione sotto
@app.route('/about')
def about():
    return "This is the about page."

@app.route('/hello')
def hello_guest():
    return render_template('hello.html')

@app.route('/hello/<name>')
def hello(name):
    return render_template('hello.html', name=name)

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        return "Form submitted!"
    else:
        return render_template('formUser.html')

@app.route('/users')
def get_all_users():
    users = User.query.all()

    response = {'users' : []}
    for user in users:
        response['users'].append(user.to_json())
    return response

@app.route('/users/<int:id>')
def get_user(id):
    #metodo vecchio
    #user = User.query.filter_by(id=id).first()

    #metodo nuovo
    stmt = db.select(User).filter_by(id=id)
    user = db.session.execute(stmt).scalar_one_or_none()
    if user:
        response = {'user':User.to_json(user)}
        return jsonify(response), 200
    else:
        response = {'error' : 'no such user'}
        return jsonify(response), 404

@app.route('/users/<string:username>')
def get_user_by_name(username):
    stmt = db.select(User).filter_by(username=username)
    user = db.session.execute(stmt).scalar_one_or_none()
    if user:
        response = {'user':User.to_json(user)}
        return jsonify(response), 200
    else:
        response = {'error' : 'no such user'}
        return jsonify(response), 404

@app.route('/users/<int:id>', methods=["PUT"])
def update_user_by_id(id):
    stmt = db.select(User).filter_by(id=id)
    user = db.session.execute(stmt).scalar_one_or_none()
    if user:
        user.username = request.json.get('username', user.username)
        user.email = request.json.get('email', user.email)
        password = request.json.get('password', None)
        if password:
            user.set_password(password)
        db.session.commit()
        response = {'user' : user.to_json()}
        return jsonify(response), 200
    else:
        response = {'error': 'no such user'}
        return jsonify(response), 404


@app.route('/users/<string:username>', methods=["PUT"])
def update_user_by_username(username):
    stmt = db.select(User).filter_by(username=username)
    user = db.session.execute(stmt).scalar_one_or_none()

    if user:
        user.username = request.json.get('username', user.username)
        user.email = request.json.get('email', user.email)
        password = request.json.get('password', None)
        if password:
            user.set_password(password)
        db.session.commit()
        response = {'user' : user.to_json()}
        return jsonify(response), 200
    else:
        response = {'error': 'no such user'}
        return jsonify(response), 404

#fastAPI framework per api in python
@app.route('/users/<int:id>', methods=["DELETE"])
def delete_user_by_id(id):
    response = {
        'message': 'Received DELETE request',
        'id': id,
        'status': 'Resource deleted'
    }
    stmt=db.select(User).filter_by(id=id)
    user=db.session.execute(stmt).scalar_one_or_none()
    if user:
        db.session.delete(user)
        db.session.commit()
    return jsonify(response), 200

@app.route('/users/<int:id>/addUmore', methods=["POST"])
def add_umore_to_user(id):
  # Creazione di un nuovo umore  
   stmt = db.select(User).filter_by(id=id)
   user = db.session.execute(stmt).scalar_one_or_none()
   if user:
    umore = Umore(stato=request.json.get('stato'), user_id=id)

    # Aggiunta dell'umore al database
    db.session.add(umore)
    db.session.commit()

    risposta = {
      "id" : umore.id,
      "user_id" : umore.user_id,
      "stato" : umore.stato,
      "timestamp" : umore.timestamp
   }
   return jsonify(risposta), 200 

# @app.route('/form', methods=['GET', 'POST'])
# def form():
#     if request.method == 'POST':
#         return "Form submitted!"
#     else:
#         return render_template('formUser.html')

    

       
  



