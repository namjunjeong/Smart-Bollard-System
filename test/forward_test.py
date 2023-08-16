from ultralytics import YOLO
model = YOLO('best.pt')
results = model('testimg1.jpg', save=True)