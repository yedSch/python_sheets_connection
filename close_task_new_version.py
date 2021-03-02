import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.options import Options


def initiateFFbrowser():
    options = Options()
    options.binary_location = r'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
    options.add_argument('-headless')
    options.profile = 'C:\\Users\\yedaya\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\ri0nggib.bot_profile'
    driver = webdriver.Firefox(executable_path="C:\\Users\\yedaya\\Gechodriver\\geckodriver.exe",
                               firefox_options=options)
    return driver


def initiateGoogleBrowser():
    # edit arguments
    opts = webdriver.ChromeOptions()
    opts.add_argument('--start-maximized')
    opts.add_argument('--headless')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    opts.add_argument('--disable-gpu')
    opts.add_argument(r"--user-data-dir=C:\\Users\\yedaya\\AppData\\Local\\Google\\Chrome\\User Data")
    opts.add_argument(r"C:\Users\yedaya\AppData\Local\Google\Chrome\User Data")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=opts)
    return driver


def Crawl(driver, projectid, tasklistid, taskid, task_identifier, given_url=None, ):
    success = 0
    if given_url:
        print("Url given as param...")
        url = given_url
    else:
        print("Building URL...")
        url = "https://projects.zoho.com/portal/voltasolar#taskdetail/" + projectid + "/" + tasklistid + "/" + taskid
    # print(given_url)
    print(url)
    driver.get(url)
    # driver.get_screenshot_as_file("screenshot.png")
    # print("Driver Get")
    WebDriverWait(driver, 30)
    # button = driver.find_element_by_class_name("zps-primary-button btn-module-transition")
    time.sleep(7)
    find_text = ''
    if task_identifier == 'TCC':
        find_text = 'תיאום התרחש'
        searchtext = "//span[contains(.,'תיאום התרחש')]"
    elif task_identifier == 'Inspection':
        searchtext = "//span[contains(.,'פעילות הסתיימה')]"
        find_text = 'פעילות הסתיימה'
    try:
        python_button = driver.find_element_by_xpath(searchtext)
        print(f"found {find_text}", python_button)
        python_button.click()
        driver.execute_script("arguments[0].click();", python_button)

    except NoSuchElementException:
        print(f"Could not find {find_text} button")
    WebDriverWait(driver, 20)
    if task_identifier=='TCC':
        complete_button_xpath = "//*[@id='trans-bp-transpop']/div[2]/div[2]/div[2]/div[1]"
    elif task_identifier == 'Inspection':
        complete_button_xpath = '//*[@id="button1"]'

    try:
        # complete_button = driver.find_element_by_xpath("//span[contains(.,'Complete')]")
        another = driver.find_element_by_xpath(complete_button_xpath)
        print("found complete button")
    except:
        print("couldn't find complete button")
    WebDriverWait(driver, 20)
    time.sleep(5)
    try:
        # complete_button.click
        another.click
        # complete_button.submit
        # complete_button.send_keys("\n")
        print("click worked")
        success = 1
    except:
        success = 0
        print("org click didn't work")
    try:
        # complete_button.click
        # another.click
        success = 1
        driver.execute_script("arguments[0].click();", another)
        # print(complete_button.click)
        print("clicking script worked")
    except:
        print("script couldn't click")
        success = 0
    time.sleep(3)
    # driver.close()
    return success
    # try:
    #     python_button2 = driver.find_element_by_xpath('//*[@id="button1"]')
    #     python_button2.click()
    #     driver.execute_script("arguments[0].click();", python_button2)
    # except NoSuchElementException:
    #     print("Could not find Complete button")
