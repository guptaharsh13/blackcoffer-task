from dotenv import dotenv_values
from pathlib import Path
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from pyvirtualdisplay import Display

env_path = os.path.join(Path(__file__).resolve().parent.parent, ".env")

config = dotenv_values(env_path)
try:
    python_env = config["python_env"]
    user_agent = config["user_agent"]
except Exception as e:
    quit({"ERROR": "Improperly Configured Environment"})


def setupChromedriver():
    chrome_options = Options()

    if python_env == "production":

        try:
            display = Display(visible=0, size=(1920, 1080))
            display.start()
        except:
            # some info and auto-detect linux
            quit({"production": "Something went wrong while configuring display"})

        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("window-size=1920x1080")
        chrome_options.add_argument(f"user-agent={user_agent}")

    chrome_options.add_argument("disable-notifications")
    chrome_options.add_experimental_option("detach", True)
    service = Service(ChromeDriverManager().install())
    chrome_driver = webdriver.Chrome(service=service, options=chrome_options)
    chrome_driver.maximize_window()
    chrome_driver.implicitly_wait(15)

    return chrome_driver


chrome_driver = setupChromedriver()


def findContent(url):
    chrome_driver.get(url=url)

    title = chrome_driver.find_element(
        by=By.XPATH, value="//h1[@class='entry-title']").text
    content = chrome_driver.find_element(
        by=By.XPATH, value="//div[@class='td-post-content']").text

    return title, content
