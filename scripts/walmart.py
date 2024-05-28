from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

import time

class WalmartWebScrapper:
    def __init__(self, debug = False):
        options = None
        
        if (debug is False):
            options = Options()
            options.headless = True
            options.add_experimental_option("excludeSwitches", ["enable-logging"])

        driver = webdriver.Chrome(options)
        driver.get("https://www.walmart.com.mx/")
        driver.implicitly_wait(5)

        self.driver = driver

    def resolveCaptcha(self, tryAgainCount = 0):
        time.sleep(5)
        pxCaptchaContainer = self.driver.find_element(by=By.ID, value='px-captcha')

        if pxCaptchaContainer is None:
            self.resolveCaptcha(tryAgainCount + 1)

        if tryAgainCount > 5:
            return False
        
        pxCaptchaContainerIFrames = pxCaptchaContainer.find_element(by=By.TAG_NAME, value='iframe')

        action = ActionChains(self.driver)
        action.click_and_hold(pxCaptchaContainer)
        action.perform()

        time.sleep(10)
        
        action.release(pxCaptchaContainer)
        action.perform()
        
        time.sleep(0.2)
        
        action.release(pxCaptchaContainer)

        return True

    def selectNextContainer(self):
        nextContainer = None

        try:
            nextContainer = self.driver.find_element(by=By.ID, value='__next')
        except NoSuchElementException:
            self.resolveCaptcha()

        if nextContainer is None:
            self.resolveCaptcha()
            
            nextContainer = self.driver.find_element(by=By.ID, value='__next')
        
        return nextContainer

    def selectMainContent(self):
        nextContainer = self.selectNextContainer()
        mainContent = nextContainer.find_element(by=By.ID, value='maincontent')

        return mainContent

    def selectSearchBox(self):
        nextContainer = self.selectNextContainer()

        header = nextContainer.find_element(by=By.TAG_NAME, value='header')
        search_box = header.find_element(by=By.CSS_SELECTOR, value='input[name="q"]')
        
        return search_box
    
    def selectResultsContainer(self):
        mainContent = self.selectMainContent()

        resultsContainer = mainContent.find_element(by=By.CSS_SELECTOR, value='* > div')
        resultsContainer = resultsContainer.find_element(by=By.CSS_SELECTOR, value='* > div:last-child')
        return resultsContainer

WalmartScrapper = WalmartWebScrapper() 

# document.getElementById with selenium
search_box = WalmartScrapper.selectSearchBox()
search_box.click()

search_box.send_keys('Audifonos Skullcandy Crusher Evo')
search_box.submit()

time.sleep(7)

successfullyResolveCaptcha = WalmartScrapper.resolveCaptcha()

if successfullyResolveCaptcha is False:
    print("Captcha could not be resolved")

resultsContainer = WalmartScrapper.selectResultsContainer()

# wait on this screen, not close the browser
time.sleep(500)

# driver.quit()