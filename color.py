# -*- coding: utf-8 -*-
import numpy as np
import cv2


video_capture = cv2.VideoCapture(0)

while(1):
    ret, image = video_capture.read()

    boundaries = [
        ([0, 0, 128], [155, 120, 255])
    ]

    for (lower, upper) in boundaries:
        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")

        mask = cv2.inRange(image, lower, upper)
        output = cv2.bitwise_and(image, image, mask=mask)

        # show the images
        cv2.imshow("images", np.hstack([image, output]))
    k = cv2.waitKey(30) & 0xFF

    if k == 27:
        break
video_capture.release()
cv2.destroyAllWindows()
