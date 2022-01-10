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

# 제목
st.title("메인 화면")

# 등록할 항목 선택
option = st.selectbox(
     '등록 항목 선택',
     ('법령', '자치법규'))

# 선택한 옵션 표현
st.write('선택한 항목 : ', option)

# 등록할 사이트 선택
option2 = st.selectbox(
     '등록 사이트 선택',
     ('알려드림e', '공공서비스 통합관리시스템'))

# 사이트 선택 표현
st.write('선택한 사이트 : ', option2)

# URL 입력 창
label = "URL"
url = st.text_input(label, value='')

# 조회 버튼 클릭으로 실행
if st.button("조회"):
    st.text("test")
     # 실행할 크롬 드라이버 정보 입력
    driver = webdriver.Chrome(ChromeDriverManager().install())

     # 스크래핑할 정보를 입력할 새로운 탭 생성
    driver.execute_script('window.open("about:blank", "_blank");')
    
     # 탭 정보 담음
    tabs = driver.window_handles
   
    # driver.switch_to_window(tabs[0])
     # 입력한 url로 페이지 정보 읽어옴
    driver.get(url)

     # 페이지 로딩 기다림
    time.sleep(3)

     # 가져온 페이지에서 클래스이름으로 요소 찾음
    result = driver.find_elements(By.CLASS_NAME, 'pty1_p4')
    
     # 법령 정보 출력 예
    for re in result:
         print(re.text)
    # soup2 = BeautifulSoup(hhttml)
    
    # print(soup2.find(id="bodyContent").get_text())


     # beautifulsoup로 정보 가져오기 셀레니움만 사용해도된다
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

     # 로그인을 위한 새로운 탭으로 변경
    driver.switch_to.window(tabs[1])

     # 알려드림e 
    driver.get('https://www.service.go.kr/usr/login')
     # 로그인 정보 채우기
    inputId = driver.find_element(By.XPATH, '//*[@id="j_username"]')
    inputPw = driver.find_element(By.XPATH, '//*[@id="j_password"]')
    inputId.send_keys('akgkf@naver.com')
    inputPw.send_keys('wjdqn24#')
    
     # 로그인 버튼 클릭
    btn_login = driver.find_element(By.CLASS_NAME, 'btn-login')
    btn_login.click()