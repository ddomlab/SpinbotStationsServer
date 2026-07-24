"""
Simple flask server

Routes:
    /               -> Public landing page
    /imagestation   -> Requires API key
            - "ping" - confirms server status
            - "capture" - returns jpeg img
"""

from flask import Flask, request, send_file, abort, Response, render_template
from SpinbotStationsDrivers import imagestation, sdc
import io
import cv2
import threading

app = Flask(__name__)
image_station = imagestation()
# sdc_station = sdc()

@app.route("/image-station")
def route_image_station():
    if 'instruction' in request.headers:
        # This means the request is coming from a python client
        return image_station.process_instruction(request.headers['instruction'])
    else:
        # Request is coming from a regular browser, show image_station.html
        return render_template('image_station.html')

def generate_frames():
    try:
        while True:

            success, frame = image_station.cap.read()

            if not success:
                break

            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

            yield (
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n'
                + frame_bytes +
                b'\r\n'
            )
    except RuntimeError:
        # camera dropped out mid-stream; end the generator gracefully
        return

@app.route('/stream')
def stream():
    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@app.route('/image-station/live')
def image_station_live():
    return render_template('image_station_live.html')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="100.107.255.14", port=80, threaded=True)