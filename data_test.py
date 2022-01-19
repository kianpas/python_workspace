import time
from turtle import clear, onclick
from urllib.parse import parse_qs, urlparse

import json
# import requests

# from bs4 import BeautifulSoup

# from webdriver_manager.chrome import ChromeDriverManager
# from webdriver_manager.microsoft import EdgeChromiumDriverManager

# 간단히 화면 표현을 위한 streamlit, 부트스트랩 비슷?
import streamlit as st
import pandas as pd

def app():
    # 제목
    st.title("데이터 수집")

    # 컨테이너
    with st.container():
        # 컬럼 2개 생성
        col1, col2 = st.columns(2)

        # 컬럼1
        with col1:
            st.header("수집항목1")
            site = st.text_input("목적", key="site")

        # 컬럼2
        with col2:
            st.header("수집항목명2")
            code = st.text_input("분류코드", key="code")

    # 인풋을 위한 카운트 세션에 생성
    if "count" not in st.session_state:
        st.session_state.count = 0

    # 카운트 증가
    def increment_counter():
        st.session_state.count += 1


    # 카운트 감소
    def decrement_counter():
        st.session_state.count -= 1


    

    # 수집항목이 담길 딕셔너리
    var_col1 = {}
    # 선택자가 담길 딕셔너리
    var_col2 = {}

    # 컬럼1에 카운트 수에 따른 동적 변수 생성 및 인풋 생성
    with col1:
        for num in range(st.session_state.count):
            var_col1[f"data{num+1}"] = st.text_input(f"수집항목{num+1}", key=f"data{num+1}")

    # 컬럼2에 카운트 수에 따른 동적 변수 생성 및 인풋 생성
    with col2:
        for num in range(st.session_state.count):
            var_col2[f"selector{num+1}"] = st.text_input(
                f"선택자{num+1}", key=f"selector{num+1}"
            )

    # 항목추가 버튼
    with col1:
        btn = st.button("항목추가", on_click=increment_counter)
    # 항목제거 버튼
    with col2:
        delbtn = st.button("항목제거", on_click=decrement_counter)

    # 데이터 프레임 형식으로 변경
    df = pd.DataFrame(columns=["목적", "분류코드"], index=None)

    # 변경된 데이터프레임 세션에 저장
    if "df" not in st.session_state:
        st.session_state["df"] = df

    # 초기화 함수
    def clear_form():
        st.session_state["code"] = ""
        st.session_state["site"] = ""
        for num in range(st.session_state.count):
            st.session_state[f"data{num+1}"] = ""
            st.session_state[f"selector{num+1}"] = ""


    # 추가, 초기화 버튼
    with col1:
        append = st.button("데이터 추가")
    with col2:
        reset = st.button("초기화", on_click=clear_form)

    # 추가버튼 클릭시 추가
    if append:
        # 초기 데이터
        raw_data = {"목적": f"{site}", "분류코드": f"{code}"}

        # 카운트 수에 따른 초기 데이터 업데이트
        for num in range(st.session_state.count):
            raw_data.update(
                {
                    f"수집항목{num+1}": var_col1[f"data{num+1}"],
                    f"선택자{num+1}": var_col2[f"selector{num+1}"],
                }
            )
        # 업데이트 된 데이터 df에 추가
        st.session_state.df = st.session_state.df.append(raw_data, ignore_index=True)

        # 컬럼 순서 정하는 코드
        col_name = ["목적", "분류코드"]
        for num in range(st.session_state.count):
            col_name.append(f"수집항목{num+1}")
            col_name.append(f"선택자{num+1}")

        st.session_state.df = st.session_state.df[col_name]
    # 스트리밋 데이터 형식으로 표시
    st.dataframe(st.session_state.df)

    

    # 데이터 csv로 저장
    if st.button("csv파일로 저장?"):
        csv = st.session_state.df.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            label="Download data as CSV",
            data=csv,
            # file_name="large_df.csv",
            mime="text/csv",
        )

    
    
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        add= st.button("엑셀에 데이터 추가")
        dataframe = pd.read_csv(uploaded_file)
        st.write(dataframe)
        if add:
            print(st.session_state.df)
            temp = st.session_state.df

            dd = temp.astype({'분류코드':'int64'}, copy=False)

           
            merge = pd.concat([dataframe, dd], ignore_index=True)
            # foo = merge.dtypes.astype(str)
              
            st.write(merge)
        
        print(merge)

        
        # 업로드 방식 사용시에도 사용 가능
        # print(dataframe['분류코드'])
        # options = dataframe["분류코드"]
        # choice = st.selectbox("데이터선택", options)
        # condition = dataframe["분류코드"] == choice
        # cond_result = dataframe[condition]
        # print(cond_result["수집항목1"].item())

    xlxs_dir = "sample.xlsx"

    # with pd.ExcelWriter(xlxs_dir) as writer:
    #     raw_data.to_excel(writer)
