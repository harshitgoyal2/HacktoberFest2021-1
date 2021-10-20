import cv2
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from datetime import datetime

class ControlPanel(GridLayout):

    def startVideo(self, event):
        self.start.disabled = True
        self.stop.disabled = False

        frame_w = int(self.MainLayout.capture.get(3))
        frame_h = int(self.MainLayout.capture.get(4))
        size = (frame_w, frame_h)
        now = datetime.now()
        date_time = now.strftime("%m-%d-%Y-%H-%M-%S")
        self.videowriter = cv2.VideoWriter(date_time+".avi", cv2.VideoWriter_fourcc(*'MJPG'), 10, size)
        self.videoClock = Clock.schedule_interval(self.write_frame, 1 / 30)

    def write_frame(self, event):
        self.videowriter.write(self.MainLayout.frame)

    def stopVideo(self, event):
        self.start.disabled = False
        self.stop.disabled = True
        self.videowriter.release()
        self.videoClock.release()

    def saveImage(self, event):
        frame = self.MainLayout.frame
        if frame is not None:
            now = datetime.now()
            date_time = now.strftime("%m-%d-%Y-%H-%M-%S")
            cv2.imwrite(date_time + '.png', frame)

    def __init__(self, MainLayout, **kwargs):
        super(ControlPanel, self).__init__(**kwargs)
        self.videowriter=None
        self.cols = 3
        self.MainLayout = MainLayout
        self.click = Button(background_normal='camera.jpg',
                            size=(32, 32))
        self.start = Button(background_normal='videoon.jpg',
                            size=(32, 32))
        self.stop = Button(background_normal='videooff.jpg',
                           size=(32, 32))
        self.video = False
        """self.start1 = Button(text="Screen Recorder", font_size="20sp",
                             background_color=(1, 0, 0, 1),

                             size=(32, 32))
        self.stop1 = Button(text="Stop Screen Recorder", font_size="16sp",
                            background_color=(1, 0, 0, 1),

                            size=(32, 32))"""

        self.add_widget(self.click)
        self.add_widget(self.start)
        self.add_widget(self.stop)
        """self.add_widget(self.start1)
        self.add_widget(self.stop1)"""
        self.click.bind(on_press=self.saveImage)
        self.start.bind(on_press=self.startVideo)
        self.stop.bind(on_press=self.stopVideo)

class MainLayout(GridLayout):

    def Update(self, event):
        retval, frame = self.capture.read()
        if retval:
            self.frame = frame
            flip = frame[::-1]
            buf = flip.tostring()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt="bgr")
            texture.blit_buffer(buf, colorfmt="bgr", bufferfmt="ubyte")

            self.image.texture = texture

    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        self.frame = None
        self.capture = cv2.VideoCapture(0)
        self.rows = 2
        self.image = Image()
        self.control = ControlPanel(self)
        self.add_widget(self.image)
        self.add_widget(self.control)
        Clock.schedule_interval(self.Update, 1 / 50)


class desktopCameraApp(App):
    def build(self):
        return MainLayout()
