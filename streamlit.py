import streamlit as st
import pandas as pd

st.title("기능 화면")

option = st.selectbox(
     '기능선택',
     ('데드링크 체크', '공모전', '공지사항', '법령'))

st.write('선택한 기능 : ', option)

label = "URL"

if option in '데드링크 체크':
        st.text_input(label, value="", max_chars=None, key=None, type="default", help=None, autocomplete=None, on_change=None, args=None, kwargs=None,  placeholder=None)
        st.button("시작", key=None, help=None, on_click=None, args=None, kwargs=None)
        data = {
        'URL' : ["www.gov.go.kr"],
        'Location' : ["www.gov.go.kr"],
        'Broken Link' : ["www.gov.go.kr"]
        }
        df = pd.DataFrame(data)

        st.dataframe(df)

        st.button("엑셀 다운", key=None, help=None, on_click=None, args=None, kwargs=None)
else:
        st.button("조회", key=None, help=None, on_click=None, args=None, kwargs=None)   
        st.button("시작", key=None, help=None, on_click=None, args=None, kwargs=None)
