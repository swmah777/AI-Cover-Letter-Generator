import streamlit as st
from utils.text_extraction import extract_text_from_cv, extract_job_description_from_link, parse_file_contents
from utils.cover_letter import generate_cover_letter, generate_feedback, create_search_terms
from utils.key_validation import is_valid_key
#from utils.add_github_link import add_github_link


import os
import re
import magic
from PyPDF2 import PdfReader
import docx2txt
import pytesseract
from PIL import Image
import json
from groq import Groq
# make sure you have .env file saved locally with your API keys
#from dotenv import load_dotenv
import pandas as pd
#import sqlite3
from jobspy import scrape_jobs
from st_aggrid import AgGrid, GridOptionsBuilder

# Setting up the SQLite database
#conn = sqlite3.connect('app_data.db')
#c = conn.cursor()

# Creating tables for jobs and comments if they don't exist
#c.execute('''CREATE TABLE IF NOT EXISTS job_searches
#             (id INTEGER PRIMARY KEY, search_term TEXT, job_title TEXT, job_description TEXT, job_link TEXT)''')
#c.execute('''CREATE TABLE IF NOT EXISTS comments
#             (id INTEGER PRIMARY KEY, comment TEXT)''')
#conn.commit()

# Custom CSS to increase the width of the main content area
st.markdown(
    """
    <style>
    .main {
        max-width: 90%;
        padding: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Introduction
st.title("Job Search App")
st.write("Welcome to the Job Search App. Write down what ")

# Sidebar for comments
#st.sidebar.header("Comments")
#user_comment = st.sidebar.text_area("Enter your comments here:")

#if user_comment:
#    c.execute("INSERT INTO comments (comment) VALUES (?)", (user_comment,))
#    conn.commit()
#    st.sidebar.write("Comment submitted!")

# Input field for job search
search_term = st.text_input("Enter your desired search term:")

if st.button("Search"):
    if search_term:
        #first use LLM to translate user input into 
        search_term_list = create_search_terms(search_term)

        st.write(search_term_list)

        df = pd.DataFrame()

        for searchword in search_term_list:

            # Call the find_jobs function
            df1 = scrape_jobs(
                site_name=["indeed"],
                search_term=searchword,
                #location="Kuala Lumpur",
                results_wanted=5,
                hours_old=168,  # (only Linkedin/Indeed is hour specific, others round up to days old)
                country_indeed="Malaysia",  # only needed for indeed / glassdoor
                # linkedin_fetch_description=True # get full description , direct job url , company industry and job level (seniority level) for linkedin (slower)
                # proxies=["208.195.175.46:65095", "208.195.175.45:65095", "localhost"],
                )
            
            df = pd.concat([df, df1], ignore_index=True)

        # Format the job_link column to be clickable
        #df['job_url'] = df['job_url'].apply(lambda x: f'<a href="{x}" target="_blank">Link</a>')
        
        ## Save jobs to the database
        #for _, row in df.iterrows():
        #    c.execute("INSERT INTO job_searches (search_term, job_title, job_description, job_link) VALUES (?, ?, ?, ?)",
        #              (search_term, row['job_title'], row['job_description'], row['job_link']))
        #conn.commit()
        
        # Display the job results
        st.write("Showing the top 10 results:")
        #st.dataframe(df[['title','description', 'job_url','site', 'location','date_posted']].head(10))
        st.markdown(df[['title','description', 'job_url','site', 'location','date_posted']].head(15).to_html(escape=False, index=False), unsafe_allow_html=True)
        #st.dataframe(df)

        # Configure st_aggrid
        #gb = GridOptionsBuilder.from_dataframe(df[['title', 'description', 'job_url', 'site', 'location', 'date_posted']].head(10))
        #gb.configure_pagination(paginationPageSize=10)
        #gb.configure_default_column(wrapText=True, autoHeight=False)
        #gb.configure_column("description", wrapText=False)  # No wrapping to enable expansion
        #gb.configure_grid_options(domLayout='autoHeight')
        #gb.configure_grid_options(onRowClicked="expand")

        #gridOptions = gb.build()

        # Display the grid
        #AgGrid(df[['title', 'description', 'job_url', 'site', 'location', 'date_posted']].head(10), 
        #        gridOptions=gridOptions, 
        #        allow_unsafe_jscode=True,
        #        height=300)

        # CSV download button
        #st.download_button(
        #    label="Download data as CSV",
        #    data=df[['job_title', 'job_description', 'job_link']].head(10).to_csv(index=False),
        #    file_name='job_results.csv',
        #    mime='text/csv',
        #)
    else:
        st.write("Please enter a search term.")

# Closing the database connection
#conn.close()
