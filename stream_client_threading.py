import cv2
import threading
import os
from ultralytics import YOLO
from dotenv import load_dotenv

load_dotenv()
img_queue = []
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
                cv2.imshow('result', result)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                lock.release()

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

        OD_thread.join()
    except Exception as e:
        print(type(e))
        print(e)
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()