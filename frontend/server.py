"""
Front-end server for deepmersion.
"""
import sys
import numpy as np

from PIL import Image
from flask import Flask, request, send_from_directory, send_file, jsonify

sys.path.append('..')
from backend.bridge import Bridge

bridge = Bridge('../backend/db/')

app = Flask(__name__, static_folder='deepmersion/build/static', static_url_path='/static')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# serve static files produced by react
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('deepmersion/build/static', path)

@app.route('/sounds/<path:path>')
def send_sounds(path):
    return send_from_directory('deepmersion/build/sounds', path)

@app.route('/')
def send_home():
    return send_file('deepmersion/build/index.html')

def do_classification(image):
    return -6*np.random.random((1000,)), -6*np.random.random((401,))

@app.route('/classify', methods=['POST'])
def classify():
    if not 'image' in request.files:
        # this should be a fatal error
        print('file not included')
    
    image = request.files['image']
    img = Image.open(image)
    
    # do the stuff here
    obj_dist, plc_dist = do_classification(img)
    volumes = bridge.get_sound(obj_dist, plc_dist, None, request.form['useObjects'], request.form['usePlaces'], request.form['useChatter'])

    return jsonify({ 'volumes': list(volumes), 'objectTags': ['a', 'b', 'c'], 'placeTags': ['d', 'e', 'f']})

if __name__ == '__main__':
    app.run(debug=True)
