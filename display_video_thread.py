import threading
import cv2
import get_template
from apply_filter import apply_filter
from max_corr_thread import MaxCorrWindow
from kalman_filter import Kalman2Dimension, Kalman1Dimension
import match_template
import match_feature
import lowes_ratio_test


class DisplayVideoThread(threading.Thread):

    is_running = False
    corr = 0.5

    def __init__(self, name, video_file, main):
        threading.Thread.__init__(self)
        self.video_file = video_file
        self.name = name
        self.main = main
        self.method = 3

    def run(self):
        self.is_running = True
        display_tracking(self)

    def stop(self):
        self.is_running = False


def nothing(x):
    pass


def display_tracking(self):

    rec_init = False
    plot_init = False

    if len(self.main.video_file) == 0:
        cap = cv2.VideoCapture(0)
        is_from_file = False
    else:
        is_from_file = True
        cap = cv2.VideoCapture(self.main.video_file)
        if not cap.isOpened():
            print("Cannot open video file ", self.main.video_file)
            return
        fps = cap.get(5)

    cv2.namedWindow(self.name)

    # initialize max corr window
    max_corr_window = MaxCorrWindow(self)

    # try:
    play_forward = True
    tracking = False
    ret, frame = cap.read()
    template = []  # array of pixels containting template image
    template_height = 0
    template_width = 0
    neon_green = (57, 255, 20) # b, g, r
    yellow = (0, 255, 255)
    is_match_template = True

    #max corr calculation
    frame_count = 0.0
    sum_of_corr = 0.0
    corr_ratio = 0.0
    lowes_ratio = 0.0
    lowes_ratio2 = 0.0

    kalman_2_dim = Kalman2Dimension()
    kalman_1_dim = Kalman1Dimension(lowes_ratio)

    while self.is_running and ret:

        # match template after template/query image was set
        if tracking:
            # get query image
            if self.main.is_feature_matching:
                frame = match_feature.match_feature_on_frame(frame, _template, kp_temp, desc_temp, self.main)

            else:
                # get template
                frame, tl, self.corr, correlation_map \
                        = match_template.match_template(frame, template, self.main.lsf_selection)

                # calculate sum max_corr
                frame_count += 1.0
                sum_of_corr += self.corr

                # calc and display mean corr value
                if frame_count > 8:
                    self.main.mean_corr = "{0:.2f}".format(sum_of_corr / frame_count)
                    corr_ratio = sum_of_corr / frame_count * self.main.corr_threshold_mean

                # conduct lowes ratio test
                if self.main.lowes_ratio < 1.0:
                    lowes_ratio = lowes_ratio_test.get_ratio(correlation_map, template_height, template_width)

                # auto detect failure with kalman filtered 2nd Lowes ratio
                if self.main.is_auto_detect_failure:
                    lowes_ratio = lowes_ratio_test.get_ratio(correlation_map, template_height, template_width)
                    lowes_ratio2 = kalman_1_dim.correct(
                        lowes_ratio_test.get_ratio(correlation_map, template_height, template_width))

                #print(lowes_ratio, "    ",self.main.lowes_ratio)

                # if object was detected
                if self.corr > self.main.corr_threshold \
                and self.corr > corr_ratio\
                and self.main.lowes_ratio >= lowes_ratio\
                and (not self.main.is_auto_detect_failure or lowes_ratio + .02 <= lowes_ratio2):  # .02 accounts for floating point errors

                    if self.main.is_kalman:
                        kalman_2_dim.predict()
                        tl = kalman_2_dim.correct(tl)  # apply filtered value to template location

                    # render track rectangle
                    br = (tl[0] + template_width, tl[1] + template_height)
                    cv2.rectangle(frame, tl, br, neon_green, 3)

                # object was not detected (threshold not met)
                else:
                    # go with the kalman prediction if enabled
                    if self.main.is_kalman:
                        tl = kalman_2_dim.predict()
                        br = (tl[0] + template_width, tl[1] + template_height)
                        cv2.rectangle(frame, tl, br, yellow, 3)

                if self.main.display_corr_map:
                    cv2.imshow('correlation values', correlation_map)

                # display max corr plot if enabled
                if self.main.display_max_corr:
                    if not plot_init:
                        max_corr_window.thread.start()
                        plot_init = True
                    else:
                        max_corr_window.is_paused = False
                else:
                    if plot_init:
                        max_corr_window.pause()

        if not tracking:
            cv2.putText(frame, "Press 't' to set template", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, .75, neon_green, 2)

        # handle recording
        if self.main.is_recording:
            if not rec_init:  # initializes the writer only once
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                out = cv2.VideoWriter(self.main.recorded_vid_name, fourcc, 20.0, (640, 480))
                rec_init = True
            out.write(frame)
        else:
            if rec_init:
                out.release()
                print("Recording written to: ", self.main.recorded_vid_name)
            rec_init = False

        cv2.imshow(self.name, frame)

        if is_from_file:
            k = cv2.waitKey(int(1000 / fps))
        else:
            k = cv2.waitKey(33) & 0xff  # attempt to remove platform dependency

        if play_forward:
            ret, frame = cap.read()

        # apply filter
        frame = apply_filter(self.main, frame)

        if k == -1:
            continue

        if k == 27:  # esc to quit
            break

        if k == 112:
            input("Press any key to continue")

        if k == 98:
            is_match_template = not is_match_template

        #if not k == 255:
        #    print(k)

        if k == 116:  # numpad 5 - pause / play
            print("Click and drag mouse on image to define template bounds")
            if play_forward:
                tl, br = get_template.run(frame, self.name)
                cv2.putText(frame, "Press 't' to track", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, .75, neon_green,
                            2)
                template = frame[tl[1]:br[1], tl[0]:br[0]]  # (y1, y2)  (x1, x2)
                template_width = abs(tl[0]-br[0])
                template_height = abs(tl[1]-br[1])
                if (self.main.is_feature_matching):
                    kp_temp, desc_temp, _template = match_feature.initialize_template(template)
                    cv2.drawKeypoints(template, kp_temp, template, color=(0, 255, 0), flags=0)
                cv2.imshow('template', template)
                cv2.rectangle(frame, tl, br, neon_green, 3)
                tracking = True
                frame_count = 0


# except Exception as e:
#     print(str(e))
# finally:
    cv2.destroyAllWindows()
    cap.release()
    if rec_init:
        out.release()
    if plot_init:
        max_corr_window.join()



