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
#sdc_station = sdc()

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

@app.route('/pump')
def pump_page():
    return render_template('pump.html')

@app.route('/pump/run', methods=['POST'])
def pump_run():
    data = request.get_json(silent=True)
    required = ['draw_port', 'dispense_port', 'speed', 'volume']
    if not data or not all(key in data for key in required):
        abort(400, description='Missing pump parameters')

    try:
        draw_port = int(data['draw_port'])
        dispense_port = int(data['dispense_port'])
        speed = float(data['speed'])
        volume = float(data['volume'])
    except (TypeError, ValueError):
        abort(400, description='Invalid pump parameters')

    #sdc_station.run(draw_port, dispense_port, speed, volume)
    return {
        'status': 'ok',
        'draw_port': draw_port,
        'dispense_port': dispense_port,
        'speed': speed,
        'volume': volume,
    }

@app.route('/image-station/live')
def image_station_live():
    return render_template('image_station_live.html')

def process_instructions(header):
    match header['machine']:
        case 'image-station':
            image_station.process_instruction(header['instruction'])
        case 'sdc':
            pass
        case _:
            raise ValueError("Unknown machine name")

@app.route('/')
def index():
    if 'station' in request.headers:
        process_instructions(request.headers)
    else:
        return render_template('index.html')
    return "Something went wrong!"

if __name__ == "__main__":
    app.run(host="100.107.255.14", port=80, threaded=True)