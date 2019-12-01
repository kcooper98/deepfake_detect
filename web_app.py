"""
Production version of web app.
Authors: Kyle Cooper, Erica Holswade,
Mark Holswade, and Stephen Kistler
"""
from flask import Flask, jsonify, request, render_template, flash, redirect, url_for
from werkzeug.utils import secure_filename
import numpy as np
import tensorflow
from tensorflow.keras.models import load_model
from tensorflow.keras.backend import clear_session
from tensorflow.keras.preprocessing import image
import cv2
import traceback
import os

UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

clear_session()
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.urandom(24)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
@app.route("/", methods=['POST', 'GET'])
def deepfake_ui():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if 'modelRadios' not in request.form:
            flash('No model chosen')
            return redirect(request.url)
        chosen_model = request.form['modelRadios']
        chosen_model = os.path.join('models', chosen_model)
        if file and allowed_file(file.filename) and chosen_model:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            return redirect(url_for('process_image',
                                    file_path=file_path,
                                    model_path=chosen_model))
    return render_template("deepfake.html")


@app.route("/process_image")
def process_image():
    file_path = request.args.get('file_path', None)
    model_path = request.args.get('model_path', None)
    # Load model
    selected_model = load_model(model_path)

    # Load and prep image
    test_image = image.load_img(file_path,
                                target_size=(64, 64))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)

    # Predict with model
    result = selected_model.predict(test_image)
    if result[0][0] == 1:
        prediction = 'real'
    else:
        prediction = 'fake'

    return render_template("output.html", prediction=prediction, image=file_path)


if __name__ == '__main__':
    app.run(debug=True)
