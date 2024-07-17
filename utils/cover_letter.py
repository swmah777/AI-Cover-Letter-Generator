from openai import OpenAI
from groq import Groq
import os


def generate_feedback(cv_text, job_description):

    prompt_template = f"""
    You are an expert CV writer highlighting improvement areas in a CV to better address the requirements of a job listing.

    You are provided with the parsed CV of the candidate. You also have the parsed listing that the candidate is applying for.

    You want to adapt the CV so it is a better fit for the job. 

    You do it in two parts: first, you list the top 3 requirements of the job listing. 
    After each requirement, you state how well the CV has points matching those requirements.

    Secondly, based on output of first section, you list the top 3 things that can be done to improve the CV. Make sure the points are distinct. 
    Explain the points in second person perspective. Keep each sentence concise and short.

    Output your comments in a structured text. Start each point on a newline. DO NOT ADD ANY OTHER TEXT OTHER THAN REQUIRED TEXT:


        Listing Requirements:
        Point 1: [State the most important requirement of the job listing][Explain in one sentence whether CV matches the requirement]
        Point 2: [State the second most important requirement of the job listing][Explain in one sentence whether CV matches the requirement]
        Point 3: [State the third most important requirement of the job listing][Explain in one sentence whether CV matches the requirement]

        Top Changes Needed: 
        Improvement 1: [Explain clearly one improvement based on points above. Use examples where possible]
        Improvement 2: [Explain clearly one improvement based on points above. Use examples where possible]
        Improvement 3: [Explain clearly one improvement based on points above. Use examples where possible]
        



    ---
    Parsed CV:
    {cv_text}
    ---

    ---
    Parsed Listing:
    {job_description}
    ---
    """

    client = Groq(
    # This is the default and can be omitted
    api_key=os.environ.get("GROQ_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt_template
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


