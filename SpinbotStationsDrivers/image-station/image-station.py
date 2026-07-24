import cv2
import os
import flask
import threading
from datetime import datetime

class imagestation:
    def __init__(self, camera_index=0, capture_dir=None):
        self.cap = cv2.VideoCapture(camera_index, cv2.CAP_V4L2)

        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1600)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1200)

        actual_w = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        actual_h = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        if (actual_w, actual_h) != (1600, 1200):
            raise RuntimeError(
                f"Camera did not accept requested resolution: "
                f"requested 1600x1200, got {int(actual_w)}x{int(actual_h)}"
            )
        
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

    def capture(self) -> bytes:
        """Grabs a single frame from the camera and returns it as
        JPEG-encoded bytes
        """
        self.check_camera()
        status, frame = self.cap.read()
        if not status:
            raise RuntimeError("Failed to read frame from camera")
        
        success, buffer = cv2.imencode('.jpg', frame)
        if not success:
            raise RuntimeError("Failed to encode from as JPEG")
        
        return buffer.tobytes()

    def start_stream(self):
        #TODO Need to finish this section
        pass

    def generate_frames(self):
        cam = cv2.VideoCapture(0)
        if not self.check_camera():
            return
        
        while True:
            success, frame = cam.read()
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

