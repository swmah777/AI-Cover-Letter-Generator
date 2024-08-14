from openai import OpenAI
from groq import Groq
import os
from prompt_templates import templates

#14/8 function to summarise listings
def summarise_listing (job_description):

    prompt_template = templates["summarise_listing"]

    prompt = prompt_template.format(job_description=job_description)

    client = Groq(
    # This is the default and can be omitted
    api_key=os.environ.get("GROQ_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content


#13/8 function to translate user input into search terms:
def create_search_terms(input_text):

    prompt_template = templates["create_search"]

    prompt = prompt_template.format(user_input=input_text)

    client = Groq(
    # This is the default and can be omitted
    api_key=os.environ.get("GROQ_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content


def generate_feedback(cv_text, job_description, template_name):

    prompt_template = templates[template_name]

    prompt = prompt_template.format(cv_text=cv_text, job_description=job_description)

    client = Groq(
    # This is the default and can be omitted
    api_key=os.environ.get("GROQ_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content
    

def generate_cover_letter(cv_text, job_description, selected_language, api_key):
    # Function to generate cover letter using GPT-3.5-turbo (or the latest available model)
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Use an appropriate chat model, e.g., "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Write a professional cover letter based on the CV summary and job description provided. Do not say anything that's not in the CV about the experience, skills and so on. The cover letter should be in {selected_language}"},
            {"role": "assistant", "content": "Certainly, please find below a professional cover letter tailored to the CV summary and job description."},
            {"role": "user", "content": f"CV Summary:\n{cv_text}"},
            {"role": "user", "content": f"Job Description:\n{job_description}"}
        ],
        temperature= 0.3
    )
    # Assuming the last message is the assistant's cover letter
    last_message = response.choices[0].message.content
    return last_message.strip()


