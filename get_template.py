import cv2


def run(im, window_name):
    im_disp = im.copy()

    # List containing top-left and bottom-right to crop the image.
    pts_1 = []
    pts_2 = []

    rects = []
    run.mouse_down = False

    run.point_drawing_complete = False

    def callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            run.mouse_down = True
            pts_1.append((x, y))
        elif event == cv2.EVENT_LBUTTONUP and run.mouse_down == True:
            run.mouse_down = False
            pts_2.append((x, y))
            run.point_drawing_complete = True
        elif event == cv2.EVENT_MOUSEMOVE and run.mouse_down == True:
            im_draw = im.copy()
            cv2.rectangle(im_draw, pts_1[-1], (x, y), (57, 255, 20), 3)
            cv2.imshow(window_name, im_draw)

    cv2.setMouseCallback(window_name, callback)

    while not run.point_drawing_complete:
        # Draw the rectangular boxes on the image
        window_name_2 = window_name
        for pt1, pt2 in zip(pts_1, pts_2):
            rects.append([pt1[0], pt2[0], pt1[1], pt2[1]])
            cv2.rectangle(im_disp, pt1, pt2, (57, 255, 20), 3)
        # Display the cropped images
        cv2.namedWindow(window_name_2, cv2.WINDOW_NORMAL)
        cv2.imshow(window_name_2, im_disp)
        key = cv2.waitKey(30)
        if key == ord('p'):
            # Press key `s` to return the selected points
            cv2.destroyAllWindows()
            point = [(tl + br) for tl, br in zip(pts_1, pts_2)]
            corrected_point=check_point(point)
            return corrected_point

    point = [(tl + br) for tl, br in zip(pts_1, pts_2)]
    tl, br = check_point(point)

    return tl, br

# ensure points are within bounds of image
def check_point(points):
    for point in points:
        tl = (min(point[0], point[2]), min(point[1], point[3]))
        br = (max(point[0], point[2]), max(point[1], point[3]))

    return tl, br


