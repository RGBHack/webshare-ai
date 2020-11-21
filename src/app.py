import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

from tensorflow.keras.applications.xception import Xception
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.xception import preprocess_input, decode_predictions
import numpy as np

from flask import Flask, render_template, make_response, flash, redirect, request, url_for, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import os
import random
import string

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
model = Xception(weights='imagenet')

ALLOWED_EXTENSIONS = {"jpg", "png"}
upP = "../usr_data"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@cross_origin()
@app.route('/ai', methods=["POST"])
def pp():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filename2 = random.choices(string.ascii_uppercase + string.digits, k=13)
        filename2 = ''.join(filename2)
        
        actual_file_path = os.path.join(upP, filename2)
        file.save(os.path.join(upP, filename2))

        img_path = os.path.join(upP, filename2)
        img = image.load_img(img_path, target_size=(229, 229))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        preds = model.predict(x)
        
        os.remove(os.path.join(upP, filename2))
        predictions = decode_predictions(preds, top=2)[0]
        arr = []
        for i in range(2):
            arr.append(predictions[i][1])
        
        return ','.join(arr)

app.run(debug=True, host='0.0.0.0', port=80)
