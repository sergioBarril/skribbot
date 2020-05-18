from time import sleep

import asyncio
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Pinturillo():
    def __init__(self, room_config = None):
        self.driver = webdriver.Chrome('driver/chromedriver.exe')
        
        if room_config is not None:
            self.room_config = room_config
        else:
            self.room_config = {
                "customs" : True,
                "language" : 'Spanish',
                "rounds"  : 4,
                "drawtime" : 80,
                "onlycustoms" : False,        
            }
        
        self.customs = ""
        self.URL = ""


    def run(self, URL='https://skribbl.io/'):
        # Open Skribbl.io
        self.driver.get(URL)

        createMode = URL == 'https://skribbl.io/'

        # Accept Cookies
        if not createMode:
            try:
                cookiesButton = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/a[2]'))
                )
                cookiesButton.click()
            except:
                print("Error al aceptar las cookies.")

        # Add a name
        nameInput = self.driver.find_element_by_xpath('//*[@id="inputName"]')
        nameInput.send_keys('Skribbot')

        if createMode:
            self.create_room()
        else:
            self.join_game()
        

    def create_room(self):
        # Create a Private Room
        privateRoomButton = self.driver.find_element_by_xpath('//*[@id="buttonLoginCreatePrivate"]')
        privateRoomButton.click()
        sleep(2)
        
        # Configuration
        self.update_config(self.room_config)
        
        # Get URL
        URL = self.driver.find_element_by_xpath('//*[@id="invite"]')
        self.URL = URL.get_attribute("value")
    
    def join_game(self):
        #Click play
        playButton = self.driver.find_element_by_xpath('//*[@id="formLogin"]/button[1]')
        playButton.click()
        sleep(1)

    def type_in_chat(self, message):
        try:
            chatInput = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="inputChat"]'))
            )
            chatInput.send_keys(message)
            chatInput.send_keys(Keys.RETURN)
        finally:
            self.quit()
    
    def update_config(self, room_config):
        """
        Updates the room config (present or future)
        """
        if not self.URL:
            return False
        
        # Rounds
        roundsSelector = Select(self.driver.find_element_by_xpath('//*[@id="lobbySetRounds"]'))
        roundsSelector.select_by_visible_text(str(room_config['rounds']))

        # Draw timer
        drawTimeSelector = Select(self.driver.find_element_by_xpath('//*[@id="lobbySetDrawTime"]'))
        drawTimeSelector.select_by_visible_text(str(room_config['drawtime']))

        # Language
        languageSelector = Select(self.driver.find_element_by_xpath('//*[@id="lobbySetLanguage"]'))
        languageSelector.select_by_visible_text(room_config['language'])

        # Load customs
        customsInput = self.driver.find_element_by_xpath('//*[@id="lobbySetCustomWords"]')
        if(room_config['customs']):
            self.read_customs()
            if customsInput.get_attribute('value') != self.customs:                
                customsInput.send_keys(self.customs)
        else:
            customsInput.clear()
    
        #Only Custom Words
        onlyCustomsBox = self.driver.find_element_by_xpath('//*[@id="lobbyCustomWordsExclusive"]') 
        if(room_config['onlycustoms'] != onlyCustomsBox.is_selected()):  
            onlyCustomsBox.click()
        
    def read_customs(self):
        """
        Returns the customs from file
        """
        with open('customs.txt', encoding="utf-8") as f:
            self.customs = f.read()
        return self.customs
    
    def start_game(self):
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
    
    def screenshot(self):
        filename = f'{random.randint(0,5000)}.png'
        self.driver.save_screenshot(filename)

        return filename

    def quit(self):
        """
        Closes the ChromeDrive
        """
        self.driver.quit()

if __name__ == "__main__":
    bot = Pinturillo()
    bot.run()