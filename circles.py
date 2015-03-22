# -*- coding: utf-8 -*-
import numpy as np
import cv2

video_capture = cv2.VideoCapture(0)

while(1):
    ret, image = video_capture.read()
    output = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 1.2, 100)
    # ensure at least some circles were found
    if circles is not None:
    # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")
    # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
    # draw the circle in the output image, then draw a rectangle
    # corresponding to the center of the circle
            cv2.circle(output, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

    # show the output image
        cv2.imshow("output", np.hstack([image, output]))

    k = cv2.waitKey(30) & 0xFF

    if k == 27:
        break
video_capture.release()
cv2.destroyAllWindows()
