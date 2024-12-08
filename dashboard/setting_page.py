import os
import time

import requests
import streamlit as st


def setting_page():
    css = f"""
        <style>
            @font-face {{
                font-family: 'Calibri';
            }}
            
            body {{
                direction: rtl;
            }}
            
            div .css-u8hs99 {{
                margin-right: 0px;
            }}
            
            section > button  {{
                margin-right:auto !important;
            }}

            .calibri-font {{
                font-family: 'Calibri', sans-serif;
                font-size: 20px;
            }}
            
            .calibri-font-over {{
                font-family: 'Calibri';
                font-size: 20px;
            }}
            
            .st-bf {{
                font-family: 'Calibri';
            }}
            
            .css-zq5wmm {{
                left: 0px;
                direction: ltr;
            }}
            
            .css-ue6h4q div p {{
                font-family: 'Calibri', sans-serif;
                font-size: 20px;
            }} 
            
            div .e1b2p2ww13 {{
                margin-left: 1rem;
                margin-right: 0px;
            }}
            .css-7ym5gk div p {{
                font-family: 'Calibri';
            }}
            .css-8msczc > div > div {{
                padding-top: 7px;
                padding-bottom: 7px;
            }}
            
            .css-5rimss p {{
                font-family: 'Calibri';
            }}
            .calibri-font-margin {{
                font-family: 'Calibri';
                margin-bottom: 0px;
                margin-top: 8px;
                font-size: 20px;
            }}
        </style>
    """

    st.markdown(css, unsafe_allow_html=True)

    # ---------------------------------- Login ------------------------------------------------
    st.sidebar.markdown("<p class='calibri-font'>ورود</p>", unsafe_allow_html=True)
    st.sidebar.text_input("شناسه کاربری")
    st.sidebar.text_input("رمز عبور", type="password")
    st.sidebar.button("ورود")

    # ---------------------------------- Settings ---------------------------------------------
    st.sidebar.markdown("<p class='calibri-font'>تنظیمات</p>", unsafe_allow_html=True)

    # st.sidebar.markdown("<p class='calibri-font'>مدل یادگیری عمیق را انتخاب کنید</p>", unsafe_allow_html=True)
    model_name = st.sidebar.radio("مدل یادگیری عمیق را انتخاب کنید", ("ParsMind", "BehsaGPT"))

    # st.sidebar.markdown("<p class='calibri-font'>روش بازیابی از پایگاه داده را انتخاب کنید</p>", unsafe_allow_html=True)
    retriver_name = st.sidebar.radio("روش بازیابی از پایگاه داده را انتخاب کنید", ("BM25", "Fuzziness"))

    # st.sidebar.markdown("<p class='calibri-font'>معماری چت بات را انتخاب کنید</p>", unsafe_allow_html=True)
    chatbot_architecture = st.sidebar.radio("معماری چت بات را انتخاب کنید",
                                            ("Retriever + Generator", "Retriever + Reader", "Generator", "Retriever"))
    if st.sidebar.button("ذخیره تنظیمات"):
        pass

    # ---------------------------------- Add text ---------------------------------------------
    st.markdown(
        "<p class='calibri-font-margin'>لطفا متنی را که میخواهید به پایگاه دانش چت بات اضافه کنید در اینجا وارد کنید</p>",
        unsafe_allow_html=True)

    subject = st.text_area("", placeholder="موضوع")
    company_type = st.text_area("", placeholder="حوزه قانون")
    question = st.text_area("", placeholder="نمونه پرسش مرتبط")
    answer = st.text_area("", placeholder="متن پاسخ")

    col1, col2 = st.columns([1, 6])
    button_clicked = col1.button("افزودن متن")

    if button_clicked:
        new_content = {
            "subject": subject,
            "company_type": company_type,
            "question": question,
            "answer": answer
        }

        add_context_url = "http://127.0.0.1:8000/" + "ai-chatbot/add-context/"
        for _ in range(3):
            try:
                response = requests.post(add_context_url, json=new_content)
                if response.status_code == 201:
                    message = 'متن با موفقیت اضافه شد!'
                else:
                    message = 'مشکلی پیش آمده، دوباره امتحان کنید!'
                break
            except Exception as e:
                message = 'مشکلی پیش آمده، دوباره امتحان کنید!'
                print(e)

        success_message = col2.info(message)
        time.sleep(2)
        success_message.empty()


# ---------------------------------- Add File ---------------------------------------------
st.markdown(
    "<p class='calibri-font-margin'>لطفا فایلی را که میخواهید جایگزین پایگاه دانش شود را در اینجا وارد کنید</p>",
    unsafe_allow_html=True)

uploaded_file = st.file_uploader("", type=["txt"])
