import cv2
import math


class Driver:
    def __init__(self):
        self.time = 0

    def drive(self, image):
        self.time += 1
        return {
            'speed': 3,
            'steer': math.sin(self.time)
        }
