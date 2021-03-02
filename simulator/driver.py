import cv2


class Driver:
    def drive(self, image):
        '''
        이 함수를 적당히 수정해서 자율주행차를 만드는 것이 목표다.
        image 시뮬레이션 속 모형차의 카메라에서 읽은 이미지가 들어가 있다.
        이 이미지에서 영상처리를 통해 모형차가 주행해야 할 적당한 속도와 조향각을 알아내야 한다.
        아래는 간단한 예제다.
        '''

        IMG_WIDTH = 320
        IMG_HEIGHT = 240

        # 이미지의 가로 중심 위치
        CENTER = IMG_WIDTH//2

        # 차선을 감지할 감지선 높이
        DETECT_LINE = 70

        # 차선의 중심으로부터 좌우 차선까지 떨어진 거리(단위:픽셀)
        DETECT_DIST = 130

        # 노란색 차선을 검출하기 위하여 HSV변환을 수행한다.
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # h(색조)채널만을 골라낸다.
        h = hsv[:, :, 0]

        # 노란색 범위(20~40)이외의 값을 0으로, 노란색 범위 안의 값을 255로 만들어 이진화한다.
        h[h < 20] = 0
        h[h > 40] = 0
        h[h > 0] = 255

        # 이미지에서 일부분을 잘라서 이 부분만 보고 차선인지 아닌지를 판단하기로 한다.
        # DETECT_LINE 위치를 중심으로, 위아래 2픽셀씩 총 4픽셀 두께의 가로 띠 모양의 영역이다.
        roi = h[DETECT_LINE-2:DETECT_LINE+2, :]

        # 차선의 중심을 움직여 보면서, 예측되는 차선의 위치에 실제로 값이 존재하는 픽셀이 몇 개나 되는지를 센다.
        # 차선의 중심 위치를 center라고 가정한 후, 이로부터 유도된 왼쪽 차선의 위치를 left, 오른쪽 차선의 위치를 right라고 하자.
        # 이때 이미지에서 left위치와 right위치에 실제로 255인 픽셀이 많이 있다면, center는 실제 차선의 중심 위치일 가능성이 높다.
        # 이런 방법을 통해서 가장 차선의 중심이 있을 법한 위치인 optimal_center를 알아낸다.
        max_score = -1
        optimal_center = 0
        for dist in range(-100, 100):
            center = CENTER+dist
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

        # 이 부분들은 그냥 그림을 그리기 위한 부분들이다.
        # 차선 감지선과 예측된 왼쪽, 오른쪽 차선 위치를 이미지에 그려준다
        image[DETECT_LINE, :] = [0, 0, 255]
        line_right = optimal_center+DETECT_DIST
        line_left = optimal_center-DETECT_DIST
        if line_left >= 0 and line_left < IMG_WIDTH:
            image[:, line_left] = [255, 0, 0]
        if line_right >= 0 and line_right < IMG_WIDTH:
            image[:, line_right] = [0, 255, 0]
        cv2.imshow('detect line', image)
        cv2.imshow('roi', roi)
        cv2.waitKey(1)

        # 앞서 결정한 optimal_cetner 값은 0~이미지 가로길이 범위를 가진다.
        # 이 값을 -1~+1범위로 바꿔줘서 방향 조절에 이용할 수 있도록 한다.
        steering = (optimal_center-CENTER)/CENTER

        # 마지막으로, 적절한 값을 곱해서 조향해준다.
        # 2를 곱했으므로 조향 범위가 -2~+2까지이다. 이는 각도로 따지면 115도정도 된다.
        # 물론 실제 차는 90도 이상으로 조향할 수 없지만, 시뮬레이션이므로 어쨌거나 되기는 한다.
        steering *= 2

        # 따라서 시뮬레이션을 좀 더 현실적으로 만들기 위해 steering에 90도 제한을 준다.
        if steering > 3.14/2:
            steering = 3.14/2
        if steering < -3.14/2:
            steering = 3.14/2

        # 마지막으로, 적절한 속도와 조향값을 반환한다.
        # 항상 이렇게 두 값을 전부 반환할 필요는 없으며,
        # {'speed':0.2}와 같이 속도만 반환하거나 steering값만 반환해도 된다.
        # 그럴 경우, 반환한 값만 업데이트되고 반환하지 않은 값은 이전과 동일하게 유지된다.
        return {
            'speed': 0.2,
            'steering': steering
        }


if __name__ == '__main__':
    '''
    이 부분은 테스트를 위한 코드다. 이 코드는 server.py를 통해 driver.py가 실행될 경우에는 실행되지 않으며,
    driver.py가 직접 실행될 경우에만 실행된다.

    영상처리를 시험해보기 위해 웹 브라우저에서 매번 시뮬레이션을 실행하려면 번거로울 것이다.
    그래서 driver.py를 바로 실행시킬 경우, test.png파일 딱 하나만을 읽어서 그 결과를 출력하도록 만들었다.
    물론 OpenCV에 익숙한 사람이라면, 이 부분을 적당히 수정하여 여러 파일을 입력받거나 영상을 입력받도록 구성하는 것도 가능하다.
    '''

    # 테스트를 위해 드라이버 객체를 만든다.
    driver = Driver()

    # 테스트를 위한 이미지를 읽어온다.
    test_image = cv2.imread('test.png')

    # 원본 이미지를 띄운다.
    cv2.imshow('original', test_image)

    # 드라이버 객체에 이미지를 입력하고 결과값을 가져온다.
    result = driver.drive(test_image)

    # 결과를 출력한다.
    print(result)

    # 사용자가 아무 키나 누를 때까지 기다린다.
    cv2.waitKey(0)
