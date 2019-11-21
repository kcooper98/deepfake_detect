"""A simple example flask application
"""
from flask import Flask, jsonify, request, render_template, flash, redirect, url_for
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.backend import clear_session
import cv2
import traceback
import os

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

clear_session()
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.urandom(24)

# def load_iris_model():
#     global iris_model
#     # Step 1: Determine file location
#     model_file = 'models/sk-model.joblib'
#     # Step 2: Load model
#     iris_model = joblib.load(model_file)

# def load_mnist_model():
#     global mnist_model
#     model_file = 'models/keras-mnist.h5'
#     mnist_model = load_model(model_file)
#     mnist_model._make_predict_function()


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/json")
def json_endpoint():
    return jsonify({
        "message": "Hello World!"
    })


@app.route("/variables/<variable>")
def example_variable(variable):
    return jsonify({
        "message": f"The variable you entered is {variable}"
    })


@app.route("/request-args")
def example_request_args():
    try:
        a = request.args["a"]
        b = request.args["b"]
        c = request.args["c"]
        return jsonify({
            "message": f"You entered a = {a}, b= {b} and c= {c}."
        })
    except:
        return jsonify({
            "message": f"You did not provide one of a, b, or c."
        })

# @app.route("/iris")
# def predict_iris():
#     # To predict the iris species we need:
#     # sepal length in cm - sepal_length
#     # sepal width in cm - sepal_width
#     # petal length in cm - petal_length
#     # petal width in cm - petal_width
#     try:
#         sl = request.args["sepal_length"]
#         sw = request.args["sepal_width"]
#         pl = request.args["petal_length"]
#         pw = request.args["petal_width"]
#     except:
#         return jsonify({
#             "message": f"You did not provide one of sepal_length, sepal_width, petal_length, or petal_width."
#         })
#     vector = np.array([sl, sw, pl, pw])
#     pred = iris_model.predict([vector])
#     classes = ["Setosa","Versicolour","Virginica"]
#     species = classes[pred[0]]
#     return jsonify({
#         "message": f"The predicted species for the observations you entered is {species} ",
#         "species": species
#     })


# @app.route("/iris-ui")
# def iris_ui():
#     return render_template("iris.html")


# @app.route("/mnist", methods=["POST"])
# def mnist_predict():
#     try:
#         image =  request.files['file'].read()
#         print("Got image")
#         # https://stackoverflow.com/a/27537664/818687
#         arr = cv2.imdecode(np.fromstring(image, np.uint8), cv2.IMREAD_UNCHANGED)
#         print("CV2 read image")
#         my_image = arr / 255.0
#         my_images = my_image.reshape(1, 28, 28, 1)
#         print("Got here")

#         pred = mnist_model.predict(my_images)
#         n = int(np.argmax(pred))
#         print(n)
#         return jsonify({
#             "message": f"The predicted number for the uploaded image is {n} ",
#             "number": n
#         })
#     except Exception as e:
#         print(traceback.format_exc())
#         return jsonify({
#             "message": f"An error occurred. {e}"
#         })

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/deepfake-ui", methods=['POST', 'GET'])
def deepfake_ui():
    flash('test')
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
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return render_template("deepfake.html")


if __name__ == '__main__':
    #     load_iris_model()
    #     load_mnist_model()
    app.run(debug=True)
