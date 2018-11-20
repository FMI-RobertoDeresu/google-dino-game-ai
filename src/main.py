import keyboard
import const
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from train_data_collector import TrainDataCollector
from config import config


def collect_data(web_driver):
        runner = web_driver.find_element_by_css_selector(".runner-container .runner-canvas")

        window_height = web_driver.execute_script('return window.outerHeight - window.innerHeight;')
        left_coord = runner.location['x']
        top_coord = runner.location['y'] + window_height + 25  # ignore score
        runner_width = runner.size['width']
        runner_height = runner.size['height']

        train_data_collector = TrainDataCollector(left_coord, top_coord, runner_width, runner_height)

        def on_up(e):
            train_data_collector.collect(const.ACTION_JUMP)

        def on_down(e):
            train_data_collector.collect(const.ACTION_DUCK)

        def on_enter(e):
            train_data_collector.collect(const.ACTION_NONE)

        def on_shift(e):
            train_data_collector.remove_last()

        keyboard.on_press_key("up", on_up)
        keyboard.on_press_key("down", on_down)
        keyboard.on_press_key("enter", on_enter)
        keyboard.on_press_key("shift", on_shift)

        while not keyboard.is_pressed("esc"):
            pass

        train_data_collector.save_train_data()


def ai_train(web_driver):
    pass


def ai_play(web_driver):
    start_action = ActionChains(web_driver).key_down(Keys.SPACE)
    jump_action = ActionChains(web_driver).key_down(Keys.UP)
    duck_action = ActionChains(web_driver).key_down(Keys.DOWN)


if __name__ == '__main__':
    with webdriver.Chrome('../chromedriver.exe') as web_driver:
        web_driver.maximize_window()
        web_driver.get('https://chromedino.com/')

        web_driver.execute_script("""
            var adds = document.querySelectorAll("ins");
            adds.forEach(function(add) { add.parentNode.removeChild(add); });
        """)

        {
            'collect_data': collect_data,
            'ai_train': ai_train,
            'ai_play': ai_play
        }[config["mode"]](web_driver)

