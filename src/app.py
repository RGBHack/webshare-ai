import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np

from flask import Flask, render_template, make_response, flash, redirect, request, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import random
import string

app = Flask(__name__)
model = ResNet50(weights='imagenet')

ALLOWED_EXTENSIONS = {"jpg"}
upP = "../usr_data"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



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
        img = image.load_img(img_path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        preds = model.predict(x)
        
        os.remove(os.path.join(upP, filename2))
        return decode_predictions(preds, top=3)[0][0][1]

app.run(debug=True, host='0.0.0.0', port=80)
