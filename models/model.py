from models.connection import db
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from flask_login import UserMixin
#dopo aver creato una nuova classe:
# flask db init
# flask db migrate -m "Descrizione della migrazione"
# flask db upgrade

# The UserMixin will add Flask-Login attributes to the model so that Flask-Login will be able to work with it.

user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)

def init_db():  #nuovo stile
    # Verifica se i ruoli esistono già
    if not db.session.execute(db.select(Role).filter_by(name='admin')).scalars().first():
        admin_role = Role(name='admin')
        db.session.add(admin_role)
        db.session.commit()

    if not db.session.execute(db.select(Role).filter_by(name='user')).scalars().first():
        user_role = Role(name='user')
        db.session.add(user_role)
        db.session.commit()

    # Verifica se l'utente admin esiste già
    if not db.session.execute(db.select(User).filter_by(username='admin')).scalars().first():
        admin_user = User(username="admin", email="admin@example.com")
        admin_user.set_password("adminpassword")
        
        # Aggiunge il ruolo 'admin' all'utente
        admin_role = db.session.execute(db.select(Role).filter_by(name='admin')).scalars().first()
        admin_user.roles.append(admin_role)

        db.session.add(admin_user)
        db.session.commit()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key= True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))  # Campo per la password criptata

    roles = db.relationship('Role', secondary=user_roles, backref=db.backref('users', lazy='dynamic'))
    
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
    
    def has_role(self, role_name):
        return any(role.name == role_name for role in self.roles)

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    expression = db.Column(db.String(255), nullable=False)
    result = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    user = db.relationship('User', backref=db.backref('results', lazy='select'))

    def __repr__(self):
        return f'<Results {self.id} {self.expression}={self.result}>'
    
    def to_json(self):
        data = {'id': self.id,
                'expression': self.expression,
                'result': self.result,
                'timestamp': self.timestamp.isoformat()}
        return data
    

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return f'<Role {self.name}>'

    



    

