from time import sleep

import asyncio

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait


class Pinturillo():

    VALID_CONFIG_KEYS = ("minimo", "customs", "language", "rounds", "drawTime", "onlyCustoms")
    VALID_ROUNDS = [str(i) for i in range(2, 11)]
    VALID_DRAWTIME = [str(i) for i in range(30, 181, 10)]
    VALID_LANGUAGES = ("English", "German", "Bulgarian", "Czech", "Danish",
        "Dutch", "Finnish", "French", "Estonian", "Greek", "Hebrew", "Hungarian",
        "Italian", "Korean", "Latvian", "Macedonian", "Norwegian", "Portuguese", "Polish", "Romanian",
        "Serbian", "Slovakian", "Spanish", "Sedish", "Tagalog", "Turkish")

    def __init__(self, customs=False, language="Spanish", rounds=4,  drawTime=80, onlyCustoms=False, roomConfig = None):
        self.driver = webdriver.Chrome('driver/chromedriver.exe')
        
        if roomConfig is not None:
            self.roomConfig = roomConfig
        else:
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
        sleep(2)

        # Configuration
        self.roomConfiguration()

        # Get URL
        URL = self.driver.find_element_by_xpath('//*[@id="invite"]')
        self.URL = URL.get_attribute("value")

    
    def roomConfiguration(self):
        """
        Updates the room config (present or future)
        """
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
        customsInput = self.driver.find_element_by_xpath('//*[@id="lobbySetCustomWords"]')
        if(self.roomConfig['customs']):
            self.readCustoms()
            if customsInput.get_attribute('value') != self.customs:                
                customsInput.send_keys(self.customs)
        else:
            customsInput.clear()
    
        #Only Custom Words
        onlyCustomsBox = self.driver.find_element_by_xpath('//*[@id="lobbyCustomWordsExclusive"]')      
        if(self.roomConfig['onlyCustoms'] != onlyCustomsBox.is_selected()):  
            onlyCustomsBox.click()
        
    def readCustoms(self):
        """
        Returns the customs from file
        """
        with open('customs.txt', encoding="utf-8") as f:
            self.customs = f.read()
        return self.customs
    
    def startGame(self):
        """
        Clicks button to start game, then quits.
        """
        startGameButton = self.driver.find_element_by_xpath('//*[@id="buttonLobbyPlay"]')
        startGameButton.click()
        sleep(0.5)
        if startGameButton.is_displayed():
            return False
        
        self.driver.quit()
        return True
    
    def quit(self):
        """
        Closes the ChromeDrive
        """
        self.driver.quit()

if __name__ == "__main__":
    bot = Pinturillo()
    bot.run()