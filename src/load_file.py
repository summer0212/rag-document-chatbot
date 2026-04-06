import requests
import streamlit as st
from tempfile import NamedTemporaryFile
from langchain_community.document_loaders import PyPDFLoader

@st.cache_data
def load_pdf_content(user_manual_url):
    with NamedTemporaryFile(delete=False,suffix=".pdf") as tmp_file:
        response = requests.get(user_manual_url)
        tmp_file.write(response.content)
        tmp_file_path = tmp_file.name

    pdf_loader = PyPDFLoader(tmp_file_path)
    pdf_reader = pdf_loader.load()

    content = [(page.page_content.replace('\n', '\n\n')if page.page_content else '....')for page in pdf_reader]

    return content

def load_uploaded_pdf(uploaded_file):
    """Load PDF from a user-uploaded file object"""
    with NamedTemporaryFile(delete=False,suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file_path = tmp_file.name

    pdf_loader = PyPDFLoader(tmp_file_path)
    pdf_reader = pdf_loader.load()

    content = [(page.page_content.replace('\n', '\n\n')if page.page_content else '....')for page in pdf_reader

    ]
    return content
        

def load_file(uploaded_file=None): #The =None is a default value — it's only used when no  argument is passed. It does NOT override the value when you DO pass something.
    """Main function: use uploaded file if available, otherwise fall back to default"""
    if uploaded_file is not None:
        with st.spinner("Processing your uploaded pdf..."):
            content = load_uploaded_pdf(uploaded_file)
    else:


        user_manual_url =  'https://raw.githubusercontent.com/Samuelchazy/Educative.io/badc624f25a17ef9c36400d4dbc7f2f1275ba21c/user_manuel/Toyota-Highlander-2024.pdf'

        with st.spinner('Loading default PDF content, Toyota manual. Please wait around a minute...'):
            content = load_pdf_content(user_manual_url)
           
    if content:

        return content
    
    else:

        st.error("Could not load the document")
        return None

    #     with st.container(height=600, border=False):
    #         col_left, col_right = st.columns(2)

    #     with col_left:
    #         image_path = "https://raw.githubusercontent.com/Samuelchazy/Educative.io/19d3100db50749489689a5c21029c3499722b254/images/Toyota_3.jpg"
    #         st.image(image_path, use_column_width=True)

    #         image_path = "https://raw.githubusercontent.com/Samuelchazy/Educative.io/19d3100db50749489689a5c21029c3499722b254/images/Toyota_4.jpg"
    #         st.image(image_path, use_column_width=True)

    #     with col_right:
    #         image_path = "https://raw.githubusercontent.com/Samuelchazy/Educative.io/19d3100db50749489689a5c21029c3499722b254/images/Toyota_5.jpg"
    #         st.image(image_path, use_column_width=True)

    #         image_path = "https://raw.githubusercontent.com/Samuelchazy/Educative.io/19d3100db50749489689a5c21029c3499722b254/images/Toyota_6.jpg"
    #         st.image(image_path, use_column_width=True)

    #     return content
    # else:
    #     st.error("User manual not found!!")
    #     return None
