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
    
class Umore(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    stato = db.Column(db.String(80), nullable=False)
    #in alternativa si possono salvare i timestamp come linux timestamp
    timestamp = db.Column(db.DateTime, default = datetime.datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @property
    def umori(self):
        #ritorna la lista degli umori associati all'utente
        # stmt = db.select(Umore).filter_by(user_id=self.id)
        # umori = db.session.execute(stmt).scalars().all()
        return [umore.to_dict() for umore in self.umore]

    user = db.relationship('User', backref=db.backref('Umore', lazy=True))

    def __repr__(self):
        return f'<Umore id:{self.id} stato:{self.stato}>'
    
    def to_dict(self):
        #timestamp dev'essere convertito in stringa sennò il json si arrabbia :(
        data = {
            'id' : self.id,
            'stato':self.stato,
            'timestamp':self.timestamp
        }
        return data
