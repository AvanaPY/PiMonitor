import cv2
import base64
import argparse
import threading
import time
import random

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

def _thread_entry_fetch_image(timeout=16):
    while 1:
        fetch_image()
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

@app.route('/get_image')
def get_image():
    image_id = int(flask.request.headers.get('Last-Image-ID'))
    if image_id == IMAGE_ID:
        return flask.jsonify({ "status": "error"})
    elif not vc or not b64:
        return flask.jsonify({ "status": "error", "message": "No video feed available" })
    else:
        return flask.jsonify({ "status": "ok", "base64": b64, "ID": IMAGE_ID})

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