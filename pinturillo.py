from time import sleep

import asyncio

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait


class Pinturillo():
    def __init__(self, customs=True, language="Spanish", rounds=4,  drawTime=80, onlyCustoms=False):
        self.driver = webdriver.Chrome('driver/chromedriver.exe')
        
        self.roomConfig = {
            "customs" : customs,
            "language" : language,
            "rounds"  : rounds,
            "drawTime" : drawTime,
            "onlyCustoms" : onlyCustoms,        
        }
        
        self.customs = ""
        self.URL = ""

    def run(self):
        # Open Skribbl.io
        self.driver.get('https://skribbl.io/')
        
        # Accept Cookies
        # cookiesButton = self.driver.find_element_by_xpath('/html/body/div[2]/div/a[2]')
        # cookiesButton.click()

        # Add a name
        nameInput = self.driver.find_element_by_xpath('//*[@id="inputName"]')
        nameInput.send_keys('Skribbot')

        # Create a Private Room
        privateRoomButton = self.driver.find_element_by_xpath('//*[@id="buttonLoginCreatePrivate"]')
        privateRoomButton.click()
        sleep(1.5)

        # Configuration
        self.roomConfiguration()

        # Get URL
        URL = self.driver.find_element_by_xpath('//*[@id="invite"]')
        self.URL = URL.get_attribute("value")

    def roomConfiguration(self):
        # Rounds
        roundsSelector = Select(self.driver.find_element_by_xpath('//*[@id="lobbySetRounds"]'))
        roundsSelector.select_by_visible_text(str(self.roomConfig['rounds']))

        # Draw timer
        drawTimeSelector = Select(self.driver.find_element_by_xpath('//*[@id="lobbySetDrawTime"]'))
        drawTimeSelector.select_by_visible_text(str(self.roomConfig['drawTime']))

        # Language
        languageSelector = Select(self.driver.find_element_by_xpath('//*[@id="lobbySetLanguage"]'))
        languageSelector.select_by_visible_text(self.roomConfig['language'])

        # Load customs
        if(self.roomConfig['customs']):
            self.readCustoms()
            customsInput = self.driver.find_element_by_xpath('//*[@id="lobbySetCustomWords"]')
            customsInput.send_keys(self.customs)

            #Only Custom Words
            if(self.roomConfig['onlyCustoms']):
                onlyCustomsBox = self.driver.find_element_by_xpath('//*[@id="lobbyCustomWordsExclusive"]')
                onlyCustomsBox.click()
    
    def readCustoms(self):
        with open('customs.txt', encoding="utf-8") as f:
            self.customs = f.read()


if __name__ == "__main__":
    bot = Pinturillo()
    bot.run()