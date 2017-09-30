import threading
import matplotlib.pyplot as plt

# class that displays the max correlation values in a plot
class MaxCorrWindow:

    is_running = False
    is_paused = False
    has_started = False

    def __init__(self, tracking_thread):
        self.thread = threading.Thread(target=self.run)
        self.i = 0
        self.x = list()
        self.y = list()
        self.tthread = tracking_thread

    def run(self):
        print("running")
        self.is_running = True
        self.is_paused = False
        start_plotting(self)

    def start(self):
        if not self.has_started:
            self.thread.start()
        else:
            self.thread.run()

    def pause(self):
        self.is_paused = True

    def join(self):
        self.is_running = False
        self.thread.join()
        plt.close()


def start_plotting(self):
    try:
        plt.ion()
        plt.figure('Max correlation values')
        print(self.tthread.__class__.__name__)
        while self.is_running:
            if not self.is_paused:
                self.x.append(self.i)
                plt.scatter(self.i, self.tthread.corr)
                self.i += 1
                plt.show()
                plt.pause(0.0001)
            else:
                plt.pause(.5) # when paused, update every half second
        plt.show()
        plt.waitforbuttonpress()
    except Exception as e:
        print(str(e))
    finally:
        plt.close()
