from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
url = "https://mail.google.com"
# fp = webdriver.FirefoxProfile('C:\\Users\\yedaya\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\ri0nggib.bot_profile')
options = Options()
options.binary_location = r'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
driver = webdriver.Firefox(executable_path="C:\\Users\\yedaya\\Gechodriver\\geckodriver.exe",firefox_options=options)
driver.get(url)
time.sleep(5)
driver.get("https://projects.zoho.com/portal/voltasolar#dashboard/1562045000003998183")
