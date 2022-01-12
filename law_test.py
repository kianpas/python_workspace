import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Edge
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.alert import Alert
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from urllib.parse import urlparse
from urllib.parse import parse_qs


import time
import json

# 간단히 화면 표현을 위한 streamlit, 부트스트랩 비슷?
import streamlit as st

# 제목
st.title("메인 화면")

# 등록할 항목 선택
option = st.selectbox("등록 항목 선택", ("법령", "자치법규"))

# 선택한 옵션 표현
st.write("선택한 항목 : ", option)

# 등록할 사이트 선택
option2 = st.selectbox("등록 사이트 선택", ("알려드림e", "공공서비스 통합관리시스템"))

# 사이트 선택 표현
st.write("선택한 사이트 : ", option2)

# URL 입력 창
label = "URL"
url = st.text_input(label, value="")

# 조회 버튼 클릭으로 실행
if option == '법령' and st.button("조회"):
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
     headers = {
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55"
     }

     # url 요청 후 정보 request에 저장
     request = requests.get(url, headers=headers)
     
     
     # 받은 요청의 내용만 담기
     content = request.content
     # 대기
     time.sleep(3)

     # 리퀘스트 내용을 BeautifulSoup, lxml 형식으로 파싱
     soup = BeautifulSoup(content, "lxml")

     # 원래 url을 파싱하여 url의 일련번호 가져오는 코드, 굳이 필요없음
     parsed_url = urlparse(url)
     #     lsiSeq = parse_qs(parsed_url.query)['lsiSeq'][0]
     #     lsId = parse_qs(parsed_url.query)['lsId'][0]
     efYd = parse_qs(parsed_url.query)['efYd'][0]
     print(efYd)
     # BeautifulSoup로 정보를 가져온 것
     
     # 법코드, 재개정 여부 판단을 위한 정보, strip은 불필요한 공백 제거
     law_info = soup.find('div', class_='subtit1_1').text.strip()
     
     # 불필요한 처리 efYd url에서 간단히 가져올 수 있음
     # law_month = law_info[10:12].strip()
     # law_day = law_info[13:15].strip()
     
     # month = law_month  if len(law_month) > 1 else '0' + law_month
     # day = law_day if len(law_day) > 1 else '0' + law_day    
     # efYd = law_info[4:8]+str(month)+str(day)
     # print(efYd)
     
     time.sleep(5)
 

     # print(dept_info)
     # 법 코드 판단 lsKndCd
     lsKndCd = ''          
     knd_list = ['법령', '대통령령', '총리령', '부령', '대통령훈령', '국무총리훈령']

     i = 0
     while i < len(knd_list):
          if knd_list[i] in law_info:
               lsKndCd = knd_list[i]
          i += 1
          
     # 법코드판단
     print(lsKndCd)
     
     # 재개정 여부 판단 rrClsCd
     
     rrClsCd = ''     
     law_list = ['제정', '일부개정', '전부개정', '폐지', '일괄개정', '일괄폐지', '타법개정', '타법폐지', '폐지제정']

     i = 0
     while i < len(law_list):
          if law_list[i] in law_info:
               rrClsCd = law_list[i]
          i += 1
          
     # 구분명
     print(rrClsCd)

     
     # 일련번호 
     # select 방식
     lsiSeq = soup.select("#lsiSeq")[0]["value"]
     # find 방식
     # lsiSeq2 = soup.find('input', id='lsiSeq')
     # print(lsiSeq2['value'])
     # 법령 ID
     lsId = soup.select("#lsId")[0]["value"]
     print(lsiSeq)
     print(lsId)
     
     # 공포번호
     ancNo = soup.select("#ancNo")[0]["value"]
     print(ancNo)
              
     # 공포일자
     ancYdBe = soup.select("#ancYd")[0]["value"]
     ancYd = ancYdBe[0:4] + "-" + ancYdBe[4:6] + "-" + ancYdBe[6:]
     print(ancYd)
     
     # 법령제목
     lsNm = soup.select("#lsNm")[0]["value"]
     print(lsNm)
     
     
     # 동적 요소 요청
     data = {'lsiSeq': f'{lsiSeq}', 'efYd' : f'{efYd}', 'efYn':'Y', 'chrClsCd': '010202', 'nwJoYnInfo':'Y', 'ancYnChk':'0'}
     
     re2 = requests.post('https://www.law.go.kr/lsInfoR.do', data=data)
     content2 = re2.content
     # 대기
     time.sleep(3)

     # 리퀘스트 내용을 BeautifulSoup, lxml 형식으로 파싱
     soup2 = BeautifulSoup(content2, "lxml")

     # print(soup2.text)
     
     # test3 = soup2.find('div', class_='cont_subtit').text.strip()
     dept_info = soup2.select('#conScroll > div.cont_subtit > p > a > span')

     # 알려드림등 등록 사이트 로그인을 위한 새로운 탭으로 변경
     #     driver.switch_to.window(tabs[1])

     # 실행할 크롬 드라이버 정보 입력,
     # ChomeDriverManager().install() 설치된 크롬드라이버 사용
     driver = webdriver.Chrome(ChromeDriverManager().install())

     # 알려드림e
     driver.get("https://www.service.go.kr/usr/login")

     time.sleep(1)
     close_btn = driver.find_element(By.XPATH, '//*[@id="nClose"]')
     close_btn.click()
     time.sleep(1)

     # 로그인 정보 채우기
     # 페이지 내 아이디, 패스워드 인풋 위치 XPATH로 찾아서 저장
     inputId = driver.find_element(By.XPATH, '//*[@id="j_username"]')
     inputPw = driver.find_element(By.XPATH, '//*[@id="j_password"]')

     # 인풋에 아이디, 비밀번호 저장
     inputId.send_keys("akgkf@naver.com")
     inputPw.send_keys("wjdqn24#")

     # 로그인 버튼 클릭
     btn_login = driver.find_element(By.CLASS_NAME, "btn-login")
     btn_login.click()

     admin_page = driver.find_element(By.XPATH, '//*[@id="header"]/div[2]/div[2]/a[2]')
     admin_page.click()

     # 현재 페이지 이동 후 정보 입력은 나중에

     law_page = driver.find_element(
          By.XPATH, "/html/body/div[3]/div/div/div[1]/div/ul/li[8]/a"
     )
     law_page.click()

     enroll_btn = driver.find_element(
          By.XPATH, "/html/body/div[3]/div/div/div[2]/div[2]/span"
     )
     enroll_btn.click()

     seq_input = driver.find_element(By.XPATH, '//*[@id="lsiSeq"]')
     seq_input.send_keys(lsiSeq)
     id_input = driver.find_element(By.XPATH, '//*[@id="lsId"]')
     id_input.send_keys(lsId)

     driver.find_element(By.XPATH, '//*[@id="ancNo"]').send_keys(ancNo)

     chk_btn = driver.find_element(By.XPATH, '//*[@id="btnChkDuplicate"]')
     chk_btn.click()
     
     da = Alert(driver)
     time.sleep(1)
     print(da.text)
     da.accept()
          
     select = Select(driver.find_element(By.XPATH, '//*[@id="lsKndCd"]')) 
     select2 = Select(driver.find_element(By.XPATH, '//*[@id="rrClsCd"]')) 
     
     select.select_by_visible_text(lsKndCd)
     select2.select_by_visible_text(rrClsCd)
     
     driver.find_element(By.XPATH, '//*[@id="ancDtFmt"]').send_keys(ancYd)
     driver.find_element(By.XPATH, '//*[@id="efDtFmt2"]').send_keys(ancYd)
     driver.find_element(By.XPATH, '//*[@id="lsNm"]').send_keys(lsNm)
     driver.find_element(By.XPATH, '//*[@id="lsNmKo"]').send_keys(lsNm)
     
     
     print(dept_info[0])
     driver.find_element(By.XPATH, '//*[@id="jrsdOfiNm"]').send_keys(dept_info[0].text)
     driver.find_element(By.XPATH, '//*[@id="jrsdDptNm"]').send_keys(dept_info[1].text)
     
     driver.find_element(By.XPATH, '//*[@id="nationLsClsNm"]').send_keys(rrClsCd)
  
    #     wait = WebDriverWait(driver, 10)
    #     driver.find_element(By.XPATH, '//*[@id="btnChkDuplicate"]').click()
    #     alert = wait.until(expected_conditions.alert_is_present()
    #     txt = alert.text
    #     alert.accept()

    #     alert.accept()
    #     time.sleep(2)


