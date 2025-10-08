import os
from dotenv import load_dotenv
from flask import Flask
from flask import render_template
from flask import url_for, request
from flask_migrate import Migrate
from routes.default import app as bp_default 
from routes.api import app as bp_api
from routes.auth import app as bp_auth
from flask_login import LoginManager
from models.connection import db
from models.model import init_db
from models.model import User

app = Flask(__name__)

app.register_blueprint(bp_default)
app.register_blueprint(bp_api, url_prefix='/api')
app.register_blueprint(bp_auth, url_prefix='/auth')

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI',"sqlite:///labo1.db")
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY',"grandepanepanegrande1212121212121212")
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER',"uploads/")
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000 # 16 MB max file size

current_path = os.getenv('PATH')
tesseract_path = os.getenv('TESSERACT',r"E:\1Goku\Programmi\tesseract-3.02.02")

if tesseract_path not in current_path:
    os.environ["PATH"] = current_path + ";" + tesseract_path

db.init_app(app)
with app.app_context():
    init_db()
migrate = Migrate(app, db)

# blocco di inizializzazione del login manager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.execute(stmt).scalar_one_or_none()
    # return User.query.get(int(user_id))   # legacy
    return user

if __name__ == "__main__": # flask viene eseguito dal comando: python app.py
    load_dotenv() #se c'è già una variabile di ambiente non la sovrascrive
    app.run(debug=True)
