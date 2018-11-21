from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver


class Dino:
    def __init__(self, web_driver: WebDriver):
        self.web_driver = web_driver
        self.jump_action = ActionChains(web_driver).key_up(Keys.DOWN).key_down(Keys.UP).pause(.2).key_up(Keys.UP)
        self.duck_action = ActionChains(web_driver).key_up(Keys.UP).key_down(Keys.DOWN).pause(.2).key_up(Keys.DOWN)

    def jump(self):
        self.jump_action.perform()

    def duck(self):
        self.duck_action.perform()
