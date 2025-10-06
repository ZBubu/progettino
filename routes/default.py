import os
import time
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import Blueprint
from flask import render_template
from flask import jsonify
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from flask import current_app
from flask_login import login_required, current_user

from PIL import Image
import pytesseract

from models.connection import db
from models.model import User, Result
        

app = Blueprint('default', __name__) 
ts = time.time()


@app.route('/')
def home():
    return render_template('base.html')

@app.route('/upload', methods=['GET'])
def upload():
    return render_template('upload.html')

@login_required
@app.route('/upload', methods=['POST'])
def upload_post():
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
        #OCR non sembra funzionare bene con le espressioni matematiche
        #https://muthu.co/all-tesseract-ocr-options/
        imageOCR= pytesseract.image_to_string(
            Image.open(
                os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                , config='textord_equation_detect=1 -c tessedit_char_whitelist=0123456789+-*/')
        flash('OCR result: '+imageOCR)
        os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        if(imageOCR.count('+')>0 or imageOCR.count('-')>0 and (imageOCR.count('*')==0 and imageOCR.count('/')==0)):
            flash('Expression detected: '+imageOCR)
            if(imageOCR.count('+')>0):
                operands=imageOCR.split('+')
                try:
                    result=int(operands[0].strip())+int(operands[1].strip())
                    r = Result(user_id=current_user.get_id(),
                       expression=imageOCR,
                       result=str(result),
                       timestamp=datetime.now())
                    db.session.add(r)  # equivalente a INSERT
                    db.session.commit()
                except Exception as e:
                    flash('Error in expression')
            elif(imageOCR.count('-')>0 or imageOCR.count('−')>0):
                operands=imageOCR.split('-')
                try:
                    result=int(operands[0].strip())-int(operands[1].strip())
                    r = Result(user_id=current_user.get_id(),
                       expression=imageOCR,
                       result=str(result),
                       timestamp=datetime.now())
                    db.session.add(r)  # equivalente a INSERT
                    db.session.commit()
                except Exception as e:
                    flash('Error in expression')
            flash('Result successfully saved')
        else:
            if(imageOCR.count('*')>0):
                operands=imageOCR.split('*')
                try:
                    result=int(operands[0].strip())*int(operands[1].strip())
                    r = Result(user_id=current_user.get_id(),
                       expression=imageOCR,
                       result=str(result),
                       timestamp=datetime.now())
                    db.session.add(r)  # equivalente a INSERT
                    db.session.commit()
                except Exception as e:
                    flash('Error in expression')
            if(imageOCR.count('/')>0):
                operands=imageOCR.split('/')
                try:
                    result=int(operands[0].strip())/int(operands[1].strip())
                    r = Result(user_id=current_user.get_id(),
                       expression=imageOCR,
                       result=str(result),
                       timestamp=datetime.now())
                    db.session.add(r)  # equivalente a INSERT
                    db.session.commit()
                except Exception as e:
                    flash('Error in expression')
            #flash('moltiplication and division are not supported')
        return redirect(url_for('default.home'))


       
  



