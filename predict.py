from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import urllib.parse
import json

from cog import BasePredictor, Input, Path
import time


class Predictor(BasePredictor):
    def setup(self) -> None:
        """Load the model into memory to make running multiple predictions efficient"""
        options = webdriver.ChromeOptions()
        options.binary_location = '/root/chrome-linux/chrome'
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        self.browser = webdriver.Chrome(options=options)

    def predict(
        self,
        image_url: str = Input(
            description="Image Input"
        ),
    ) -> str:
        self.browser.set_window_size(1920, 1080)
        baseURL = " https://lens.google.com/uploadbyurl?url="
        url = baseURL + urllib.parse.quote_plus(image_url)

        self.browser.get(url)

        elements = self.browser.find_elements(By.CSS_SELECTOR, '[style]')

        itemsList = []

        for element in elements:
            style = element.get_attribute('style')
            if '--lens-grid-column-count' in style:
                # select each a tag in the element
                aTags = element.find_elements(By.TAG_NAME, 'a')
                for aTag in aTags:
                    # get the href attribute
                    divElement = aTag.find_element(By.TAG_NAME, 'div')
                    objectStucture = {
                        "pageLink": aTag.get_attribute('href'),
                        "title": divElement.get_attribute('data-item-title'),
                        "thumbnail": divElement.get_attribute('data-thumbnail-url'),
                        "data-card-token": divElement.get_attribute('data-card-token')
                    }

                    itemsList.append(objectStucture)
                    

                
                

        return json.dumps(itemsList, indent=4)

