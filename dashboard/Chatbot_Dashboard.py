import streamlit as st

from common_elements import common_elements
from main_page import main_page
from setting_page import setting_page


###############################################
#      streamlit run dashboard\Chatbot_Dashboard.py
#      streamlit run dashboard\Chatbot_Dashboard.py --server.port 8080
###############################################

def chat_bot():
    common_elements()
    page = st.sidebar.selectbox("صفحه مورد نظر خود را انتخاب کنید", ["چت بات", "تنظیمات"])

    if page == "چت بات":
        main_page()
    elif page == "تنظیمات":
        setting_page()


if __name__ == "__main__":
    chat_bot()
