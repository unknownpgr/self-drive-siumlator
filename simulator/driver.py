import cv2
import math


class Driver:
    def drive(self, image):
        IMG_WIDTH = 320
        IMG_HEIGHT = 240
        CENTER = IMG_WIDTH//2
        DETECT_LINE = 70
        DETECT_DIST = 130

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h = hsv[:, :, 0]
        h[h < 20] = 0
        h[h > 40] = 0
        h[h > 0] = 255

        roi = h[DETECT_LINE-2:DETECT_LINE+2, :]

        max_score = -1
        optimal_center = 0
        for i in range(-100, 100):
            center = CENTER+i
            left = center-DETECT_DIST
            right = center+DETECT_DIST

            score_left = sum(
                roi[:, left]) if left >= 0 and left < IMG_WIDTH else 0
            score_right = sum(
                roi[:, right]) if right >= 0 and right < IMG_WIDTH else 0

            score_total = score_left+score_right
            if score_total > max_score:
                max_score = score_total
                optimal_center = center

        image[DETECT_LINE, :] = [0, 0, 255]

        line_right = optimal_center+DETECT_DIST
        line_left = optimal_center-DETECT_DIST
        if line_left >= 0 and line_left < IMG_WIDTH:
            image[:, line_left] = [255, 0, 0]
        if line_right >= 0 and line_right < IMG_WIDTH:
            image[:, line_right] = [0, 255, 0]

        # The range of optimal_center is 0 to IMG_WIDTH(which is CENTER*2).
        # Convert it to -1 to 1
        steering = (optimal_center-CENTER)/CENTER
        # And multiply appropriate constant
        steering *= 2

        cv2.imshow('detect line', image)
        cv2.imshow('roi', roi)
        cv2.waitKey(1)

        return {
            'speed': 0.2,
            'steering': steering
        }


if __name__ == '__main__':
    driver = Driver()
    test_image = cv2.imread('test.png')
    cv2.imshow('original', test_image)
    result = driver.drive(test_image)
    print(result)
    cv2.waitKey(0)
