import os
import mss
import keyboard
import const
from config import config
from mss import tools as mss_tools
from dino import Dino
from datetime import datetime
from selenium.webdriver.remote.webdriver import WebDriver
from app_logger import Logger


class TrainDataCollector:
    def __init__(self, web_driver: WebDriver):
        train_data_config = config["train_data"]
        train_data_monitor_number = train_data_config["monitor_number"]
        train_data_directory = train_data_config["directory"].format(datetime=datetime.now().strftime("%Y%m%d_%H%M%S"))
        train_data_csv_filename = os.path.join(train_data_directory, train_data_config["csv_filename"])
        train_data_image_filename = os.path.join(train_data_directory, train_data_config["image_filename"])

        self.sct = mss.mss()
        self.dino = Dino(web_driver)
        self.train_data_csv_filename = train_data_csv_filename
        self.train_data_image_filename = train_data_image_filename
        self.train_data = []

        monitor = self.sct.monitors[train_data_monitor_number]
        runner = web_driver.find_element_by_css_selector(".runner-container .runner-canvas")
        window_height = web_driver.execute_script('return window.outerHeight - window.innerHeight;')

        self.grab_options = {
            "left": monitor["left"] + int(runner.location['x']) + 70,  # ignore dino,
            "top": monitor["top"] + int(runner.location['y']) + window_height + 25,  # ignore score,
            "width": int(runner.size['width']) - 70,
            "height": int(runner.size['height']) - 25
        }

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sct.__exit__()

    def collect(self):
        def on_home(e):
            self._collect_sample(const.ACTION_JUMP)
            self.dino.jump()
            Logger.info("Jump")

        def on_end(e):
            self._collect_sample(const.ACTION_DUCK)
            self.dino.duck()
            Logger.info("Duck")

        def on_insert(e):
            self._collect_sample(const.ACTION_NONE)
            Logger.info("None")

        def on_delete(e):
            self._remove_last_sample()
            Logger.info("Remove")

        keyboard.on_press_key("home", on_home)
        keyboard.on_press_key("end", on_end)
        keyboard.on_press_key("insert", on_insert)
        keyboard.on_press_key("delete", on_delete)

        while not keyboard.is_pressed("esc"):
            pass

        self._save_train_data()

    def _collect_sample(self, image_label):
        image = self.sct.grab(self.grab_options)
        self.train_data.append((image_label, image))

    def _remove_last_sample(self):
        if len(self.train_data):
            self.train_data.pop()
        else:
            Logger.warning("No sample to remove")

    def _save_train_data(self):
        Logger.info("Saving train data")
        os.makedirs(os.path.dirname(self.train_data_csv_filename), exist_ok=True)
        ids = dict.fromkeys(set(list(zip(*self.train_data))[0]), 0)
        with open(self.train_data_csv_filename, 'a+') as csv_file:
            for image_label, image in self.train_data:
                ids[image_label] += 1
                image_filename = self.train_data_image_filename.format(image_label=image_label, id=ids[image_label])
                mss_tools.to_png(image.rgb, image.size, output=image_filename)
                csv_file.write(f'{image_label},{image_filename.split("/")[-1]}\n')
