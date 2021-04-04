import cv2
import base64
import argparse
import threading
import time
import random
from appdata import AppData
appdata = AppData()

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

import flask
app = flask.Flask(__name__)

vc = None

lock = threading.Lock()
frame = None
b64 = ''
IMAGE_ID = -1

GRAB_NEW_IMAGE_READY = False

def _thread_entry_fetch_image(timeout=16):
    global GRAB_NEW_IMAGE_READY
    while 1:
        if GRAB_NEW_IMAGE_READY:
            fetch_image()
            GRAB_NEW_IMAGE_READY = False
            
        time.sleep(timeout * 0.001)

def fetch_image():
    global frame, b64, IMAGE_ID
    with lock:
        retv, frame = vc.read()
        _, frame = cv2.imencode('.JPEG', frame)
        b64 = base64.b64encode(frame).decode("utf-8")

        IMAGE_ID += 1
        if IMAGE_ID > 1000:
            IMAGE_ID = 1

@app.route('/')
def home():
    return flask.render_template('index.html')

@app.route('/api/print')
def api_print():
    args = flask.request.args
    user = args.get('user')
    pwd = args.get('pwd')

    if not user or not pwd:
        return flask.jsonify({ 
            "error": 400, 
            "message": "Missing credentials"
        }), 400

    if not user == 'emil' or not pwd == '123':
        return flask.jsonify({
            "error": 400,
            "message": "Invalid credentials"
        })
    
    data_tags = args.get('data')
    if not data_tags:
        return flask.jsonify({
            "error": 400,
            "message": "No data tags"
        })

    data = {}
    for tag in data_tags.split(','):
        tag_args = tag.split(':')

        tag = tag_args[0]
        tag_args = tag_args[1:]

        data_tag = {}
        for arg in tag_args:
            if tag == 'time':
                if arg == 'left':
                    data_tag[arg] = appdata.print_time_manager.time_left()
            elif tag == 'image':
                if arg == 'base64':
                    data_tag[arg] = b64
                if arg == 'id':
                    data_tag[arg] = IMAGE_ID

        data[tag] = data_tag

    global GRAB_NEW_IMAGE_READY
    GRAB_NEW_IMAGE_READY = True

    return flask.jsonify({ 
        "status": "ok", 
        "data": data 
    })

def main():
    ap = argparse.ArgumentParser()

    ap.add_argument("-i", "--ip", type=str, required=True, help="Ip address of the device")
    ap.add_argument("-p", "--port", type=int, required=True, help="Port to run on")
    ap.add_argument("-c", "--camera", type=int, default=0, help="Which camera index to run")
    args = vars(ap.parse_args())

    global vc, frame
    vc = cv2.VideoCapture(args["camera"])
    
    if vc.isOpened():
        vc.set(3,1280)
        vc.set(4,720)

        retv, frame = vc.read()

        if not retv:
            vc = None
        else:
            t = threading.Thread(target=_thread_entry_fetch_image)
            t.daemon = True
            t.start()
    else:
        vc = None

    app.run(host=args["ip"], port=args["port"], debug=True, 
            threaded=True, use_reloader=False)

    if vc:
        vc.release()

if __name__ == '__main__':
    main()
    # print(appdata)