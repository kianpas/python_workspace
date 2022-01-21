import streamlit as st


class MultiApp:
    # 초기 선언
    def __init__(self):
        # apps 리스트 생성
        self.apps = []
        
    def add_app(self, title, func):
        # apps 리스트에 추가
        self.apps.append({"title": title, "function": func})

    def run(self):
        app = st.sidebar.selectbox(
            "Navigation",
            self.apps,
            format_func=lambda app: app['title']
        )
        # app안에 function 실행
        app["function"]()