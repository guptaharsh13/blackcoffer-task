import os
from pathlib import Path
from unicodedata import name
from dotenv import dotenv_values
from bs4 import BeautifulSoup
import requests

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
        # implement logging
        return

    soup = BeautifulSoup(response.content, "lxml")
    title = soup.findAll(
        name="h1", attrs={"class": "entry-title"})[0].get_text()
    content = soup.findAll(
        name="div", attrs={"class": "td-post-content"})[0]
    if content.find(name="pre"):
        content.pre.decompose()
    content = content.get_text()

    return title, content


if __name__ == "__main__":
    title, content = findContent(
        "https://insights.blackcoffer.com/all-you-need-to-know-about-online-marketing/")
    print(title)
    print(content)
