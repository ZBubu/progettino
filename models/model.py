from models.connection import db
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from flask_login import UserMixin
#dopo aver creato una nuova classe:
# flask db init
# flask db migrate -m "Descrizione della migrazione"
# flask db upgrade

# The UserMixin will add Flask-Login attributes to the model so that Flask-Login will be able to work with it.
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key= True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))  # Campo per la password criptata
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.id} {self.username}>'
    
    def to_json(self):
        data = {'username': self.username,
                'email':self.email,
                'id':self.id}
        return data


    

