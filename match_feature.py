import cv2
import numpy as np

# initiate orb and brute force matcher
orb = cv2.ORB_create(nfeatures=200000, scoreType=cv2.ORB_FAST_SCORE)
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)


def initialize_template(template):
    _template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    kp_temp, desc_temp = orb.detectAndCompute(_template, None)
    return kp_temp, desc_temp, _template


def match_feature_on_frame(frame, template, kp_temp, desc_temp, main):

    # convert to grayscale
    _frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # calculate keypoints and descriptors
    kp_frame, desc_frame = orb.detectAndCompute(_frame, None)

    #compute matches between descriptors
    matches = bf.match(desc_temp, desc_frame)

    # filter matches based on set threshold
    best_matches = []
    for m in matches:
        if m.distance < main.match_dist_thresh:
            best_matches.append(m)

    if len(best_matches) > 9:

        src_pts = np.float32([kp_temp[m.queryIdx].pt for m in best_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp_frame[m.trainIdx].pt for m in best_matches]).reshape(-1, 1, 2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 1.0)

        h, w = template.shape
        pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, M)

        frame = cv2.polylines(frame, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)

    else:
        cv2.putText(frame, "Not enough matches, set larger image", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, .75,(255, 0, 0), 2)

    return frame
