import cv2
import threading
import os
from ultralytics import YOLO
from dotenv import load_dotenv
from flask import Flask, render_template, Response

load_dotenv()
img_queue = []
result_queue = []
lock = threading.Lock()

class VideoCollector(threading.Thread):
    def __init__(self, cap):
        super().__init__()
        self.cap = cap

    def run(self):
        print("VC thread start")
        while(True):
            ret, frame = self.cap.read()
            lock.acquire()
            if len(img_queue) < 4 :
                img_queue.append(frame)
            lock.release()

class ObjectDetector(threading.Thread):
    def __init__(self, model):
        super().__init__()
        self.model = model

    def run(self):
        print("OD thread start")
        while(True):
            lock.acquire()
            if len(img_queue) > 0 :
                frame = img_queue.pop(0)
                lock.release()
                result = self.model(frame, verbose=False)[0].plot()
                result_queue.append(result)
            else:
                lock.release()

app = Flask(__name__)

@app.route('/')
def video_show():
    return render_template('video_show.html')

def gen_frames():
    while True:
        try:
            ret, buffer = cv2.imencode('.jpg', result_queue.pop(0))
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except:
            continue

@app.route('/video')
def video():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def main():
    model = YOLO(os.getenv("YOLO_MODEL"))
    try:
        cap = cv2.VideoCapture(os.getenv("TCP_VIDEO_URL"))
        VC_thread = VideoCollector(cap)
        VC_thread.setDaemon(True)
        OD_thread = ObjectDetector(model)
        OD_thread.setDaemon(True)
        VC_thread.start()
        OD_thread.start()

        app.run(host = "0.0.0.0", port = 80)
    except Exception as e:
        print(type(e))
        print(e)
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()