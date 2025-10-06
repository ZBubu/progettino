import json
import datetime
from flask import Blueprint
from flask import jsonify
from flask import request
from flask import current_app 

from models.connection import db
from models.model import User, Result



app = Blueprint('api', __name__) 


# @app.route('/invert/<string>')
# def invert(string):
#     response = {
#         'original_string':string,
#         'inverted':string[::-1] 
#     }
#     return jsonify(response), 200

@app.route('/users', methods=['GET'])
def getAllUsers():
    users = db.session.execute(db.select(User)).scalars().all()
    users_json = [user.to_json() for user in users]
    if users_json:
            return jsonify(users_json), 200
    else:
            return jsonify({"message": "No users found"}), 404


@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    users = db.session.execute(db.select(User)).scalars().all()
    user = next((u for u in users if u.id == id), None)
    if user:
        return jsonify(user.to_json()), 200
    else:
        return jsonify({"message": "User not found"}), 404
    
@app.route('/users/<string>', methods=['GET'])
def get_user_by_email(string):
    user = db.session.execute(db.select(User).filter_by(email=string)).scalar_one_or_none()
    if user:
        return jsonify(user.to_json()), 200
    else:
        return jsonify({"message": "User not found"}), 404

@app.route('/results', methods=['GET'])
def getAllResults():
    results = db.session.execute(db.select(Result)).scalars().all()
    results_json = [result.to_json() for result in results]
    if results:
        return jsonify(results_json), 200
    else:
        return jsonify({"message": "No results found"}), 404

@app.route('/results/greater/<int:val>', methods=['GET'])
def getAllResultsGreater(val):
    #TODO: capire perché non funziona come dovrebbe
    results = db.session.execute(db.select(Result).filter(Result.result > val)).scalars().all()
    results_json = [result.to_json() for result in results]
    current_app.logger.info(f'results: {results}')
    if results:
        return jsonify(results_json), 200
    else:
        return jsonify({"message": "No results found"}), 404

@app.route('/results/lastHour',methods=['GET'])
def getAllResultsLastHour():
    #TODO: capire perché non funziona come dovrebbe
    one_hour_ago = datetime.datetime.utcnow() - datetime.timedelta(hours=1)
    results = db.session.execute(db.select(Result).filter(Result.timestamp >= one_hour_ago)).scalars().all()
    results_json = [result.to_json() for result in results]
    if results:
        return jsonify(results_json), 200
    else:
        return jsonify({"message": "No results found"}), 404
     