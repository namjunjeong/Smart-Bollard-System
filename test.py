from ultralytics import YOLO
import cv2
model = YOLO('yolov8n.pt')

result = model("testimg.jpg")[0].plot()
print(type(result))
cv2.imshow('result', result)
cv2.waitKey(0)
cv2.destroyAllWindows()