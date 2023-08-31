import grpc
import Proto.result_pb2 as result_pb2
import Proto.result_pb2_grpc as result_pb2_grpc
import threading
import os
import cv2
import queue
from concurrent import futures
from ultralytics import YOLO
from dotenv import load_dotenv
from flask import Flask, request, url_for, redirect, render_template, Response
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from Utils.analyzer import analyzer
from Utils.user_util import User, find_user

load_dotenv()
app = Flask(__name__)
app.secret_key = os.urandom(12)
login_manager = LoginManager()
login_manager.init_app(app)

img_queue = queue.Queue()
current_system_status = threading.Event()
client_setting_lock = threading.Lock()
client_setting_value = result_pb2.OptVal()
result_condition = threading.Condition()
result_buf = None
a=analyzer()

class VideoCollector(threading.Thread):
    def __init__(self,):
        super().__init__()

    def run(self):
        while(True):
            try:
                cap = cv2.VideoCapture(os.getenv("HTTP_VIDEO_URL"))
                print("VC thread start")
                while(True):
                    ret, frame = cap.read()
                    if ret and img_queue.qsize() < 4 :
                        img_queue.put(cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE))
            except:
                continue


class Result(result_pb2_grpc.ResultServicer):
    def __init__(self, model):
        super(Result, self).__init__()
        self.model = model

    def Require(self, request, context):
        global a
        global result_buf
        global result_condition
        while(current_system_status.is_set()):
            if img_queue.qsize() > 0 :
                frame = img_queue.get()
                result = self.model(frame, verbose=False, conf=float(os.getenv("CONF")))[0]
                resp = result_pb2.Res(response=a.analyze(result=result))
                with result_condition:
                    result_buf = result.plot()
                    result_condition.notify_all()
                yield resp

    def Option(self, request, context):
        while(not current_system_status.is_set()):
            client_setting_lock.acquire()
            yield client_setting_value

class GRPCThread(threading.Thread):
    def __init__(self, model):
        super().__init__()
        self.model = model

    def run(self):
        grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        result_pb2_grpc.add_ResultServicer_to_server(Result(model=self.model), grpc_server)
        grpc_server.add_insecure_port("[::]:50051")
        grpc_server.start()
        print("GRPC server start")
        grpc_server.wait_for_termination()

@login_manager.user_loader
def user_loader(user_id):
    return find_user(user_id)

@app.route('/', methods=['GET','POST'])
def login():
    if request.method=='GET':
        if current_user.is_authenticated:
            return redirect(url_for('setting'))
        else:
            return render_template("login.html")
    user_id = request.form.get("user_id")
    password = request.form.get("password")
    user = User(user_id)
    if user.is_exist():
        if user.can_login(password):
            user = find_user(user_id)
            login_user(user, remember=True)
            return redirect(url_for('setting'))
        else:
            return render_template("login.html", flag="wrong")
    else:
        return render_template("login.html", flag="nodata")

@app.route('/setting', methods=['GET', 'POST'])
@login_required
def setting():
    global current_system_status
    global client_setting_lock
    global client_setting_value
    global a
    if request.method=='GET':
        if current_system_status.is_set():
            return render_template("setting.html", system_status="run", message="")
        else:
            return render_template("setting.html", system_status="stop", message="")
    else:
        if request.form['action'] == 'bopen':
            client_setting_value = result_pb2.OptVal(\
                manual_flag = True, manual = True, letsgo_flag=False, letsgo = False)
            client_setting_lock.release()
            return render_template("setting.html", system_status="stop", message="볼라드가 열렸습니다")

        elif request.form['action'] == 'bclose':
            client_setting_value = result_pb2.OptVal(\
                manual_flag = True, manual = False, letsgo_flag=False, letsgo = False)
            client_setting_lock.release()
            return render_template("setting.html", system_status="stop", message="볼라드가 닫혔습니다")

        elif request.form['action'] == 'server':
            occupy_ratio = request.form.get("occupy_ratio")
            maintain_frame = request.form.get("maintain_frame")
            target_object=request.form.get("target_object")
            a=analyzer(occupy_ratio, maintain_frame, target_object)
            print(a.target_object, a.maintain_frame, a.occupy_ratio)
            return render_template("setting.html", system_status="stop", message="서버 설정 완료")

        elif request.form['action'] == 'stop_bollard':
            current_system_status.clear()
            return render_template("setting.html", system_status="stop", message="시스템이 정지되었습니다")

        elif request.form['action'] == 'run_bollard':
            client_setting_value = result_pb2.OptVal(\
                manual_flag = False, manual = False, letsgo_flag=True, letsgo = True)
            client_setting_lock.release()
            current_system_status.set()
            return render_template("setting.html", system_status="run", message="시스템이 시작되었습니다")

        elif request.form['action'] == 'logout':
            user = current_user
            user.authenticated = False
            logout_user()
            return redirect(url_for('login'))

def result_streamer():
    while True:
        with result_condition:
            result_condition.wait()
            _, img = cv2.imencode('.jpg', result_buf)
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + img.tobytes() + b'\r\n')

@app.route('/stream')
def stream():
    return render_template("stream.html")

@app.route('/mjpeg')
def mjpeg():
    return Response(result_streamer(), mimetype='multipart/x-mixed-replace; boundary=frame')

def main():
    model = YOLO(os.getenv("YOLO_MODEL"))
    try:
        current_system_status.clear()
        client_setting_lock.acquire()

        VC_thread = VideoCollector()
        VC_thread.setDaemon(True)
        VC_thread.start()

        GRPC_thread = GRPCThread(model)
        GRPC_thread.setDaemon(True)
        GRPC_thread.start()

        app.run(host="0.0.0.0", port=80, threaded=True)

    except Exception as e:
        print(type(e))
        print(e)
    finally:
        print("server down")
        #cv2.destroyAllWindows()

if __name__ == "__main__":
    main()