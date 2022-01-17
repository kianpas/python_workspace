import streamlit as st
import requests
import time
from bs4 import BeautifulSoup

def app():
    
     # 셀렉트박스에 표현하기 위해 df 가져옴
    data = st.session_state.df
    if not data.empty:
        # 저장된 데이터의 분류코드만 가져와서 options으로 저장
        options = data["분류코드"]
        # options를 스트리밋 셀렉트박스로 사용
        choice = st.selectbox("데이터선택", options)
        # 선택한 값과 데이터의 분류코드 일치한 조건 저장
        condition = data["분류코드"] == choice
        cond_result = data[condition]
        
        col1, col2 = st.columns(2)
        
        purpose = f"{cond_result['목적'].item()}"
        
        with col1:
            st.text_input("목적", value=purpose)
            
        with col2:
            st.text_input("분류코드", value=f"{cond_result['분류코드'].item()}")

        if purpose == "법령":
            st.write("법령임")

        # 선택된 데이터가 있을 시 하나의 정보만 출력 테스트
        if len(cond_result) > 0:
            # print(cond_result['수집항목1'].item())
            # st.write(cond_result["수집항목1"].item())
            
            st.text_input("URL")
            selector1 = cond_result["선택자1"].item()
            st.write(cond_result)
            
            
            if st.button("수집"):
            
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55"
                }

                # url 요청 후 정보 request에 저장
                request = requests.get("https://www.law.go.kr/lsInfoP.do?lsiSeq=24144&lsId=004546&chrClsCd=010202&urlMode=lsInfoP&viewCls=lsInfoP&efYd=19691204&vSct=1945%EB%85%84%EC%9D%B4%ED%9B%84%EC%A2%85%EC%A0%84%EC%9D%98%EA%B7%9C%EC%A0%95%EC%97%90%EC%9D%98%ED%95%9C&ancYnChk=0#0000", headers=headers)

                # 받은 요청의 내용만 담기
                content = request.content
                # 대기
                time.sleep(1)

                # 리퀘스트 내용을 BeautifulSoup, lxml 형식으로 파싱
                soup = BeautifulSoup(content, "lxml")
                
                law_info = soup.select(f"{selector1}")[0]["value"]
                
                print(law_info)
                st.write(cond_result.iloc[:, 2].item(), "는 ", law_info, " 입니다")