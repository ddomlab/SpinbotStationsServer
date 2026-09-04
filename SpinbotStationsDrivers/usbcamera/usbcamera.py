import cv2, os

class usbcamera:
    def __init__(self, camera_index=0, capture_dir=None):
        width = 1280
        height = 800

        self.cap = cv2.VideoCapture(camera_index, cv2.CAP_V4L2)

        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        actual_w = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        actual_h = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        if (actual_w, actual_h) != (width, height):
            raise RuntimeError(
                f"Camera did not accept requested resolution: "
                f"requested {width}x{height}, got {int(actual_w)}x{int(actual_h)}"
            )
        
        self.check_camera()

    def check_camera(self) -> bool:
        if not self.cap.isOpened():
            raise RuntimeError("Could not open camera")
        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Can't receive frame")
        return True

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