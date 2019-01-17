import os

from flask import Flask, request, send_from_directory, jsonify
from werkzeug.utils import secure_filename

IMAGES_FOLDER = '../images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['IMAGES_FOLDER'] = IMAGES_FOLDER

def allowed_file(filename):
    return '.' in filename and \
       filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['POST'])
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
    file.save(os.path.join(app.config['IMAGES_FOLDER'], filename))
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