if option == '자치법규' and st.button("조회"):

     headers = {
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55"
     }

     # url 요청 후 정보 request에 저장
     request = requests.get(url, headers=headers)
     
     
     # 받은 요청의 내용만 담기
     content = request.content
     # 대기
     time.sleep(3)

     # 리퀘스트 내용을 BeautifulSoup, lxml 형식으로 파싱
     soup = BeautifulSoup(content, "lxml")

     # 원래 url을 파싱하여 url의 일련번호 가져오는 코드, 굳이 필요없음
     parsed_url = urlparse(url)
     # efYd = parse_qs(parsed_url.query)['efYd'][0]
     
     ordinSeq = soup.find('input', id='ordinSeq')['value']
     print(ordinSeq)
     ordinId = soup.find('input', id='ordinId')['value']
     print(ordinId)
     ordinNm = soup.find('input', id='ordinNm')['value']
     print(ordinNm)
     ancNo = soup.find('input', id='ancNo')['value']
     print(ancNo)     
     # 공포일자
     ancYd = soup.find('input', id='ancYd')['value']
     print(ancYd)
     auto_law_info = soup.find('div', class_='subtit1_1').text.strip()
     print(auto_law_info)
     law_month = auto_law_info[9:11].strip()
     law_day = auto_law_info[12:14].strip()

     month = law_month  if len(law_month) > 1 else '0' + law_month
     day = law_day if len(law_day) > 1 else '0' + law_day    
     efYd = auto_law_info[4:8]+str(month)+str(day)
     # 공포날짜
     print(efYd)
     
     rrClsNm = ''     
     law_list = ['제정', '일부개정', '전부개정', '폐지', '일괄개정', '일괄폐지', '타법개정', '타법폐지', '폐지제정']

     i = 0
     while i < len(law_list):
          if law_list[i] in auto_law_info:
               rrClsNm = law_list[i]
          i += 1
          
     # 구분명
     print(rrClsNm)
