from flask import Flask, render_template, make_response, flash, redirect, request, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import random
import string

app = Flask(__name__)

# def ai(imgpath) {
#     # for runnign model
# }

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
        os.rename(filename,filename2 )
        actual_file_path = os.path.join(upP, filename2)
        file.save(os.path.join(upP, filename2))
        os.remove(os.path.join(upP, filename2))


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=int(os.environ.get('PORT', 5003)))