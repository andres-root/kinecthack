# -*- coding: utf-8 -*-
import numpy as np
import cv2

video_capture = cv2.VideoCapture(0)

while(1):
    ret, img = video_capture.read()
    # find Harris corners
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray, 4, 3, 0.04)

    #result is dilated for marking the corners, not important
    dst = cv2.dilate(dst, None)

    # Threshold for an optimal value, it may vary depending on the image.
    img[dst > 0.01 * dst.max()] = [0, 0, 255]

    cv2.imshow('img2',  img)
    k = cv2.waitKey(30) & 0xFF
    if k == 27:
        break
video_capture.release()
cv2.destroyAllWindows()
