"""
Front-end server for deepmersion.
"""
import sys
import numpy as np

from PIL import Image
from flask import Flask, request, send_from_directory, send_file, jsonify

sys.path.append('..')
from backend.bridge import Bridge

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
    return np.zeros((1000,)), np.zeros((401,))

@app.route('/classify', methods=['POST'])
def classify():
    if not 'image' in request.files:
        print('file not included')
    image = request.files['image']
    img = Image.open(image)
    
    # do the stuff here
    obj_dist, plc_dist = do_classification(img)
    volumes = Bridge.get_sound(obj_dist, plc_dist)

    return jsonify({ 'volumes': list(volumes), 'tags': ['a', 'b', 'c']})

if __name__ == '__main__':
    app.run(debug=True)
