import cv2, numpy as np


class Kalman2Dimension():

    def __init__(self):
        self.kalman = cv2.KalmanFilter(4,2)  # 4 dim state, 2 dimension measurements (x and y)
        self.kalman.measurementMatrix = np.array([[1,0,0,0],[0,1,0,0]],np.float32)
        self.kalman.transitionMatrix = np.array([[1,0,1,0],[0,1,0,1],[0,0,1,0],[0,0,0,1]],np.float32)
        self.kalman.processNoiseCov = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]],np.float32) * 0.03

    def predict(self):
        pred = self.kalman.predict()
        pred_tl = (int(pred[0]), int(pred[1]))
        return pred_tl

    def correct(self, tl):
        corrected = self.kalman.correct(np.array([[np.float32(tl[0])], [np.float32(tl[1])]]))
        return corrected[0], corrected[1]


class Kalman1Dimension():

    error_variance = 0.5 ** 2   # how quickly the kalman filter adapts to changes (higher = slower to adapt)
                                # or how well the measurement values should be trusted

    def __init__(self, inital_state):
        self.xhat = inital_state   # saved state
        self.p = .1               # error variance

    def predict(self):
        return self.xhat

    def correct(self, x):
        kalman_gain = self.p / (self.p +self.error_variance)
        self.xhat = self.xhat + kalman_gain * (x - self.xhat)
        self.p = (1 - kalman_gain) * self.p
        return self.xhat



