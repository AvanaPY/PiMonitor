import cv2
import base64
import argparse
import threading
import time

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

import flask
app = flask.Flask(__name__)

vc = cv2.VideoCapture(0)
vc.set(3,1280)
vc.set(4,1024)

lock = threading.Lock()
frame = None
b64 = ''

def _thread_entry_fetch_image(timeout=16):
    while 1:
        fetch_image()
        time.sleep(timeout * 0.001)

def fetch_image():
    global frame, b64
    with lock:
        retv, frame = vc.read()
        _, frame = cv2.imencode('.JPEG', frame)
        b64 = base64.b64encode(frame).decode("utf-8")

@app.route('/')
def home():
    return flask.render_template('index.html')

@app.route('/get_image')
def get_image():
    while lock.locked() or not b64: 
        pass
    response = flask.jsonify({ "base64": b64 })
    return response

def main():

    ap = argparse.ArgumentParser()

    ap.add_argument("-i", "--ip", type=str, required=True, help="Ip address of the device")
    ap.add_argument("-p", "--port", type=int, required=True, help="Port to run on")
    ap.add_argument("-c", "--camera", type=int, default=0, help="Which camera index to run")
    args = vars(ap.parse_args())

    global vc
    vc = cv2.VideoCapture(args["camera"])
    if not vc.isOpened():
        print('Could not find a VideoCapture source.')
        return

    t = threading.Thread(target=_thread_entry_fetch_image)
    t.daemon = True
    t.start()

    print(f"Running app at {args['ip']}:{args['port']}")
    app.run(host=args["ip"], port=args["port"], debug=True, 
            threaded=True, use_reloader=False)

    vc.release()
    cv2.destroyWindow("preview")

if __name__ == '__main__':
    main()