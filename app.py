import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from utils import Utils

UPLOAD_FOLDER = os.getcwd() + '/data/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'ufile' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['ufile']
        print(file and Utils(file.filename).allowed_file())
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return render_template('index.html', text_detected = "",ufile="Upload File")
        if file and Utils(file.filename).allowed_file():
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            txt = Utils(filename).read_image()
            request.args.get("ufile", "")
            return render_template('index.html',text_detected = txt, ufile="Choose Another File")
    return render_template('index.html', text_detected = "", ufile="Upload File")

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)

