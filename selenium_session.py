from selenium import webdriver
from selenium.webdriver.chrome import options
from webdriver_manager.chrome import ChromeDriverManager
import requests


options = webdriver.ChromeOptions()


# options.add_argument('--user-data-dir=C:/Users/1/AppData/Local/Google/Chrome/User Data')

s = requests.get("https://www.google.co.kr")
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.google.co.kr")
for c in s.cookies:
    driver.add_cookie({'name': c.name, 'value': c.value, 'path': c.path, 'expiry': c.expires})
driver.refresh()


# executor_url = driver.command_executor._url
# session_id = driver.session_id
# driver.get("https://www.google.co.kr")
# print(session_id)
# print(executor_url)

# driver2 = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
# driver2.session_id = session_id
# print(driver2.current_url)
