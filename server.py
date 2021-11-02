
from flask import Flask, render_template, request
import eventlet
import socketio
import eventlet.wsgi
import base64
from VideoStream import VideoStream

sio = socketio.Server()
app = Flask(__name__)
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

INIT = 0
READY = 1
PLAYING = 2

state = {}

@app.route('/')
def index():
    return render_template('file.html')

@sio.event
def connect(sid, environ=None, auth=None):
    global state
    state[sid] = INIT

@sio.on('play')
def playVideo(sid):
    global state
    if state[sid] == READY:
        state[sid] = PLAYING
        i = 0
        while state[sid] == PLAYING:
            frame = video.nextFrame()
            if not frame:
                state[sid] = READY
            else:
                frame= base64.encodebytes(frame).decode("utf-8")
                i += 1
                sio.emit("response", frame)
                sio.sleep(0.04)

@sio.on('setup')
def setupVIDEO(sid):
    global state, video
    state[sid] = READY
    video = VideoStream('movie.Mjpeg')

@sio.on('pause')
def pauseVIDEO(sid):
    global state
    state[sid] = READY

@sio.event
def disconnect(sid):
    print("[INFO] disconnected from the server")

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('127.0.0.1',5000)), app)
    



