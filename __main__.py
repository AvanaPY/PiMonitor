import os
import sys
import argparse

from dotenv import load_dotenv
load_dotenv()

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

from app import App

def main():
    ap = argparse.ArgumentParser()

    ap.add_argument("-i", "--ip", type=str, required=True, help="Ip address of the device")
    ap.add_argument("-p", "--port", type=int, required=True, help="Port to run on")
    ap.add_argument("-c", "--camera", type=int, default=0, help="Which camera index to run")
    args = vars(ap.parse_args())
    
    app = App(args["ip"], args["port"], args["camera"])
    app.run()

if __name__ == '__main__':
    main()