import streamlit as st
import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import parse_qs, urlparse
import os.path
import json
import pandas as pd


def app():
    # 셀렉트박스에 표현하기 위해 df 가져옴
    df = st.session_state.df
    data = pd.read_excel("output.xlsx") if os.path.exists("output.xlsx") else df
    data = data.astype({"분류코드": "int64"}, copy=False)
    # data에 하나의 행이 존재할 경우
    if len(data) > 0:
        # 저장된 데이터의 분류코드만 가져와서 options으로 저장
        options = data["분류코드"]
        # 분류코드 options를 스트리밋 셀렉트박스로 사용
        choice = st.selectbox("데이터선택", options)
        # 선택한 값과 데이터의 분류코드 일치한 값을 condition에 저장
        condition = data["분류코드"] == choice
        # 조건에 따른 결과 가져옴
        cond_result = data[condition]

        col1, col2 = st.columns(2)

        purpose = cond_result["목적"].item()

        with col1:
            st.text_input("목적", value=purpose)

        with col2:
            st.text_input("분류코드", value=f"{cond_result['분류코드'].item()}")

        # 선택된 데이터가 있을 시 하나의 정보만 출력 테스트
        if len(cond_result) > 0:
            cond_result = cond_result.fillna(0)
            print(cond_result)
            print(len(cond_result.columns))
            leng = (len(cond_result.columns) - 2) / 2
            var1 = {}
            var2 = {}
            for num in range(int(leng)):
                temp_select = cond_result[f"선택자{num+1}"].item()
                temp_col = cond_result[f"수집항목{num+1}"].item()
                if temp_select != 0:
                    var1[f"selector{num+1}"] = temp_select
                    var2[f"name{num+1}"] = temp_col

            print(var1)
            url = st.text_input("URL")

            st.write(cond_result)

            collect_btn = st.button("수집")
        if collect_btn:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55"
            }
            request = requests.get(url, headers=headers)
            content = request.content
            soup = BeautifulSoup(content, "lxml")

            result_var = {}

            for num in range(len(var1)):
                result_var[f"result{num+1}"] = (
                    soup.select(var1[f"selector{num+1}"])[0]["value"]
                    if soup.select(var1[f"selector{num+1}"]) is not None
                    else ""
                )

            print(result_var)
            print(var2)

            json_object = {}
            # 결과데이터 json형식으로 변경

            for num in range(len(var1)):
                json_object[var2[f"name{num+1}"]] = result_var[f"result{num+1}"]

                # json 타입으로 변경
            json_string = json.dumps(json_object, indent=2, ensure_ascii=False)
            print(json_string)

            st.text_input("수집결과데이터", value=json_string)

            # lsiSeq = soup.select(f"{selector1}")[0]["value"] if soup.select(f"{selector1}") is not None else ""

            # lsId = soup.select(f"{selector2}")[0]["value"] if soup.select(f"{selector2}") is not None else ""

            # if collect_btn and purpose == "법령":

            #     headers = {
            #         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55"
            #     }

            #     url = "https://www.law.go.kr/lsInfoP.do?lsiSeq=24144&lsId=004546&chrClsCd=010202&urlMode=lsInfoP&viewCls=lsInfoP&efYd=19691204&vSct=1945%EB%85%84%EC%9D%B4%ED%9B%84%EC%A2%85%EC%A0%84%EC%9D%98%EA%B7%9C%EC%A0%95%EC%97%90%EC%9D%98%ED%95%9C&ancYnChk=0#0000"
            #     # url 요청 후 정보 request에 저장
            #     request = requests.get(url, headers=headers)

            #     # 받은 요청의 내용만 담기
            #     content = request.content
            #     # 대기
            #     time.sleep(1)

            #     # 리퀘스트 내용을 BeautifulSoup, lxml 형식으로 파싱
            #     soup = BeautifulSoup(content, "lxml")
            #     # 일련번호

            #     lsiSeq = soup.select(f"{selector1}")[0]["value"] if soup.select(f"{selector1}") is not None else ""
            #      # 법령 ID
            #     lsId = soup.select(f"{selector2}")[0]["value"] if soup.select(f"{selector2}") is not None else ""

            #      # 공포번호
            #     ancNo = soup.select("#ancNo")[0]["value"]
            #     print(ancNo)

            #     ancYd_ = soup.select("#ancYd")[0]["value"]
            #     ancYd = ancYd_[0:4] + "-" + ancYd_[4:6] + "-" + ancYd_[6:]
            #     print(ancYd)
            #     # 법령제목
            #     lsNm = soup.select("#lsNm")[0]["value"]
            #     print(lsNm)
            #     law_info = soup.select("#leftContentLi > div")[0].text.strip()
            #     lsKndCd = ""
            #     knd_list = ["법률", "대통령령", "총리령", "부령", "대통령훈령", "국무총리훈령"]

            #     for i, v in enumerate(knd_list):
            #         if v in law_info:
            #             lsKndCd = v
            #     print(lsiSeq)

            #     rrClsCd = ""
            #     law_list = ["제정", "일부개정", "전부개정", "폐지", "일괄개정", "일괄폐지", "타법개정", "타법폐지", "폐지제정"]
            #     for i, v in enumerate(law_list):
            #         if v in law_info:
            #             rrClsCd = v

            #     parsed_url = urlparse(url)

            #     efYd = parse_qs(parsed_url.query)["efYd"][0]
            #     print(efYd)

            #     # 동적 페이지 위한 데이터
            #     data = {
            #         "lsiSeq": f"{lsiSeq}",
            #         "efYd": f"{efYd}",
            #         "efYn": "Y",
            #         "chrClsCd": "010202",
            #         "nwJoYnInfo": "Y",
            #         "ancYnChk": "0",
            #     }

            #     # 동적페이지 요청을 위한 두번째 리퀘스트
            #     re2 = requests.post("https://www.law.go.kr/lsInfoR.do", data=data)
            #     content2 = re2.content
            #     soup2 = BeautifulSoup(content2, "lxml")
            #     dept_info = soup2.select("#conScroll > div.cont_subtit > p > a > span")
            #     efYd = efYd[0:4] + "-" + efYd[4:6] + "-" + efYd[6:]

            #     # 결과데이터 json형식으로 변경
            #     json_object = {
            #        "법령일련번호": f"{lsiSeq}",
            #        "법령아이디": f"{lsId}",
            #        "공포번호" : f"{ancNo}",
            #        "공포일자" : f"{ancYd}",
            #        "법령종류코드" : f"{lsKndCd}",
            #        "제개정구분코드" : f"{rrClsCd}",
            #        "시행일자" : f"{efYd}",
            #        "법령명": f"{lsNm}",
            #        "법령명한글": f"{lsNm}",
            #        "소관부처명": f"{dept_info[0].text}",
            #        "소관부서명": f"{dept_info[1].text}"
            #        }

            #     # json 타입으로 변경
            #     json_string = json.dumps(json_object, indent=2, ensure_ascii=False)
            #     print(json_string)

            #     st.write(cond_result.iloc[:, 2].item(), "는 ", lsiSeq, " 입니다")
            #     st.write(cond_result.iloc[:, 4].item(), "는 ", lsId, " 입니다")

            #     st.text_input("수집결과데이터", value=json_string)

            # if collect_btn and purpose == "자치법규":
            #     st.write("자치법규 준비중")
    else:
        st.write("데이터 없음")
