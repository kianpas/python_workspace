import time
from urllib.parse import parse_qs, urlparse

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

        
with st.container():
    col1, col2= st.columns(2)

    with col1:
        st.header("수집항목1")
        site = st.text_input("목적")
        # data3 = st.text_input("수집항목1")
    with col2:
        st.header("수집항목명2")
        code = st.text_input("분류코드")
        # data4 = st.text_input("선택자")

# number = st.number_input('Insert a number', step=1,)



if 'count' not in st.session_state:
	st.session_state.count = 0

def increment_counter():
	st.session_state.count += 1
 
def decrement_counter():
	st.session_state.count -= 1

btn = st.button('Increment', on_click=increment_counter)
delbtn = st.button('Decrement', on_click=decrement_counter)
# if delbtn:
#     print(st.session_state.count)

# if btn:
#     print(st.session_state.count)
    # col1.empty()
var_col1 = {}
var_col2 = {}
with col1:
    for num in range(st.session_state.count):
        var_col1[f'data{num+1}'] = st.text_input(f'수집항목{num+1}')
        
with col2:
    for num in range(st.session_state.count):
        var_col2[f'selector{num+1}'] = st.text_input(f'선택자{num+1}')           

df = pd.DataFrame(columns = ['목적', '분류코드', '수집항목1', '선택자1'], index=None)


# st.dataframe(df)
if 'df' not in st.session_state:
    st.session_state['df'] = df
    
print(var_col1['data3'])
if st.button("Append"):
    raw_data = {
            '목적' : f'{site}',
            '분류코드' : f'{code}'
            }
    
    for num in range(st.session_state.count):
        raw_data.update({f'수집항목{num+1}' : var_col1[f'data{num+1}'], f'선택자{num+1}' : var_col2[f'selector{num+1}']})
           
            
       
    st.session_state.df = st.session_state.df.append(raw_data, ignore_index=True)
    
st.dataframe(st.session_state.df)
data = st.session_state.df
options = data['분류코드']
choice = st.selectbox('데이터선택', options)
condition = (data['분류코드'] == choice)
cond_result = data[condition]
# if cond_result['수집항목1'].item():
#     print(cond_result['수집항목1'].item())
       

if st.button("csv파일로 저장?"):
    csv = data.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='large_df.csv',
        mime='text/csv',
    )
    

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    dataframe = pd.read_csv(uploaded_file)
    st.write(dataframe)
    # print(dataframe)
    # 행, 열 순서
    # print(dataframe['분류코드'])
    options = dataframe['분류코드']
    choice = st.selectbox('데이터선택', options)
    condition = (dataframe['분류코드'] == choice)
    cond_result = dataframe[condition]
    print(cond_result['수집항목1'].item())
    
xlxs_dir = 'sample.xlsx'

    # with pd.ExcelWriter(xlxs_dir) as writer:
    #     raw_data.to_excel(writer)
        
        
        
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