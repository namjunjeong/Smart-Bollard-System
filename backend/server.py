import grpc
import Proto.result_pb2 as result_pb2
import Proto.result_pb2_grpc as result_pb2_grpc
import threading
import os
import cv2
from concurrent import futures
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

class GRPCserver(result_pb2_grpc.ResultServicer):
    def __init__(self, model):
        super(GRPCserver, self).__init__()
        self.model = model

    def Require(self, request):
        while(True):
            lock.acquire()
            if len(img_queue) > 0 :
                frame = img_queue.pop(0)
                lock.release()
                result = self.model(frame, verbose=False)[0].boxes.data
                print(result)
                resp = result_pb2.Res()
                resp.response = True
            else:
                lock.release()

def main():
    model = YOLO(os.getenv("YOLO_MODEL"))
    try:
        cap = cv2.VideoCapture(os.getenv("TCP_VIDEO_URL"))
        VC_thread = VideoCollector(cap)
        VC_thread.setDaemon(True)
        VC_thread.start()
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        result_pb2_grpc.add_ResultServicer_to_server(GRPCserver(model=model), server)
        server.add_insecure_port("[::]:50051")
        server.start()
        server.wait_for_termination()
    except Exception as e:
        print(type(e))
        print(e)
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()