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


class HTTPHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def do_POST(self):
        data = str(self.rfile.read(
            int(self.headers['Content-Length'])), encoding='utf-8')
        arr = np.frombuffer(base64.b64decode(data), np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        drive_data = driver.drive(img)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes(json.dumps(drive_data), encoding='utf-8'))


httpd = HTTPServer(("0.0.0.0", 8080), HTTPHandler)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass
httpd.server_close()
