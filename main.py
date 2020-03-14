
import cv2 as cv2
import time
import numpy as np


# GREEN
Hmin = 42
Hmax = 92
Smin = 62
Smax = 255
Vmin = 63
Vmax = 235

# RED
# Hmin = 0
# Hmax = 179
# Smin = 131
# Smax = 255
# Vmin = 126
# Vmax = 255



rangeMin = np.array([Hmin, Smin, Vmin], np.uint8)
rangeMax = np.array([Hmax, Smax, Vmax], np.uint8)


minArea = 50

# cv2.NamedWindow("Entrada")
# cv2.NamedWindow("HSV")
# cv2.NamedWindow("Thre")
# cv2.NamedWindow("Erosao")

capture = cv2.VideoCapture(0)


width = 160
height = 120
minArea = 50
centerx=(width/2)*2
centery=(height/2)*2
L_x = height/2.5
L_y= width/5


if capture.isOpened():
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


def img_processing(img_color):
    imgMedian = cv2.medianBlur(img_color, 1)
    imgHSV = cv2.cvtColor(imgMedian, cv2.COLOR_BGR2HSV)
    # imgErode = cv2.inRange(imgHSV, rangeMin, rangeMax)
    imgThresh = cv2.inRange(imgHSV, rangeMin, rangeMax)
    imgErode = cv2.erode(imgThresh, None, iterations=3)
    return imgErode

while True:
    ret, img_color = capture.read()
    processed_image = img_processing(img_color)
    moments = cv2.moments(processed_image , True)
    if moments['m00'] >= minArea:
        x = moments['m10'] / moments['m00']
        y = moments['m01'] / moments['m00']
        print(x, ", ", y)
        cv2.circle(img_color, (int(x), int(y)), 5, (0, 255, 0), -1)


        cv2.line(img_color , (int(x), int(y)), (int(centerx), int(centery)), (0, 255, 0), 1)


        cv2.rectangle(img_color, (0, 220), (160, 120*2), (255, 255, 255), -1)


        cv2.putText(img_color, "the distance: " + str(int(x)) + " , " + str(int(y)), (0, 234), cv2.FONT_HERSHEY_COMPLEX_SMALL,.5, (0, 0, 0))

    else:
        cv2.rectangle(img_color, (0, 220), (160, 120*2), (255, 255, 255), -1)
        cv2.putText(img_color, "No object detected", (0, 117*2), cv2.FONT_HERSHEY_COMPLEX_SMALL, .5, (0, 0, 0))


#############
    # numOfLabelsA, img_labelA, statsA, centroidsA = cv2.connectedComponentsWithStats(processed_image)
    #
    # for idx, centroid in enumerate(centroidsA):
    #     if statsA[idx][0] == 0 and statsA[idx][1] == 0:
    #         continue
    #
    #     if np.any(np.isnan(centroid)):
    #         continue
    #
    #     x, y, width, height, area = statsA[idx]
    #     centerX1, centerY2 = int(centroid[0]), int(centroid[1])
    #
    #     if area > 1500:
    #         cv2.circle(img_color, (centerX1, centerY2), 10, (0, 0, 255), 10)
    #         cv2.rectangle(img_color, (x, y), (x + width, y + height), (0, 0, 255))
#############



    cv2.imshow("img_color", img_color)
    cv2.imshow("processed image",processed_image)

    if cv2.waitKey(10) == 27:
        break
cv2.DestroyAllWindows()
