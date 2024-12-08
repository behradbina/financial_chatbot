import streamlit as st


# ___________________________ HEADER ___________________________ #
def common_elements():
    image_path = "E:/News_Chatbot/dashboard/bot.jpg"
    header_path = "E:/News_Chatbot/dashboard/Logo.jpg"
    st.sidebar.image(image_path, use_column_width=True,  width=200)

    css = f"""
        <style>
            @font-face {{
                font-family: 'Calibri';
            }}

            .calibri-font {{
                font-family: 'Calibri', sans-serif;
                font-size: 20px;
                text-align: center;
            }}

            #root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.css-uf99v8.ea3mdgi5 > div.block-container.css-1y4p8pa.ea3mdgi4 > div:nth-child(1) > div > div:nth-child(1) > div > div > div > img {{
            position: relative;
            left: 18%;
            margin-top: -51px;
            }}
        </style>
    """
    st.image(header_path, use_column_width='never')
    st.markdown(css, unsafe_allow_html=True)
    st.markdown("<p class='calibri-font'>چت بات هوشمند خدمات انفورماتیک</p>", unsafe_allow_html=True)


