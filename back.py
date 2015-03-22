# -*- coding: utf-8 -*-
import numpy as np
import cv2

video_capture = cv2.VideoCapture(0)
fgbg = cv2.createBackgroundSubtractorMOG()

while(1):
    ret, frame = video_capture.read()
    fgmask = fgbg.apply(frame)

    cv2.imshow('frame', fgmask)
    k = cv2.waitKey(30) & 0xFF

    if k == 27:
        break
video_capture.release()
cv2.destroyAllWindows()
