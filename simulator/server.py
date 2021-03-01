from os import path
from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
import cv2
import base64
import numpy as np
from driver import Driver
import json

ROOT = path.join(path.dirname(path.abspath(__file__)), 'public')
print("PUBLIC :", ROOT)

driver = Driver()


class DriverHandler(SimpleHTTPRequestHandler):
    '''
    이 클래스는 가상의 운전자를 시뮬레이션하기 위한 클래스이다. HTTP request를 통해 제어된다.    
    다음과 같은 기능을 가진다.
        - ROOT 변수의 디렉토리에서 정적으로 파일을 서비스한다.
        - /reset 경로로 post요청이 들어올 경우, 운전자를 초기화한다.
        - 그 외 경로로 post요청이 들어올 경우 시뮬레이션 요청이라 가정한다.

    시뮬레이션 요청을 받았을 경우, 요청에 포함된 base64형식의 이미지를 디코딩한 후, driver에 넘긴다.
    이후 driver의 결과값을 string으로 dump한 후 요청에 응답한다.
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def do_POST(self):
        global driver

        if self.path == '/reset':
            print("Driver reset!")
            driver = Driver()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(
                bytes(json.dumps({'STATUS': 'OK'}), encoding='utf-8'))
            return

        data = str(self.rfile.read(
            int(self.headers['Content-Length'])), encoding='utf-8')
        arr = np.frombuffer(base64.b64decode(data), np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        drive_data = driver.drive(img)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes(json.dumps(drive_data), encoding='utf-8'))

    def log_message(self, format, *args):
        '''
        매 호출마다 로그 메시지가 뜨면 다른 print결과를 보기 힘들기 때문에 빈 함수로 오버라이드하여 로그를 제거한다.
        만약 HTTP request로그가 보고싶을 경우, 이 함수에 로그를 출력하는 코드를 삽입하거나 이 함수 자체를 삭제하면 된다.
        '''
        pass


httpd = HTTPServer(("0.0.0.0", 8080), DriverHandler)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("Stop server")
httpd.server_close()
