import cv2
import os
import io
from flask import abort, send_file
from time import sleep

class imagestation:
    def __init__(self, camera_index=0, width=1280, height=800, capture_dir=None):

        self.cap = cv2.VideoCapture(camera_index, cv2.CAP_V4L2)

        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        self.check_camera()

        self.capture_dir = capture_dir if capture_dir else os.path.join(os.getcwd(), "captures")
        if not os.path.exists(self.capture_dir):
            os.makedirs(self.capture_dir)

    def check_camera(self) -> bool:
        if not self.cap.isOpened():
            raise RuntimeError("Could not open camera")
        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Can't receive frame")
        return True

    def capture(self):
        """Grabs a single frame from the camera and returns it as
        a PNG download response
        """
        self.check_camera()
        status, frame = self.cap.read()
        if not status:
            raise RuntimeError("Failed to read frame from camera")
        
        success, buffer = cv2.imencode('.png', frame)
        if not success:
            raise RuntimeError("Failed to encode frame as PNG")

        sleep (10)
        
        return send_file(
            io.BytesIO(buffer.tobytes()),
            mimetype="image/png",
            as_attachment=True,
            download_name="capture.png"
        )

    def generate_frames(self):
        while True:
            success, frame = self.cap.read()
            if not success:
                break
            success, buffer = cv2.imencode('.jpg', frame)
            if not success:
                continue
            frame_bytes = buffer.tobytes()

            yield (
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n'
                + frame_bytes +
                b'\r\n'
            )

    def process_instruction(self, ins):
        # parse through instruction to see what needs to be run
        match ins:
            case 'ping':
                print("Returning pong")
                return "pong"
            case 'capture':

                return self.capture()
            case _:  # problem with instruction
                abort(400, description=f"Unknown instruction: {ins}\n")
    