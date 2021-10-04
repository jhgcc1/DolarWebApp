from selenium import webdriver
options = webdriver.ChromeOptions()
# Create your tests here.
driver = webdriver.Chrome(options=options,executable_path=r'C:\Users\jh_gc\Desktop\doalr\chromedriver.exe')

driver.get("https://www.investing.com/")