import time
from urllib.parse import parse_qs, urlparse
import openpyxl

import json
import requests
from bs4 import BeautifulSoup

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# 간단히 화면 표현을 위한 streamlit, 부트스트랩 비슷?
import streamlit as st
import pandas as pd

# 제목
st.title("메인 화면")
# # 등록할 항목 선택
# option = st.selectbox("등록 항목 선택", ("법령", "자치법규"))

# # 선택한 옵션 표현
# st.write("선택한 항목 : ", option)

# # 등록할 사이트 선택
# option2 = st.selectbox("등록 사이트 선택", ("알려드림e", "공공서비스 통합관리시스템"))

# # 사이트 선택 표현
# st.write("선택한 사이트 : ", option2)

# # URL 입력 창
# label = "URL"
# url = st.text_input(label, value="")

# with st.container():
#     col1, col2, col3 = st.columns(3)

#     with col1:
#         st.header("분류")
        
#     with col2:
#         st.header("데이터명")
#         st.text_input("데이터명")
#     with col3:
#         st.header("분류코드")
#         st.text_input("분류코드")
        
with st.container():
    col1, col2= st.columns(2)

    with col1:
        st.header("수집항목1")
        data1 = st.text_input("데이터명")
    with col2:
        st.header("수집항목명2")
        data2 = st.text_input("항목명")
        
    # with col3:
    #     st.header("수집항목명3")
    #     data3 = st.text_input("선택자")
        
raw_data = {
            '수집항목1' : [f'{data1}'],
            '수집항목2' : [f'{data2}']
            }


raw_data = pd.DataFrame(raw_data)           

csv = raw_data.to_csv().encode("utf-8-sig")
st.download_button(
     label="Download data as CSV",
     data=csv,
     file_name='large_df.csv',
     mime='text/csv',
 )



xlxs_dir = 'sample.xlsx'
if st.button("저장"):
    with pd.ExcelWriter(xlxs_dir) as writer:
        raw_data.to_excel(writer)