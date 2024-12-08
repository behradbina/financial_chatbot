import os
import random
import time

import requests
import streamlit as st


def print_response(string_response):
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for chunk in string_response.split():
            full_response += chunk + " "
            time.sleep(0.06)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})


def main_page():
    response = ''
    # ---------------------------------- CSS code for style ------------------------------------------------
    css = f"""
        <style>
            body {{
                direction: rtl;
            }}
            div .css-f4ro0r {{
                transform: rotate(180deg);
                left: 0px;
                right: auto !important;
            }}
            @font-face {{
                font-family: 'Calibri';
            }}
            
            .st-bf {{
                font-family: 'Calibri';
            }}

            .calibri-font {{
                font-family: 'Calibri', sans-serif;
                font-size: 30px;
                text-align: center;
            }}
            
            .css-zq5wmm {{
                left: 0px;
                direction: ltr;
            }}
            
            .css-ue6h4q div p {{
                font-family: 'Calibri', sans-serif;
                font-size: 20px;
            }}
            
            .css-s1k4sy > div > div > textarea{{
                font-family: Calibri;
            }}
            #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-uf99v8.ea3mdgi5 > div.block-container.css-1y4p8pa.ea3mdgi4 > div:nth-child(1) > div > div.stChatMessage.css-1c7y2kd.eeusbqq4 > div.css-bncv4y.eeusbqq3 > div:nth-child(1) > div > div > div > div > p {{
                font-family: Calibri;
            }}
            
            .css-5rimss > p {{
                font-family: Calibri;
            }}
            
            .css-1c7y2kd, .css-4oy321 {{
                background-color: rgba(240, 242, 246, 0.95);
                padding: 1rem 1rempx 1rem 1rem;
            }}
            
            .css-4oy321 {{
                background-color: rgba(235, 235, 246, 0.35);
            }}
            
            .css-1lr5yb2 {{
                margin-right: 10px;
            }}
            
        </style>
    """

    st.markdown(css, unsafe_allow_html=True)

    # ---------------------------------- CODE FOR THE WELCOME MESSAGE --------------------------------------

    welcome_message1 = """
    سلام! من یک دستیار هوشمند هستم که توسط واحد هوش تجاری شرکت خدمات انفورماتیک طراحی شده است
    آماده‌ام  برای پاسخگویی به سوالاتتان  کمک کنم
    لطفاً سوال یا درخواست خود را وارد کنید. 😊
    """
    welcome_message2 = "روزتون بخیر؛ من دستیار هوشمند خدمات انفورماتیک هستم، چطور میتونم کمکتون کنم؟"
    welcome_message3 = "سلام، به راهنمایی نیاز دارین؟"
    welcome_messages_list = [welcome_message1, welcome_message2, welcome_message3]

    # ---------------------------------- Initialize chat history ---------------------------------------------
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # ---------------------------------- append old chat messages to the list ---------------------------------
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # ---------------------------------- chat message input box -----------------------------------------------
    if prompt := st.chat_input("سوال خود را در این کادر وارد کنید"):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.spinner("در حال تولید پاسخ مناسب ..."):
            request_body = {
                "user_id": "9999",
                "question": prompt
            }
            question_url = "http://127.0.0.1:8000/ai-chatbot/chatbot/"

            #try:
            response = requests.post(question_url, json=request_body).json().get('answer')
            # except Exception as e:
            #     response = 'پاسخی برای این سوال یافت نشد'
            #     print(e)

    # ---------------------------------- Display assistant response in chat message container ------------------

    if "welcome_message_shown" not in st.session_state:
        assistant_response = random.choice(welcome_messages_list)
        st.session_state.welcome_message_shown = True
        print_response(assistant_response)
    elif not response:
        pass
    else:
        assistant_response = response
        response = None
        print_response(assistant_response)
