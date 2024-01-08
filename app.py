import streamlit as st
from utils.text_extraction import extract_text_from_cv, extract_job_description_from_link
from utils.cover_letter import generate_cover_letter
from utils.key_validation import is_valid_key
from utils.add_github_link import add_github_link



# Sidebar

# Assuming you have a path to your logo image
logo_path = 'img/logo_ai_coverletter.png'

st.sidebar.title('AI Cover Letter Generator!')
# Display the logo at the top of the sidebar
st.sidebar.image(logo_path, use_column_width=True)  # Adjusts the image to the column width

# Input for the OpenAI API key - Now in the sidebar
api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")


# Define the GitHub repository link
github_repo_url = 'https://github.com/hheydaroff/dostgpt'

# Add the GitHub button to the sidebar by calling the utility function
add_github_link(st, github_repo_url)


# CV Upload
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


# Language selection
languages = ['English', 'French', 'Spanish', 'German', 'Chinese', 'Japanese', 'Italian', 'Portuguese', 'Russian', 'Arabic', 'Turkish']
selected_language = st.selectbox("Select the language for the cover letter", languages)

if st.button("Generate Cover Letter"):
    if not api_key:
        st.warning('Please enter your OpenAI API key.')
    elif not cv_text or not job_description:
        st.warning('Please upload a CV and provide a job description.')
    else:
        valid, message = is_valid_key(api_key)
        if valid:
            # Generate cover letter
            cover_letter = generate_cover_letter(cv_text, job_description, selected_language, api_key)
            st.subheader("Generated Cover Letter")
            st.write(cover_letter)
        else:
            # If the API key is invalid, display the error message
            st.error(f"The API key provided is invalid. Error: {message}")