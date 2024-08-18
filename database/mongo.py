import pymongo
import streamlit as st


# Setting up MongoDB connection
@st.cache_resource
def init_connection():
    return pymongo.MongoClient(st.secrets["db_url"])


class Database:
    def __init__(self):
        self.client = init_connection()

    def write_feedback(self, data):
        return self.client["jom"]["feedbacks"].insert_one(data).inserted_id

    def write_search_log(self, query, generated_keywords):
        data = {"query": query, "generated_keywords": generated_keywords}
        return self.client["jom"]["search_logs"].insert_one(data).inserted_id
