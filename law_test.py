import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Edge
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from urllib.parse import urlparse
from urllib.parse import parse_qs

import time
import streamlit as st

st.title("메인 화면")

option = st.selectbox(
     '기능선택',
     ('법령', '데드링크'))

st.write('선택한 기능 : ', option)

label = "URL"
url = st.text_input(label, value='')


if st.button("조회"):
    st.text("test")
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.execute_script('window.open("about:blank", "_blank");')
    tabs = driver.window_handles
   
    # driver.switch_to_window(tabs[0])
    driver.get(url)

    time.sleep(3)
    result = driver.find_elements(By.CLASS_NAME, 'pty1_p4')
    # print(result)
    for re in result:
         print(re.text)
    # soup2 = BeautifulSoup(hhttml)
    
    # print(soup2.find(id="bodyContent").get_text())


    headers = {'user-agent' :'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36'}
    
    request = requests.get(url, headers=headers)
    content = request.content
    time.sleep(3)
    soup = BeautifulSoup(content, 'lxml')
    parsed_url = urlparse(url)
#     lsiSeq = parse_qs(parsed_url.query)['lsiSeq'][0]
#     lsId = parse_qs(parsed_url.query)['lsId'][0]
   
    print(soup.find('div', class_='subtit1_1'))

    lsiSeq = soup.select('#lsiSeq')[0]['value']
    lsId = soup.select('#lsId')[0]['value']
    print(lsiSeq)
    print(lsId)
    #parents_info = soup.find('section', class_='add-info-section contest-outline')
    ancNo = soup.select('#ancNo')[0]['value']
    print(ancNo)
    ancYd = soup.select('#ancYd')[0]['value']
    text = ancYd[0:4] + "-" + ancYd[4:6] + "-" + ancYd[6:]
    print(text)
    lsNm = soup.select('#lsNm')[0]['value']
    print(lsNm)

    
    driver.switch_to.window(tabs[1])
    driver.get('http://cms.gov.kr/')