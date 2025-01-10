import streamlit as st 
import os 
from PIL import Image
import google.generativeai as genai


st.set_page_config(page_title="Multi Language Invoice extractor" , page_icon="🧙‍♂️")
st.header("MultiLang Invoice Wizard")
st.sidebar.title("Enter Google Gemini API Key : ")
API_KEY=st.sidebar.text_input("Enter API Key" , type="password")

google_api_key=API_KEY
genai.configure(api_key=API_KEY)
os.environ['GOOGLE_API_KEY']=API_KEY

model=genai.GenerativeModel("gemini-1.5-flash")
st.sidebar.write("Don't have an API key? Click the button below")

# Path to the existing text file
file_path = 'generate_api_key.txt'

try:
    # Open and read the file content
    with open(file_path, 'r') as file:
        file_content = file.read()

    # Add a download button in the sidebar
    st.sidebar.download_button(
        label="Download API Key File",
        data=file_content,  # File content
        file_name="generate_api_key.txt",  # File name for download
        mime="text/plain",  # MIME type
    )
except FileNotFoundError:
    st.sidebar.error("The file 'generate_api_key.txt' was not found. Please check the file path.")

def get_gemini_response(prompt , img , input):
    response=model.generate_content([input , img[0] , prompt])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        
        bytes_data=uploaded_file.getvalue()
        images_parts=[{
            'mime_type' : uploaded_file.type,
            "data":bytes_data
        }]

        return images_parts
    else:
        raise FileNotFoundError("File not found")
    

input=st.text_input("Input prompt: " , key="input")
uploaded_file=st.file_uploader("Choose an image of the invoice...." , type=['jpg' , 'jpeg' , 'png'])
image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image , caption="Uploaded Iamge")
    
submit=st.button("Tell me about the image")
input_prompt="""
You are an expert in understanding invoices . We will upload a image as invoice 
and you will have to any questions based on the uploaded invoice image
"""
if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_response(input_prompt , image_data , input)
    st.subheader("Response is : ")
    st.write(response)




st.markdown(
    """
    <style>
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: black;
            color: white;
            text-align: center;
            padding: 10px 0;
            font-size: 14px;
            z-index: 100;
        }
        .footer a {
            color: white;
            text-decoration: none;
        }
        .footer img {
            width: 30px;
            vertical-align: middle;
            margin-left: 10px;
        }
    </style>
    <div class="footer">
        <strong>CopyRight © 2025 Mohit Raje</strong>
        <a href="https://github.com/Mohit-Raje" target="_blank">
            <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" alt="GitHub">
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
    
