from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import Edge
from selenium.webdriver.edge.service import Service
from bs4 import BeautifulSoup

import requests


import time
import pyperclip
import streamlit as st
import pandas as pd
#driver = webdriver.Edge(EdgeChromiumDriverManager().install())



st.title("메인 화면")

option = st.selectbox(
     '기능선택',
     ('공모전', '데드링크'))

st.write('선택한 기능 : ', option)

label = "URL"
url = st.text_input(label, value='URL 입력')

if st.button("조회"):
    options = webdriver.ChromeOptions()
    options.add_argument('user-data-dir=C:/UsersAdministrator/AppData/Local/Google/Chrome/User Data/Default')
    print(options)
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    user_agent = {'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36'}
   
    #driver = webdriver.Edge(EdgeChromiumDriverManager().install())
    cmsUrl = 'https://cms.gov.kr/'
    driver.get(cmsUrl)
    time.sleep(2)

    uid = 'akgkf@naver.com'
    upw = 'wjdqn24#'

    tag_id = driver.find_element(By.NAME, 'j_username')
    tag_pw = driver.find_element(By.NAME, 'j_password')

    tag_id.click()
    pyperclip.copy(uid)
    tag_id.send_keys(Keys.CONTROL, 'v')
    time.sleep(1)

    tag_pw.click()
    pyperclip.copy(upw)
    tag_pw.send_keys(Keys.CONTROL, 'v')
    time.sleep(1)
    
    login_btn = driver.find_element(By.XPATH, '//*[@id="usrLoginVo"]/div[1]/div[2]/button')
    login_btn.click()
    
    news_btn = driver.find_element(By.XPATH, '/html/body/div[2]/div/ul/li/ul/li[3]/a')
    news_btn.click()
    
    exhibit_link = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[1]/div/ul/li[3]/a')
    exhibit_link.click()
    
    enroll_btn = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div[2]/span')
    enroll_btn.click()
    
    
    request = requests.get(url, headers=user_agent)
    content = request.content
    soup = BeautifulSoup(content)
    title = soup.find('span', class_='title')
    table = soup.find('table', class_='type-5')
    info = soup.find('div', class_='info-cont')
    parents_info = soup.find('section', class_='add-info-section contest-outline')
    print(title.text)
    print(table.text)
    print(info)
    
    
    title_input = driver.find_element(By.NAME, 'cnstexhbNm')
    title_input.send_keys(title.text)
    # content = driver.find_element(By.NAME, 'pssrpCts')
    # content.send_keys(info.text)
    #dateStart_input = driver.find_element(By.ID, 'cnstexhbStDtFmt')
    #dateStart_input.send_keys(date.text)
  
    # while True:
    #     pass


#time.sleep(2)
#driver.implicitly_wait(110)
