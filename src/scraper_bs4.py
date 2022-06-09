import os
from pathlib import Path
from unicodedata import name
from dotenv import dotenv_values
from bs4 import BeautifulSoup
import requests
from logger_config import configLogger

scraper_logger = configLogger(__name__)

env_path = os.path.join(Path(__file__).resolve().parent.parent, ".env")

config = dotenv_values(env_path)
try:
    user_agent = config["user_agent"]
except Exception as e:
    quit({"ERROR": "Improperly Configured Environment"})


def findContent(url):

    # surround with try-catch

    response = requests.get(url=url, headers={
                            "User-Agent": user_agent, 'Accept-Language': 'en-US, en;q=0.5'})
    if not response.status_code == 200:
        scraper_logger.error(f"request unsuccessful for {url}")
        quit({"error": f"request unsuccessful for {url} - may be due to a network error"})

    soup = BeautifulSoup(response.content, "lxml")
    title = soup.findAll(
        name="h1", attrs={"class": "entry-title"})[0].get_text()
    content = soup.findAll(
        name="div", attrs={"class": "td-post-content"})[0]
    if content.find(name="pre"):
        content.pre.decompose()
    content = content.get_text()

    return title, content
