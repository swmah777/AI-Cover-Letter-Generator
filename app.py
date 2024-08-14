import streamlit as st
from utils.text_extraction import extract_text_from_cv, extract_job_description_from_link, parse_file_contents
from utils.cover_letter import generate_cover_letter, generate_feedback, create_search_terms, summarise_listing, rank_match
from utils.key_validation import is_valid_key
#from utils.add_github_link import add_github_link


import os
import re
import ast
import magic
from PyPDF2 import PdfReader
import docx2txt
import pytesseract
from PIL import Image
import json
from groq import Groq
# make sure you have .env file saved locally with your API keys
from dotenv import load_dotenv
import pandas as pd
#import sqlite3
from jobspy import scrape_jobs
from st_aggrid import AgGrid, GridOptionsBuilder

load_dotenv()

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
st.set_page_config(layout="wide")
# Custom CSS to include Tailwind
st.markdown(
    """
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <style>
    body {
        background-color: white;
    }
    .header-container {
        background-color: #34d399; /* Light emerald background */
        padding: 10px;
        border-radius: 0px;
        margin-bottom: 10px;
    }
    .header-container h1 {
        color: #333333; /* Same darker text for contrast */
        font-size: 2.0rem; /* Larger font size */
        margin: 0;
    }
    .header-container h2, .header-container p {
        font-size: 1.0rem; /* Smaller font size */
        margin: 0;
    }
    .main {
        max-width: 90%;
        padding: 0px;
    }
    /* Table header styling */
    table th {
        background-color: #34d399; /* Same green background */
        color: #333; /* Darker text for contrast */
        padding: 10px;
        border-bottom: 2px solid #ddd; /* Subtle border at the bottom */
    }
    table td {
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Combined header block
st.markdown(
    """
    <div class="header-container">
        <h1>Malaysia JobFinder - Let AI find your perfect job</h1>
        <h2>We summarise relevant jobs from Indeed and Glassdoor posted in the past day.</h2>
        <p>Write down what you are looking for. This can be short ('Analyst') or detailed ('I want a job in social media').</p>
    </div>
    """, 
    unsafe_allow_html=True
)

#clear cache and create new df
st.cache_data.clear()
df = pd.DataFrame()

# Sidebar for comments
#st.sidebar.header("Comments")
#user_comment = st.sidebar.text_area("Enter your comments here:")

#if user_comment:
#    c.execute("INSERT INTO comments (comment) VALUES (?)", (user_comment,))
#    conn.commit()
#    st.sidebar.write("Comment submitted!")

##define needed functions
def extract_and_llm (description):
    # Step 1: Extract the text (this is just an example; modify as needed)
    cleaned_description = description.replace('\n', ' ').strip()
    # Step 2: input to summarise function
    summary = summarise_listing(cleaned_description)
    return summary

def score_match (title, description, searchterm):
    cleaned_title = title.replace('\n', ' ').strip()
    cleaned_description = description.replace('\n', ' ').strip()

    score = rank_match(cleaned_title, cleaned_description, searchterm)
    cleaned_score = score.strip()

    return int(cleaned_score)


# Input field for job search
search_term = st.text_input("What are you looking for?")

if st.button("Search"):
    if search_term:
        #first use LLM to translate user input into 
        search_term_list = create_search_terms(search_term)

        # Convert the string to a list
        search_term_list = ast.literal_eval(search_term_list)

        st.write(search_term_list)

        for searchword in search_term_list:

            # Call the find_jobs function
            df1 = scrape_jobs(
                site_name=["indeed","glassdoor"],
                search_term=searchword,
                location="Malaysia",
                results_wanted=5,
                hours_old=48,  # (only Linkedin/Indeed is hour specific, others round up to days old)
                country_indeed="Malaysia",
                country_glassdoor="Malaysia",  # only needed for indeed / glassdoor
                # linkedin_fetch_description=True # get full description , direct job url , company industry and job level (seniority level) for linkedin (slower)
                # proxies=["208.195.175.46:65095", "208.195.175.45:65095", "localhost"],
                )
            
            
            df = pd.concat([df, df1], ignore_index=True)
            df = df.drop_duplicates(subset=['title'],keep='first')

        # Format the job_link column to be clickable
        df['job_url'] = df['job_url'].apply(lambda x: f'<a href="{x}" target="_blank">Link</a>')
        
        ## Save jobs to the database
        #for _, row in df.iterrows():
        #    c.execute("INSERT INTO job_searches (search_term, job_title, job_description, job_link) VALUES (?, ?, ?, ?)",
        #              (search_term, row['job_title'], row['job_description'], row['job_link']))
        #conn.commit()
        
        # Display the job results
        st.write("Showing the top 10 results:")
        #st.dataframe(df[['title','description', 'job_url','site', 'location','date_posted']].head(10))

        #truncate to what needs to be shown, summarise then display
        #df = df.sort_values(by='date_posted', ascending=False)
        display_df = df.head(15)
        display_df['score'] = display_df.apply(lambda row: score_match(row['title'], row['description'], search_term), axis=1)
        display_df = display_df.sort_values(by='score', ascending=False)
        display_df['summary'] = display_df['description'].apply(extract_and_llm)
        display_df['summary'] = display_df['summary'].str.replace('\n', '<br>')
        st.markdown(display_df[['score','title','company','summary', 'job_url','site', 'location','date_posted']].to_html(escape=False, index=False), unsafe_allow_html=True)
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
