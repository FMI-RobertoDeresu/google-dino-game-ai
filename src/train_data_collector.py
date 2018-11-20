import mss
import uuid
from config import config
from mss import tools as mss_tools


class TrainDataCollector:
    def __init__(self, left, top, width, height):
        self.sct = mss.mss()
        self.csv_file = open(config["train_data_csv_filename"], 'a+')
        self.train_data = []

        monitor = self.sct.monitors[config["train_data_monitor_number"]]
        self.grab_options = {
            "top": monitor["top"] + top,
            "left": monitor["left"] + left,
            "width": width,
            "height": height
        }

        self.img_size = config["train_data_image_size"]
        self.train_data_image_filename = config["train_data_image_filename"]

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sct.__exit__()
        self.csv_file.close()

    def collect(self, image_label):
        self.train_data.append((image_label, self.sct.grab(self.grab_options)))

    def remove_last(self):
        if len(self.train_data):
            self.train_data.pop()

    def save_train_data(self):
        for image_label, image in self.train_data:
            image_filename = self.train_data_image_filename.format(image_label=image_label, uid=uuid.uuid4())
            mss_tools.to_png(image.rgb, image.size, output=image_filename)
            self.csv_file.write(f'{image_label},{image_filename.split("/")[-1]}\n')
