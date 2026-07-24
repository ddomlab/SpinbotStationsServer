"""
Simple flask server

Routes:
    /               -> Public landing page
    /imagestation   -> Requires API key
            - "ping" - confirms server status
            - "capture" - returns jpeg img
"""

from flask import Flask, request, send_file, abort, Response, render_template
from auth import require_http_api_key
from SpinbotStationsDrivers import imagestation
import io
import cv2
import threading

app = Flask(__name__)
station = imagestation()

camera_lock = threading.Lock()

@app.route("/image-station")
@require_http_api_key
def run():
    match request.headers['instruction']:
        case 'ping':
            pass
        case 'capture':
            try:
                with camera_lock:
                    image_bytes = station.capture()
            except RuntimeError as e:
                abort(500, description=str(e))

            return send_file(
                io.BytesIO(image_bytes),
                mimetype="image/jpeg",
                as_attachment=False,
                download_name="capture.jpg"
            )
        case 'pump':
            amount = request.headers['amount']
            pass
        case _:  # problem with instruction
            abort(400, description=f"Unknown instruction: {request.headers['instruction']!r}")

    return "Done"


def generate_frames():
    try:
        while True:
            with camera_lock:
                if not station.check_camera():
                    break
                success, frame = station.cap.read()

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


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host="100.107.255.14", port=80, threaded=True)