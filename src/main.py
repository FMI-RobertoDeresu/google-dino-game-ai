from selenium import webdriver
from train_data_collector import TrainDataCollector
from config import config
from app_logger import Logger


def collect_data(web_driver):
        Logger.info("start collect_data")
        TrainDataCollector(web_driver).collect()
        Logger.info("stop collect_data")


def ai_train(web_driver):
    Logger.info("start ai_train")
    Logger.info("stop ai_train")


def ai_play(web_driver):
    Logger.info("start ai_play")
    Logger.info("stop ai_play")


if __name__ == '__main__':
    with webdriver.Firefox(executable_path=r'..\geckodriver.exe', log_path='NUL') as web_driver:
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
