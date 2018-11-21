from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys


class Dino:
    def __init__(self, web_driver):
        self.start_action = ActionChains(web_driver).key_down(Keys.SPACE)
        self.jump_action = ActionChains(web_driver).key_down(Keys.UP)
        self.duck_action = ActionChains(web_driver).key_down(Keys.DOWN)

    def start(self):
        self.start_action.perform()

    def jump(self):
        self.jump_action.perform()

    def duck(self):
        self.duck_action.perform()
