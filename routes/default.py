import os
from flask import Blueprint
from flask import render_template
from flask import jsonify
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from flask import current_app
from werkzeug.utils import secure_filename
from PIL import Image
import pytesseract

from models.connection import db
from models.model import User

app = Blueprint('default', __name__) 


@app.route('/')
def home():
    return render_template('base.html')

@app.route('/upload', methods=['GET'])
def upload_file():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_file_post():
    # https://flask.palletsprojects.com/en/stable/patterns/fileuploads/
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        if os.path.isdir(current_app.config['UPLOAD_FOLDER']):
            if os.access(current_app.config['UPLOAD_FOLDER'], os.W_OK):
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            else:
                flash('Directory not writable')
                return "Directory not writable"
        else:
            flash('Directory not found')
            return "Directory not found"
        print(pytesseract.image_to_string(Image.open(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))))
        #TODO: salvare nel database il risultato di tesseract
        #  cancellare l'immagine caricata dall'utente
        # risolvere l'espressione e salvarla db
        return redirect(url_for('default.home'))


       
  



