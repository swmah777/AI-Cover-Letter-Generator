import streamlit as st
from utils.text_extraction import extract_text_from_cv, extract_job_description_from_link, parse_file_contents
from utils.cover_letter import generate_cover_letter, generate_feedback
from utils.key_validation import is_valid_key
#from utils.add_github_link import add_github_link

import os
import re
import os
import magic
from PyPDF2 import PdfReader
import docx2txt
import pytesseract
from PIL import Image
import json
from groq import Groq
# make sure you have .env file saved locally with your API keys
from dotenv import load_dotenv

load_dotenv()

# Sidebar

# Assuming you have a path to your logo image
logo_path = 'img/logo_ai_coverletter.png'

st.sidebar.title('AI Cover Letter Generator')
# Display the logo at the top of the sidebar
st.sidebar.image(logo_path, use_column_width=True)  # Adjusts the image to the column width

# Input for the OpenAI API key - Now in the sidebar
#api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")

# CV Upload and Processing
cv_file = st.file_uploader("Upload your CV", type=['pdf', 'docx', 'txt'])
cv_text = ""
if cv_file is not None:
    try:
        cv_text = extract_text_from_cv(cv_file)
        # Use an expander to allow users to toggle the display of the CV text
        with st.expander("Preview CV Text", expanded=True):
            # Create a scrollable container with a fixed height
            st.text_area('', cv_text, height=300)  # You can adjust the height as needed
    except Exception as e:
        st.error(f"An error occurred when processing the CV: {e}")


# Job Description

job_description = ""
job_description = st.text_area("Paste the job description here", height=300)


#automatic summary of top requirements of job


# Language selection
#languages = ['English', 'French', 'Spanish', 'German', 'Chinese', 'Japanese', 'Italian', 'Portuguese', 'Russian', 'Arabic', 'Turkish']
#selected_language = st.selectbox("Select the language for the cover letter", languages)


#button to generate changes needed
if st.button("CV Changes Needed"):
    if not cv_text or not job_description:
        st.warning('Please upload a CV and provide a job description.')
    else:
        # Generate cover letter
        cover_letter = generate_feedback(cv_text, job_description)
        st.subheader("Changes Needed to Tailor Your CV")
        st.write(cover_letter)

        # Add download button for the cover letter
        st.download_button(
            label="Download CV Changes as Text",
            data=cover_letter,
            file_name="cv_changes.txt",
            mime="text/plain"
        )


