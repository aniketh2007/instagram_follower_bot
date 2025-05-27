from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time

USERNAME = "foodielove590"
PASSWORD = "Aniketh@707"
SIMILAR_ACCOUNT = "missionimpossible"

class InstaFollower:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)

    def wait_for_login(self):
        print("Waiting for login to complete...")
        max_wait = 60
        waited = 0
        while waited < max_wait:
            try:
                # Wait for homepage element as an indicator of success
                self.driver.find_element(By.XPATH, "//a[contains(@href, '/accounts/edit/')]")
                print("Login successful!")
                return True
            except NoSuchElementException:
                time.sleep(5)
                waited += 5
        print("Login timeout.")
        return False

    def login(self):
        self.driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(5)

        # Accept or decline cookies
        try:
            cookie_btn = self.driver.find_element(By.XPATH, "//button[text()='Only allow essential cookies']")
            cookie_btn.click()
        except NoSuchElementException:
            pass

        username = self.driver.find_element(By.NAME, "username")
        password = self.driver.find_element(By.NAME, "password")
        username.send_keys(USERNAME)
        password.send_keys(PASSWORD)
        time.sleep(2)
        password.send_keys(Keys.ENTER)

        self.wait_for_login()

    def find_followers(self):
        self.driver.get(f"https://www.instagram.com/{SIMILAR_ACCOUNT}/")
        time.sleep(5)

        try:
            followers_link = self.driver.find_element(By.PARTIAL_LINK_TEXT, "followers")
            followers_link.click()
            time.sleep(5)

            modal = self.driver.find_element(By.XPATH, "//div[@role='dialog']//ul")
            for i in range(5):
                self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal)
                time.sleep(2)
        except NoSuchElementException as e:
            print("Could not load followers modal:", e)

    def follow(self):
        time.sleep(2)
        buttons = self.driver.find_elements(By.XPATH, "//button[normalize-space()='Follow']")
        for button in buttons:
            try:
                button.click()
                time.sleep(1)
            except ElementClickInterceptedException:
                try:
                    time.sleep(1)
                    popup = self.driver.find_element(By.XPATH, "//div[contains(text(), 'Try Again Later')]")
                    cancel_button = self.driver.find_element(By.XPATH, "//button[text()='OK']")
                    cancel_button.click()
                    print("Popup dismissed: 'Try Again Later'")
                except NoSuchElementException:
                    pass
bot = InstaFollower()
bot.login()
bot.find_followers()
bot.follow()
