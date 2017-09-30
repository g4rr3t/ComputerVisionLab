import os

#the following imports are requred to build the windows executable package with PyInstaller
import sys
import tkinter.filedialog
import matplotlib.pyplot as plt
import threading
import numpy as np
import cv2

from kivy.app import App
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup

from display_video_thread import DisplayVideoThread


# defines the gui layout and handles certain button presses
# most toggles simply modify a boolean, which is read by other classes
class CVLabLayout(BoxLayout):

    # radio buttons
    input_from_camera = True
    input_from_file = False

    # booleans
    is_grayscale = False
    is_lap = False
    is_canny = False
    is_gaussian = False
    is_median = False
    is_bilat = False
    is_circles = False
    is_lines = False
    is_kalman = False
    is_harris = False
    is_shi = False
    is_sift = False
    is_recording = False
    display_corr_map = False
    display_max_corr = False
    is_orb = False
    is_feature_matching = False
    is_auto_detect_failure = False


    # labels
    recorded_vid_name = 'recording.avi'
    video_file = ObjectProperty('')
    video_file_name = ObjectProperty('')
    mean_corr = ObjectProperty('')
    display_video_thread = DisplayVideoThread('tracking thread', video_file, None)
    lsf_selection = 5
    corr_threshold = 0.0
    corr_threshold_mean = 0.0
    match_dist_thresh = 50
    lowes_ratio = 1.0

    # translate spinner to opencv algorithm value
    def lsf_selected(self):
        text = self.ids.alg_spinner.text
        if text == 'Square difference':
            self.lsf_selection = 0
        elif text == 'Normalized Square Diff':
            self.lsf_selection = 1
        elif text == 'Cross Correlation':
            self.lsf_selection = 2
        elif text == 'Normalized Cross Corr':
            self.lsf_selection = 3
        elif text == 'Coefficient':
            self.lsf_selection = 4
        elif text == 'Normalized Corr Coeff':
            self.lsf_selection = 5
        else:
            print('invalid algorithm selection')

    # called when display video is toggled
    def display_video(self, state):
        if state is "down":
            print("Press t to set template")
            try:
                if self.input_from_camera:
                    self.display_video_thread = DisplayVideoThread('video window', '', self)
                else:
                    self.display_video_thread = DisplayVideoThread('video window', self.video_file, self)
                self.display_video_thread.start()
            except Exception as e:
                print("Error starting display video thread", str(e))
        else:
            self.display_video_thread.is_running = False
            self.display_video_thread.join()
            del self.display_video_thread

    # called when record is toggled
    def record_toggled(self, state):
        if state is "down":
            self.recorded_vid_name = self.ids.rec_text_input.text
            self.is_recording = True
        else:
            self.is_recording = False

    # when enter is pressed on corr threshold
    def set_corr_thresh(self):
        self.corr_threshold = float(self.ids.corr_threshold.text)

    def set_corr_thresh_mean(self):
        self.corr_threshold_mean = float(self.ids.corr_thresh_mean.text)

    def set_match_dist_thresh(self):
        self.match_dist_thresh = float(self.ids.match_dist.text)

    def set_lowes(self):
        self.lowes_ratio = float(self.ids.lowes_id.text)

    # show file chooser
    def show_load(self, is_template):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        content.ids.file_chooser.path = os.getcwd()
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    # called when load is pressed on file chooser
    def load(self, path, filename):
        if len(filename) > 0:
            self.video_file = filename[0]
            head, tail = os.path.split(filename[0])
            self.video_file_name = tail
        self.dismiss_popup()

    # required for file chooser
    def dismiss_popup(self):
        self._popup.dismiss()


# class to define the properties of the file chooser
class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


# main class that runs kivy
class CVLabApp(App):
    layout = None

    def build(self):
        self.layout = CVLabLayout()
        return self.layout

    def on_stop(self):
        try:
            self.layout.display_video_thread.stop()
        except Exception as e:
            print(str(e))


if __name__ == '__main__':
    Window.size = (1000, 430)
    CVLabApp().run()

Factory.register('LoadDialog', cls=LoadDialog)
