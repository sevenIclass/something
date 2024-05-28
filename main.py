from flask import render_template, g, redirect, url_for, jsonify, Response
#from flask_login import LoginManager, login_user, login_required
from controllers.controller_2.controller_2 import *
from flask import Flask, request
import uvicorn
from flask import send_file
#from dxcams import *
import asyncio
import time
import numpy
import cv2
import dxcam
import time
from PIL import ImageGrab, ImageOps
camera = dxcam.create()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'twegawekglHILQGED'


def screen():
    #print('nothing')
    #with mss.mss() as sct:
        #while True:
            #raw = sct.grab(monitor)
            # Use numpy and opencv to convert the data to JPEG.
            #img = cv2.imencode('.jpg', numpy.array(raw))[1].tobytes()
            #yield (img)

    while True:
        screenshot = camera.grab()
        if screenshot is not None:
            #screenshot[:,:,2] = cv2.bitwise_not(screenshot[:,:,2])
            screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)
            ret, buffer = cv2.imencode('.png', screenshot)
            #frame = buffer.tobytes()
            #buffer = ImageOps.invert(buffer)
            frame = bytearray(buffer)
            yield(b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        elif screenshot is None:
            pass
    pass


@app.route('/')
def video():
    return Response(screen(), mimetype='multipart/x-mixed-replace; boundary=frame')
    #return render_template('screen.html')


#@app.route('/')
#def video():
#    return render_template('screen.html')


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
