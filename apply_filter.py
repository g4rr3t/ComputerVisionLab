import cv2
import numpy as np

orb = cv2.ORB_create()
# returns a frame with the filter applied, set by main
def apply_filter(main, frame):
    try:
        if main.is_grayscale:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if main.is_lap:
            frame = cv2.Laplacian(frame, cv2.CV_64F)
        if main.is_canny:
            frame = cv2.Canny(frame, 100, 200)
        if main.is_gaussian:
            frame = cv2.GaussianBlur(frame, (5, 5), 0)
        if main.is_median:
            frame = cv2.medianBlur(frame, 5)
        if main.is_bilat:
            frame = cv2.bilateralFilter(frame, 9, 75, 75)
        if main.is_circles:
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            img = cv2.medianBlur(img, 5)
            circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 100, param1=50, param2=30, minRadius=0,
                                       maxRadius=0)
            if circles is None:
                return
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                # draw the outer circle
                cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
                # draw the center of the circle
                cv2.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 3)
        if main.is_lines:
            if main.is_grayscale or main.is_canny:
                gray = frame
            else:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 150, apertureSize=3)
            minLineLength = 100
            maxLineGap = 10
            lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength, maxLineGap)
            if lines is not None:
                for i in range(len(lines)):
                    for x1, y1, x2, y2 in lines[i]:
                        cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        if main.is_harris:
            if main.is_grayscale or main.is_canny:
                gray = frame
            else:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            dst = cv2.cornerHarris(gray, 2, 3, 0.04)
            dst = cv2.dilate(dst, None)
            frame[dst>0.01*dst.max()] = [0,0,255]
        if main.is_shi:
            if main.is_grayscale or main.is_canny:
                gray = frame
            else:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            corners = cv2.goodFeaturesToTrack(gray, 25, 0.01, 10)
            corners = np.int0(corners)
            for i in corners:
                x, y = i.ravel()
                cv2.circle(frame, (x, y), 3, 255, -1)
        if main.is_orb:
            if main.is_grayscale or main.is_canny:
                gray = frame
            else:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            kp = orb.detect(gray, None)

            kp, des = orb.compute(gray, kp)

            cv2.drawKeypoints(frame, kp, frame, color=(0,255,0), flags=0)






    except Exception as e:
        print(str(e))
    return frame
