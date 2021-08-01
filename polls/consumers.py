import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from time import sleep
from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
import random
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from polls.datas import get_dates
from bs4 import BeautifulSoup

class CrawPredictConsume(AsyncWebsocketConsumer):
    # Connected to websocket.connect
    async def connect(self):
        #self.scope["session"]["seed"] = random.randint(1, 10000)

        await self.accept()

    async def disconnect(self,close_code):
        driver.quit()
        print("disc")

    async def receive(self, text_data):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options,executable_path=r'C:\Users\jh_gc\Desktop\doalr\chromedriver.exe')
        wait = WebDriverWait(driver, 60)
        datapoint = json.loads(text_data)
        val =datapoint['message']

        if val == "gold":
            driver.get("https://www.investing.com/commodities/gold")
        if val == "DXY":
            driver.get("https://www.investing.com/indices/usdollar")
        if val == "Brent":
            driver.get("https://www.investing.com/commodities/brent-oil")
        if val == 'ibovespa':
            driver.get("https://www.investing.com/indices/ibovespa-futures")
        if val == 'VIX':
            driver.get("https://www.investing.com/indices/volatility-s-p-500")
        if val == 'usd/cny':
            driver.get("https://www.investing.com/currencies/usd-cny")
        if val == 'usd/cop':
            driver.get("https://www.investing.com/currencies/usd-cop")
        if val == 'usd/mxn':
            driver.get("https://www.investing.com/currencies/usd-mxn")
        
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#quotes_summary_current_data')))
        while True:
            await asyncio.sleep(2)
            quote=driver.find_element(By.ID,"last_last").text
            print(quote)
            await self.send(text_data=json.dumps(str(quote)))


