import cv2
import asyncio
import os
from ultralytics import YOLO
from dotenv import load_dotenv

load_dotenv()
img_queue = []

async def VideoCollector(cap):
    ret, frame = cap.read()
    if len(img_queue) < 4 :
        img_queue.append(frame)

async def ObjectDetector(model):
    if len(img_queue) > 0 :
        frame = img_queue.pop(0)
        result = model(frame, verbose=False, conf=os.getenv("CONF"))[0].plot()
        cv2.imshow('result', result)

async def main():
    model = YOLO(os.getenv("YOLO_MODEL"))
    try:
        cap = cv2.VideoCapture(os.getenv("TCP_VIDEO_URL"))
        while(True):
            await VideoCollector(cap)
            await ObjectDetector(model)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except Exception as e:
        print(type(e))
        print(e)
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    asyncio.run(main())


