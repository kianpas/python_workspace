import time
from turtle import clear, onclick
from urllib.parse import parse_qs, urlparse

import os.path
import json

# import requests

# from bs4 import BeautifulSoup

# from webdriver_manager.chrome import ChromeDriverManager
# from webdriver_manager.microsoft import EdgeChromiumDriverManager

# 간단히 화면 표현을 위한 streamlit, 부트스트랩 비슷?
import streamlit as st
import pandas as pd


# 카운트 증가
def increment_counter():
    st.session_state.count += 1

# 카운트 감소    
def decrement_counter():
    st.session_state.count -= 1


# # 인풋 초기화 함수
def clear_form():
    st.session_state["code"] = ""
    st.session_state["site"] = ""
    for num in range(st.session_state.count):
        st.session_state[f"data{num+1}"] = ""
        st.session_state[f"selector{num+1}"] = ""


# 수집항목이 담길 딕셔너리
var_col1 = {}
# 선택자가 담길 딕셔너리
var_col2 = {}

# 페이지 열 추가 함수
def loop_col(str, dict):
    for num in range(st.session_state.count):
        if str == "var_col1":
            dict[f"data{num+1}"] = st.text_input(f"수집항목{num+1}", key=f"data{num+1}")
        else:
            dict[f"selector{num+1}"] = st.text_input(
                f"선택자{num+1}", key=f"selector{num+1}"
            )

    # 반복처리 함수 오버로딩 비슷하게?


# 반복 함수 파라미터에 따라 딕셔너리 업데이트, 또는 정렬 역할
def loop_def(str, data):
    for num in range(st.session_state.count):
        # 데이터 업데이트
        if str == "raw_data":
            data.update(
                {
                    f"수집항목{num+1}": var_col1[f"data{num+1}"],
                    f"선택자{num+1}": var_col2[f"selector{num+1}"],
                }
            )
            # 정렬 처리
        elif str == "col_name":
            data.append(f"수집항목{num+1}")
            data.append(f"선택자{num+1}")

    return data


# 저장된 데이터 초기화
def reset_data():
    st.session_state.df = pd.DataFrame(columns=["목적", "분류코드"], index=None)


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

    # # 인풋을 위한 카운트 세션에 생성
    if "count" not in st.session_state:
        st.session_state.count = 0

    # 컬럼1에 카운트 수에 따른 동적 변수 생성 및 인풋 생성
    with col1:
        loop_col("var_col1", var_col1)
        btn = st.button("항목추가", on_click=increment_counter)

    # 컬럼2에 카운트 수에 따른 동적 변수 생성 및 인풋 생성
    with col2:
        loop_col("var_col2", var_col2)
        delbtn = st.button("항목제거", on_click=decrement_counter)

    # 데이터 프레임 형식으로 생성
    df = pd.DataFrame(columns=["목적", "분류코드"], index=None)

    # 생성된 데이터프레임 세션에 저장
    if "df" not in st.session_state:
        st.session_state["df"] = df
        
     # 시작과 함께 지정된 엑셀파일 읽기
    excel_read = pd.read_excel("output.xlsx") if os.path.exists("output.xlsx") else df
    excel_read = excel_read.astype({"분류코드": "int64"}, copy=False)
    

    # 추가, 초기화 버튼
    with col1:
        append = st.button("데이터 추가")
    with col2:
        reset = st.button("항목 초기화", on_click=clear_form)

    # 추가버튼 클릭시 추가
    if append:
        # 초기 데이터
        raw_data = {"목적": f"{site}", "분류코드": f"{code}"}

        # 카운트 수에 따른 초기 데이터 업데이트
        raw_data_result = loop_def("raw_data", raw_data)

        # 세션의 df에 추가
        st.session_state.df = st.session_state.df.append(
            raw_data_result, ignore_index=True
        )

        # 컬럼 순서 정하는 코드
        col_name = ["목적", "분류코드"]
        set_col_name = loop_def("col_name", col_name)

        # 세션에 순서정리된 df 다시 저장
        st.session_state.df = st.session_state.df[set_col_name]

    # 스트리밋 데이터 형식으로 표시
    st.dataframe(st.session_state.df)
    st.button("입력한 데이터 초기화", on_click=reset_data)

    # 데이터 csv로 저장
    # if st.button("입력한 데이터 csv파일로 저장"):
    #     csv = st.session_state.df.to_csv(index=False).encode("utf-8-sig")
    #     data_download = download_btn("Download data as CSV", csv)

    # uploaded_file = st.file_uploader("Choose a file")
    add = st.button("엑셀에 데이터 추가")
    # if uploaded_file is not None:
    #     add = st.button("엑셀에 데이터 추가")
    #     dataframe = pd.read_csv(uploaded_file)
    #     st.write(dataframe)
    if add:
        temp = st.session_state.df

        # 엑셀의 분류코드 문자열에서 int로 변경
        add_data = temp.astype({"분류코드": "int64"}, copy=False)
        # 엑셀에서 불러온 데이터와 입력한 데이터 합침
        merge = pd.concat([excel_read, add_data], ignore_index=True)
        st.session_state.df = merge
        st.write(merge)

        # merge_csv = merge.to_csv(index=False).encode("utf-8-sig")
        # merge_download = download_btn("Download Merge Data", merge_csv)
        # panda_down =
        # 합쳐진 데이터 정해진 엑셀파일로 추출, 덮어쓰기 처리
        merge.to_excel("output.xlsx", index=False)


# 다운로드 버튼 함수
def download_btn(label, data):
    return st.download_button(
        label=label,
        data=data,
        file_name="large_df.csv",
        mime="text/csv",
    )

    # if add_csv:
    #     print(merge)
    #     merge_csv = merge.to_csv(index=False).encode("utf-8-sig")
    #     print(merge_csv)
    #     st.download_button(
    #         label="Download Merge Data",
    #         data=merge_csv,
    #         # file_name="large_df.csv",
    #         mime="text/csv",
    #     )

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
