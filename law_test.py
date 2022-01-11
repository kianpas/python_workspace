import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Edge
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from urllib.parse import urlparse
from urllib.parse import parse_qs

import time

# 간단히 화면 표현을 위한 streamlit, 부트스트랩 비슷? 
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
   

     # 스크래핑할 정보를 입력할 새로운 탭 생성
#     driver.execute_script('window.open("about:blank", "_blank");')
    
     # 탭 정보 담음
#     tabs = driver.window_handles
   
    # driver.switch_to_window(tabs[0])
    
     # 입력한 url로 페이지 정보 읽어옴
#     driver.get(url)

     # 페이지 로딩 기다림
#     time.sleep(3)

     # 가져온 페이지에서 클래스이름으로 요소 찾음
#     result = driver.find_elements(By.CLASS_NAME, 'pty1_p4')
    
     # 법령 정보 출력 예
#     for re in result:
     #     print(re.text)
    # soup2 = BeautifulSoup(hhttml)
    
    # print(soup2.find(id="bodyContent").get_text())


     # beautifulsoup로 정보 가져오기 
     # 법령정보 동적으로 보여주므로 셀레니움만 사용해도된다
     # 현재 가져올 수 있는 몇가지 정보만 BeautifulSoup로 가져오고 있음
     # 헤더에 유저 에이전트 정보 담기
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55'}
    
     # url 요청 후 정보 request에 저장
    request = requests.get(url, headers=headers)
     # 받은 요청의 내용만 담기
    content = request.content
     # 대기
    time.sleep(3)
    
     # 리퀘스트 내용을 BeautifulSoup, lxml 형식으로 파싱
    soup = BeautifulSoup(content, 'lxml')
    
     # 원래 url을 파싱하여 url의 일련번호 가져오는 코드, 굳이 필요없음
    parsed_url = urlparse(url)
#     lsiSeq = parse_qs(parsed_url.query)['lsiSeq'][0]
#     lsId = parse_qs(parsed_url.query)['lsId'][0]

     # BeautifulSoup로 정보를 가져온 것
    test1 = soup.find('div', class_='subtit1_1').text.strip()
    print(test1[19:23])
    ttt = soup.select_one('#conTop > div > span')
    print(ttt)
     # 일련번호
    lsiSeq = soup.select('#lsiSeq')[0]['value']
     # 법령 ID
    lsId = soup.select('#lsId')[0]['value']
    print(lsiSeq)
    print(lsId)
    #parents_info = soup.find('section', class_='add-info-section contest-outline')
     # 공포번호
    ancNo = soup.select('#ancNo')[0]['value']
    print(ancNo)
     # 공포일자
    ancYd = soup.select('#ancYd')[0]['value']
    text = ancYd[0:4] + "-" + ancYd[4:6] + "-" + ancYd[6:]
    print(text)
     # 
    lsNm = soup.select('#lsNm')[0]['value']
    print(lsNm)


     # 알려드림등 등록 사이트 로그인을 위한 새로운 탭으로 변경
#     driver.switch_to.window(tabs[1])

       # 실행할 크롬 드라이버 정보 입력, 
     # ChomeDriverManager().install() 설치된 크롬드라이버 사용
    driver = webdriver.Chrome(ChromeDriverManager().install())


     # 알려드림e 
    driver.get('https://www.service.go.kr/usr/login')
    
    time.sleep(1)
    close_btn = driver.find_element(By.XPATH, '//*[@id="nClose"]')
    close_btn.click()
    time.sleep(1)

     # 로그인 정보 채우기
     # 페이지 내 아이디, 패스워드 인풋 위치 XPATH로 찾아서 저장
    inputId = driver.find_element(By.XPATH, '//*[@id="j_username"]')
    inputPw = driver.find_element(By.XPATH, '//*[@id="j_password"]')
    
     # 인풋에 아이디, 비밀번호 저장
    inputId.send_keys('akgkf@naver.com')
    inputPw.send_keys('wjdqn24#')
    
     # 로그인 버튼 클릭
    btn_login = driver.find_element(By.CLASS_NAME, 'btn-login')
    btn_login.click()
    
    admin_page = driver.find_element(By.XPATH, '//*[@id="header"]/div[2]/div[2]/a[2]')
    admin_page.click()
    
     # 현재 페이지 이동 후 정보 입력은 나중에
     
     
    law_page = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[1]/div/ul/li[8]/a')
    law_page.click()
    
    enroll_btn = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div[2]/span')
    enroll_btn.click()
    
    seq_input = driver.find_element(By.XPATH, '//*[@id="lsiSeq"]')
    seq_input.send_keys(lsiSeq)

    id_input = driver.find_element(By.XPATH, '//*[@id="lsId"]')
    id_input.send_keys(lsId)

    driver.find_element(By.XPATH, '//*[@id="ancNo"]').send_keys(ancNo)
    
#     chk_btn = driver.find_element(By.XPATH, '//*[@id="btnChkDuplicate"]')
#     print(chk_btn)
#     chk_btn.click()
    
    driver.find_element(By.XPATH, '//*[@id="ancDtFmt"]').send_keys(text)
    driver.find_element(By.XPATH, '//*[@id="efDtFmt2"]').send_keys(text)
    driver.find_element(By.XPATH, '//*[@id="lsNm"]').send_keys(lsNm)
    driver.find_element(By.XPATH, '//*[@id="lsNmKo"]').send_keys(lsNm)
#     wait = WebDriverWait(driver, 10)
#     driver.find_element(By.XPATH, '//*[@id="btnChkDuplicate"]').click()
#     alert = wait.until(expected_conditions.alert_is_present())
#     txt = alert.text
#     alert.accept()
    
#     alert.accept()
#     time.sleep(2)
    