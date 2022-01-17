import streamlit as st
from multiapp import MultiApp
import data_test
import url_test

# MultiApp
app = MultiApp()

app.add_app("데이터 수집", data_test.app)
app.add_app("URL", url_test.app)

# MultiApp의 run 실행
app.run()