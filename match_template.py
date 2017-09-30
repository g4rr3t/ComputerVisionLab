import cv2


def match_template(frame, template, lsf_selection):
    match_method = lsf_selection  # cv2.getTrackbarPos(trackbar_label, self.name)
    correlation_map = cv2.matchTemplate(frame, template, match_method)
    min_c2, max_c2, _, _ = cv2.minMaxLoc(correlation_map)
    cv2.normalize(correlation_map, correlation_map, 0, 1, cv2.NORM_MINMAX, -1)

    min_c, max_c, min_loc, max_loc = cv2.minMaxLoc(correlation_map)
    if match_method == cv2.TM_SQDIFF or match_method == cv2.TM_SQDIFF_NORMED:
        tl = min_loc
        corr = min_c2
    else:
        tl = max_loc
        corr = max_c2

    return frame, tl, corr, correlation_map
# displayed image, matched template location, highest correlation value, correlation map

