import os
from flask import Flask, flash, request, redirect, jsonify
from werkzeug.utils import secure_filename
import config as conf
from utils.classifier_image import  validaImagem


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify(
               status=200,
               msg='api rodando'
              )
    pass

@app.route('/validate-fish', methods=['POST'])
def upload_file():
    if request.method == 'POST':
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
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(conf.UPLOAD_FOLDER, filename))
            ret,acc=validaImagem(os.path.join(conf.UPLOAD_FOLDER, filename))
            os.remove(os.path.join(conf.UPLOAD_FOLDER, filename))
            return jsonify(
               type=ret,
               accuracy=str(acc)
              )



if __name__ == "__main__":
    ON_HEROKU = os.environ.get('ON_HEROKU')
    port = ''
    if ON_HEROKU:
    # get the heroku port 
        port = int(os.environ.get("PORT", 17995))  # as per OP comments default is 17995
    else:
        port = 3000
    app.run(host='0.0.0.0', port=port)
