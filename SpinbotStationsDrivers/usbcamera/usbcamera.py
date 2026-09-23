import cv2

class usbcamera:
    def __init__(self, camera_index=0, width=1920, height=1080):
        self.cap = cv2.VideoCapture(camera_index, cv2.CAP_V4L2)

        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        self.check_camera()

    def check_camera(self) -> bool:
        if not self.cap.isOpened():
            raise RuntimeError("Could not open camera")
        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Can't receive frame")
        return True

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