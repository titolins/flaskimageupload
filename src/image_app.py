import os

from flask import Flask, request, send_from_directory, jsonify
from werkzeug.utils import secure_filename

import pickle

#IMAGES_FOLDER = '../images'
# pythonanywhere path
#IMAGES_FOLDER = '/home/chipos/flaskimageupload/images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
MODEL_FILE = 'finalized_model.pkl'


# create flask app and set config
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
MODEL_FILE_PATH = os.path.join(app.config['ROOT_PATH'], 'src', MODEL_FILE)
#app.config['IMAGES_FOLDER'] = IMAGES_FOLDER

# load the model from disk
cls = pickle.load(open(MODEL_FILE_PATH, 'rb'))

########### utility methods ##############
def allowed_file(filename):
    return '.' in filename and \
       filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



########### routes ##############
@app.route('/classify', methods=['GET'])
def classify():
    # get the file info
    img_data = request.get_json()
    # supposing the json format to be as follows
    '''
    {
        'data': []float (img_data)
    }
    '''
    res = cls.predict(img_data)
    return jsonify(
        status='ok',
        message='image prediction succesful'.format(filename),
        pred='{}'.format(res))


@app.route('/upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    print(request.files)
    file = request.files['image'] if 'image' in request.files else None
    if file is None or request.files['image'].filename == '':
        return jsonify(
            status='error',
            message='image is None or filename = \'\''
        )

    #######################################
    #######################################
    print(file)
    attrs = vars(file)
    print(''.join(['file.{} = {}\n'.format(k, v) for k,v in attrs.items()]))
    #######################################
    #######################################

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
    file.save(os.path.join(
        app.config['ROOT_PATH'], app.config['IMAGES_FOLDER'], filename))
    '''
    #TO GET THE PATH, USE THIS METHOD BELOW
    return jsonify(
        status='ok',
        message='image uploaded to `/images/{}`'.format(filename),
        path='/images/{}'.format(filename))

    #TO GET THE IMAGE, USE THIS OTHER ONE (BELOW)
    '''
    return send_from_directory(app.config['IMAGES_FOLDER'], filename)


@app.route('/images/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['IMAGES_FOLDER'], filename)

