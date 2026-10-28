#!/usr/bin/env python3
"""
Simple flask server

import threading
Routes:
    /               -> Public landing page
    /imagestation   -> Requires API key
            - "ping" - confirms server status
#sdc_station = sdc()
            - "capture" - returns jpeg img
"""

from flask import Flask, request, send_file, abort, Response, render_template
from SpinbotStationsDrivers import imagestation
import stepper
import station_functions
import threading

app = Flask(__name__)
ip_type = "else"      # can be PUBLIC or TAILSCALE
image_station = imagestation()
setup_camera = imagestation(camera_index=2, width=1600, height=1200)
stepper_lock = threading.Lock()
MOTOR_INCREMENTS = {1, 10, 100, 250, 500}
MOTOR_COUNT = stepper.steppers.num_motors
#sdc_station = sdc()

@app.route("/image-station")
def route_image_station():
    if 'instruction' in request.headers:
        # This means the request is coming from a python client
        return image_station.process_instruction(request.headers['instruction'])
    else:
        # Request is coming from a regular browser, show image_station.html
        return render_template('image_station.html')

@app.route('/stream')
def stream():
    return Response(
        image_station.generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@app.route('/stream/setup')
def setup_stream():
    return Response(
        setup_camera.generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@app.route('/capture')
def capture_image():
    return setup_camera.capture()

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

@app.route('/station/functions')
def station_function_list():
    return {
        'functions': [
            {'name': name, 'label': definition['label']}
            for name, definition in station_functions.FUNCTIONS.items()
        ],
    }

@app.route('/station/function/run', methods=['POST'])
def station_function_run():
    data = request.get_json(silent=True) or {}
    function_name = data.get('name')
    if not isinstance(function_name, str):
        abort(404, description='Station function not found')

    definition = station_functions.FUNCTIONS.get(function_name)
    if definition is None:
        abort(404, description='Station function not found')

    try:
        with stepper_lock:
            result = definition['handler']()
    except Exception as error:
        app.logger.exception('Station function failed: %s', function_name)
        abort(500, description=f'Station function failed: {error}')

    return {
        'status': 'ok',
        'name': function_name,
        'message': result or f'{definition["label"]} completed.',
    }

@app.route('/action/one', methods=['POST'])
def action_one():
    with stepper_lock:
        stepper.action_one()
    return {'status': 'ok'}

@app.route('/motor/move', methods=['POST'])
def motor_move():
    data = request.get_json(silent=True) or {}
    try:
        motor_index = int(data['motor'])
        steps = int(data['steps'])
    except (KeyError, TypeError, ValueError):
        abort(400, description='Invalid motor selection or increment')

    if not 0 <= motor_index < MOTOR_COUNT:
        abort(400, description='Invalid motor selection')

    if abs(steps) not in MOTOR_INCREMENTS:
        abort(400, description='Unsupported motor increment')

    with stepper_lock:
        stepper.move(motor_index, steps)

    return {'status': 'ok', 'motor': motor_index + 1, 'steps': steps}

@app.route('/image-station/live')
def image_station_live():
    return render_template('image_station_live.html')

def process_instructions(header):
    match header['Station']:
        case 'image-station':
            image_station.process_instruction(header['instruction'])
        case 'sdc':
            pass
        case _:
            raise ValueError("Unknown machine name")

@app.route('/')
def index():
    print(request.headers)
    if 'station' in request.headers:
        process_instructions(request.headers)
    else:
        return render_template('index.html')
    return "Something went wrong!"

if __name__ == "__main__":
    if ip_type=="PUBLIC":
        host = "0.0.0.0"
        print("----------WARNING----------\nRUNNING ON PUBLIC IP")
    else:
        host="100.107.255.14"
    app.run(host=host, port=80, threaded=True)