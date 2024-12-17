import os
from pathlib import Path
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

ROOT_PATH = Path(__file__).parent.parent.parent

CHROMEDRIVER_NAME = os.getenv("CHROMEDRIVER_NAME")

CHROMEDRIVER_PATH = ROOT_PATH / "bin" / "chromedriver-linux64" / CHROMEDRIVER_NAME


def make_chrome_browser(*options):
    chrome_options = webdriver.ChromeOptions()
    if options is not None:
        for option in options:
            chrome_options.add_argument(option)

    chrome_service = Service(executable_path=CHROMEDRIVER_PATH)
    browser = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return browser


if __name__ == "__main__":
    browser = make_chrome_browser("--headless")
    browser.get("https://www.twoofus.com.br")
    sleep(5)
    browser.quit()
