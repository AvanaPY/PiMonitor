import cv2
import base64
import threading
import time
from .appdata import AppData
appdata = AppData()

import flask
flask_app = flask.Flask(__name__)

@flask_app.route('/')
def home():
    return flask.render_template('index.html')

@flask_app.route('/api/print')
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
                    data_tag[arg] = appdata.b64
                if arg == 'id':
                    data_tag[arg] = appdata.IMAGE_ID

        data[tag] = data_tag

    appdata.GRAB_NEW_IMAGE_READY = True

    return flask.jsonify({ 
        "status": "ok", 
        "data": data 
    })


###################################
#             My App              #
###################################
class App:
    def __init__(self, ip, port, camera):
        self._flask_app = flask_app

        self._ip = ip
        self._port = port

        self._vc = None
        self._camera = camera
        self._lock = threading.Lock()

    def _thread_entry_fetch_image(self, timeout=16):
        while 1:
            if appdata.GRAB_NEW_IMAGE_READY:
                self.__fetch_image()
                appdata.GRAB_NEW_IMAGE_READY = False
                
            time.sleep(timeout * 0.001)

    def __fetch_image(self):
        with self._lock:
            retv, frame = self._vc.read()
            _, frame = cv2.imencode('.JPEG', frame)

            appdata.frame = frame
            appdata.b64 = base64.b64encode(frame).decode("utf-8")

            appdata.IMAGE_ID += 1
            if appdata.IMAGE_ID > 1000:
                appdata.IMAGE_ID = 1

    def _set_up_camera(self):
        self._vc = cv2.VideoCapture(self._camera)
        if self._vc.isOpened():
            self._vc.set(3, 1280) # Set width to 1280px
            self._vc.set(4, 720)  # Set height to 720px

            retv, _ = self._vc.read()
            return retv
        return False

    def run(self):
        result = self._set_up_camera()
        if result:
            t = threading.Thread(target=self._thread_entry_fetch_image)
            t.daemon = True
            t.start()

        self._flask_app.run(host=self._ip, port=self._port,
                            debug=True, threaded=True, use_reloader=False)