import os

from flask import Flask, request, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np

import pickle

# CONSTANTS
# allowed image extensions for the upload method
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
# the saved model file
MODEL_FILE = 'finalized_model.pkl'
# N_COLS used for training the model. Considering the images have different
# sizes, we need to insert extra data to run predictions. Just a hack for now
N_COLS = 612900

# create flask app and set config
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
# considering the model path is environment dependent, we need to load the
# config before generating it
MODEL_FILE_PATH = os.path.join(app.config['ROOT_PATH'], 'src', MODEL_FILE)

# load the model from disk
cls = pickle.load(open(MODEL_FILE_PATH, 'rb'))

########### utility methods ##############
def allowed_file(filename):
    '''
    Method for checking if the filename extension in ALLOWED_EXTESIONS

    Args
    ===
        filename - name of the file that is being uploaded

    Returns
    ===
        boolean - allowed or not
    '''
    return '.' in filename and \
       filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_image_data(file):
    '''
    Method for loading the image data for classification. It opens the image
    file and adds the extra data required (considering the images have
    different sizes, we need N_COLS cols).

    This is a hack and should not go into production like that. Ideally, all
    images received should be sized the same. Also, the transformation from
    np.array to list and back to np.array is awful and should be improved.

    Args
    ===
        file - werkzeug.FileStorage

    Returns
    ===
        np.array - flatten image data
    '''
    # open the imge file as a PIL Image
    pic = Image.open(file)
    # transform into a np.array so we may conveniently flatten it and then cast
    # into a list
    img_data = list(np.array(pic).flatten())
    # fill the data up to N_COLS
    # is this logic right?
    for i in range(N_COLS - len(img_data)):
        img_data.append(0)
    # cast back to np.array and return
    return np.array(img_data)

def check_request_file():
    '''
    Helper method for checking if there is a file named 'image' in the request.
    If there isn't, raise FileNotFoundException.

    Returns
    ===
        werkzeug.FileStorage - image stream

    Raises
    ===
        FileNotFoundException
    '''
    if 'image' not in request.files or request.files['image'].filename is '':
        raise FileNotFoundException(
            'No \'image\' in request or empty filename')
    return request.files['image']

def build_error_response(e):
    '''
    Helper method for building json error message responses.

    Args
    ===
        e - Exception / custom error message

    Returns
    ===
        json formatted string - see
            http://flask.pocoo.org/docs/0.12/api/#flask.json.dumps
    '''
    return jsonify(
        status='error',
        message='{}'.format(e)
    )

########### routes ##############
@app.route('/classify', methods=['POST'])
def classify():
    '''
    Method for classifying an image received through a POST request using the
    model saved to the server.
    '''
    try:
        # check if we have a file in the request
        file = check_request_file()
        # load img data
        img = load_image_data(file)
        # run prediction
        res = cls.predict([img,img])
        # return result
        return jsonify(
            status='ok',
            message='image prediction succesful'.format(res),
            pred='{}'.format(res))
    except FileNotFoundException as e:
        # if check_request_file does not find a valid file, it will raise a
        # FileNotFoundException
        return build_error_response(e)


@app.route('/upload', methods=['POST'])
def upload_file():
    '''
    Method for transforming and saving an image to the server.

    For now, we're just uploading and returning it to test the workflow, but
    the intent is to transform the image, save it to the server and return it
    transformed.
    '''
    # check if the post request has the file part
    try:
        # check if we have a file in the request
        file = check_request_file()
        # check if the file extension is in ALLOWED_EXTENSIONS
        if allowed_file(file.filename):
            # use werkzeug's convenient secure_filename function to generate a
            # secure filename lol
            filename = secure_filename(file.filename)
            # save file using the app.config['ROOT_PATH'] to build the absolute
            # path
            file.save(os.path.join(
                app.config['ROOT_PATH'], app.config['IMAGES_FOLDER'], filename))
            # transform here in the future
            # if all is ok, return the image
            return send_from_directory(app.config['IMAGES_FOLDER'], filename)
        else:
            # if the extension is not in allowed extensions, we return an error
            # message
            return build_error_response('filename not allowed')

    except FileNotFoundException as e:
        # if check_request_file does not find a valid file, it will raise a
        # FileNotFoundException
        return build_error_response(e)


@app.route('/images/<filename>')
def uploaded_file(filename):
    '''
    Method for visualizing the uploaded images.

    Args
    ===
        filename - actual name of the file (with extension)
    '''
    return send_from_directory(app.config['IMAGES_FOLDER'], filename)

