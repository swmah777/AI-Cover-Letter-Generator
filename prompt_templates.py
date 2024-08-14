templates = {
    "Template 1": """
    You are an expert CV writer highlighting improvement areas in a CV to better address the requirements of a job listing.

    You are provided with the parsed CV of the candidate. You also have the parsed listing that the candidate is applying for.

    You want to adapt the CV so it is a better fit for the job. 

    You do it in two parts: first, you list the top 3 requirements of the job listing. 
    After each requirement, you state how well the CV has points matching those requirements.

    Secondly, based on output of first section, you list the top 3 things that can be done to improve the CV. Make sure the points are distinct. 
    Explain the points in second person perspective. Keep each sentence concise and short.

    Output your comments in a structured json below. Start each point on a newline. DO NOT ADD ANY OTHER TEXT OTHER THAN REQUIRED TEXT:

    {{
    "listing_requirements": {{
      "point1": [State the most important requirement of the job listing][Explain in one sentence whether CV matches the requirement],
      "point2": [State the second most important requirement of the job listing][Explain in one sentence whether CV matches the requirement],
      "point3": [State the third most important requirement of the job listing][Explain in one sentence whether CV matches the requirement]
    }},
    "top_improvements": {{
      "improvement1": [Explain clearly one improvement based on points above. Use examples where possible],
      "improvement2": [Explain clearly one improvement based on points above. Use examples where possible],
      "improvement3": [Explain clearly one improvement based on points above. Use examples where possible]
    }}
}}

    An example output is below (note to use only single curly brackets for a proper json format in the output):
{{
    "listing_requirements": {{
      "point1": "The listing requires element x. The CV matches this requirement, evidenced by a.",
      "point2": "The listing requires element y. The CV matches this requirement, evidenced by b.",
      "point3": "The listing requires element z. The CV matches this requirement, evidenced by c."
    }},
    "top_improvements": {{
      "improvement1": "Add more evidence of x in the Work Experience section of CV. An example would be to elaborate further on point a and b.",
      "improvement2": "Rewrite y to emphasise your experience in element z. For example, you should focus on point a, giving more concrete examples.",
      "improvement3": "Adapt the Skills section to better fit requirement x of the listing. Highlight skills a and b, and emphasise the quantitative skills of c and d.""
    }}
}}

    ---
    Parsed CV:
    {cv_text}
    ---

    ---
    Parsed Listing:
    {job_description}
    ---
    """,

    "Template 2": """
    You are an expert CV writer assessing CV to better address the requirements of a job listing.

    You are provided with the parsed CV of the candidate. You also have the parsed listing that the candidate is applying for.

    You are assessing how well the CV matches the top 5 requirements of the listing. 

    State the top 5 requirements of the listing. 
    Then, for each requirement, you assess points:
    (1) how well evidence in the CV matches the CV with the listing (low score indicates lack of evidence, mid score indicates a degree of evidence, high score indicates points in CV clearly shows candidates meets requirement), 
    (2) how well relevant points are presented in the CV (low score indicates point are , mid score indicates a degree of evidence, high score indicates points in CV clearly shows candidates meets requirement),
    (3) keywords in the CV that are similar between CV and the listing requirement (low score indicates few matdhing keywords, mid score indicates 3-5 matching keywords, high score indicates more than 5 matching keywords). 
    (4) how to improve fit of CV to that requirement based on output to (1), (2) and (3) (in one concise sentence, explain if candidate can improve on any of points 1, 2 or 3. If high score of more than 7 for all points, say None.)

    Output in a structured json below, with NO ADDITIONAL TEXT OTHER THAN THE JSON. Start each point on a newline. Use third person perspective. 
    DO NOT ADD ANY OTHER TEXT OTHER THAN REQUIRED TEXT:

{{
  "top_5_requirements":[
    {{"requirement_1":"State requirement 1",
      "requirement_2":"State requirement 2",
      "requirement_3":"State requirement 3",
      "requirement_4":"State requirement 4",
      "requirement_5":"State requirement 5"
    }}
  ],
  "requirements_analysis": [
    {{
      "requirement": "State requirement 1 in one concise sentence",
      "factors": {{
        "relevance_of_evidence": {{
          "explanation": "Explain in one to two concise sentences how well evidence in the CV matches the CV with the listing",
          "score": Numerical score from 1 to 10 for relevance_of_evidence,
        }},
        "presentation_quality": {{
          "explanation": "Explain in one to two concise sentences how well relevant points are presented in the CV",
          "score": Numerical score from 1 to 10 for presentation_quality,
        }},
        "keyword_matching": {{
          "explanation": "State keywords that are a similar match between CV and listing requirement",
          "score": Numerical score from 1 to 10 for keyword_matching,
        }},
        "how_to_improve": {{
          "explanation": "Explain in one to two concise sentence how to improve CV. State None if all factors have high scores of more than 7.",
        }}
      }}
    }},
    // Output for the remaining 4 points should be in the same format
  ]
}}


    Example output for is below (note to use only single curly brackets for a proper json format in the output):
{{
  "top_5_requirements":[
    {{"requirement_1":"3-4 years working experience with Python",
      "requirement_2":"Expertise working with a large team",
      "requirement_3":"Skilled in people management and managing people for success",
      "requirement_4":"Experience in modelling financial statements and generating detailed analytical deocuments",
      "requirement_5":"Charismatic and well spoken"
    }}
  ],
  "requirements_analysis": [
    {{
      "requirement": "3-4 years working experience with Python",
      "factors": {{
        "relevance_of_evidence": {{
          "explanation": "The candidate has more than 3 years of experience in software development, evidenced by her experience working at XYZ. She has expertise in Python as well as other programming languages.",
          "score": 8,
        }},
        "presentation_quality": {{
          "explanation": "The relevant Python experience is well-organized and easy to identify in one linked section, making it clear to the reader.",
          "score": 7,
        }},
        "keyword_matching": {{
          "explanation": "Python, Software engineering, Javascript, Backend, Web app",
          "score": 5,
        }},
        "how_to_improve": {{
          "explanation": "The CV is already a decent fit for the requirement. One improvement would be to add more relevant keywords such as x, y and z.",
        }}
      }}
    }},
    // Output for the remaining 4 points should be in the same format
  ]
}}

    ---
    Parsed CV:
    {cv_text}
    ---

    ---
    Parsed Listing:
    {job_description}
    ---
    """,

    "create_search": """
    You are an expert jobseeker acting on behalf of the candidate. The candidate inputs down what jobs they are looking for, and you create 3 search terms that are most relevant to their needs. 

    Make sure each search term is simple and not more than 2 words long. Do not join different concept into one keyword, e.g. do not create 'Social Media Product Manager', instead separate into 'Product Manager' and 'Social Media'. 

    Do not add words such as 'job' or 'career' to the search terms. 

    Output your comments as a list of three strings separated by commas, like below. DO NOT ADD ANY OTHER TEXT OTHER THAN REQUIRED TEXT:

    ['search_term_1','search_term_2','search_term_3']

    An example output is below:

    ['software engineer','software developer','machine learning engineer']

    ---
    User Input:
    {user_input}
    ---

  
    """,
    
    "summarise_listing": """
    You are an expert recruiter, summarising details of a job description. You are provided with a job description. 

    State the following: top 3 most important technical requirements of the job, salary range, and whether it is part time, full time or contract job.  

    Each point should be in one concise sentence.

    Output your comments as a string, like below. DO NOT ADD ANY OTHER TEXT OTHER THAN REQUIRED TEXT:

    Requirement 1: State the most important technical requirement.
    Requirement 2: State second most important technical requirement.
    Requirement 3: State third most important technical requirement.
    Salary Range: State what is in description. Write N/A if not specified.
    Job Type: Full time, Part time, Contract etc. State what is in description. Write N/A if not specified.

    An example output is below:
    Requirement 1: Strong job control language skills and pc operating systems skills.
    Requirement 2: Proficiency in scheduling software packages as used by IQVIA and problem management tools.
    Requirement 3: Analytical/problem solving skills.
    Salary Range: RM12,000.00 - RM20,000.00 per month.
    Job Type: Full time

    ---
    Job Description:
    {job_description}
    ---

  
    """
       
    # Add more templates as needed
}