#=========LOAD-MODULES==========
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
import langchain
from langchain.agents import create_agent
from tavily import TavilyClient
import pytesseract as pyt # For OCR
import streamlit as st
import os
import time
from PIL import Image
import pandas as pd
import numpy as np


# TO SHOW WEB APP: Complete page layout
st.set_page_config(layout = "wide")

# TO GIVE TITLE
st.title("AI RESUME GENERATOR")
st.write("""This app helps user to build customized professional 
resume with latest job apply links""")
st.image("https://raw.githubusercontent.com/aadyarajvanshi16/AI_RESUME_GEN/refs/heads/main/bg.png")
st.sidebar.title("Fill Important Details")
st.sidebar.image("https://raw.githubusercontent.com/aadyarajvanshi16/AI_RESUME_GEN/refs/heads/main/bg.png")

#========API-KEYS=========
GROQ_API_KEY = st.sidebar.text_input("Groq-API", type = "password")
GOOGLE_API_KEY = st.sidebar.text_input("Gemini-API", type = "password")
TAVILY_API_KEY = st.sidebar.text_input("Tavily-API", type = "password")

all_API = [GROQ_API_KEY, GOOGLE_API_KEY, TAVILY_API_KEY]
if not all(all_API):
    st.error("Must give API keys")
    st.stop()
elif all(all_API):
    st.success("API KEYS LOADED SUCCESFULLY")
    #==========MODEL==========
    model = ChatGoogleGenerativeAI(
        model = 'gemini-3.5-flash-lite',
        google_api_key = GOOGLE_API_KEY
    )
else:
    st.info("Pass all API keys")

#=======MULTISELECT_OPTION========
options = ["Delhi", "Mumbai", "Pune", "Banglore", "Gurugram/Gurgaon", "Noida"]
location = st.sidebar.multiselect("Select Location: ", options = options)
profile_op = ["Data Analyst", "Ethical Hacker", "Cyber Security Analyst", "Full Stack Developer", "Gen AI Expert"]
profile = st.sidebar.multiselect("Select Job profile: ", options = profile_op)

#=======Get_User_Info==========
st.markdown("""### GET UER INFO""")
user_info = st.text_area("""Write your Resume Description: """)

# response = model.invoke("Hello Buddy!")
# response.content[-1]['text']

#========FUNCTION=========
def search_latest_news_job(query):
  """This function helps to fetch latest
  news or jobs related article using
  tavily"""

  client = TavilyClient(
      api_key = TAVILY_API_KEY
      )
  response = client.search(query)
  return response

  #==========AGENT-CREATION========
agent = create_agent(
    model = model,
    tools = [search_latest_news_job]
)

#=========MAIN-AGENT===========
def main_agent(agent, query):
  """This is main agent or leader agent
  orchestrate sub agents"""

  # Giving prompt to create detailed prompt for code generation
  prompt = """You are AI Assistant and
  below given is a prompt, your
  task is to give detailed prompt for this.
  You are a professional Resume generator
  where user will give their personal info,
  you have to create detailed Resume
  for students or professional one,
  it must be with dynamic UI and UX and,
  with advanced CSS Professional Designing
  Make sure to give output in HTML format only,
  THE COLOUR THEME SHOULD BE A COMBINATION OF PATEL SHADES ONLY,
  no markdowns allowed
  """

  response = agent.invoke({'messages': [{'role':'user', 'content': prompt}]})
  detailed_prompt = response['messages'][-1].content[-1]['text']

  # SAVE PROMPT using file handling

  with open('prompt.txt', 'w') as f:
    f.write(detailed_prompt)

  user_details = f"""Below given are the user details generate Resume based on that, if not given keep: Default Resume: Python Developer user details: {query}"""

  final_prompt = prompt + detailed_prompt + user_details

  # CODE GENERATION
  response = agent.invoke({'messages':[{'role': 'user', 'content': final_prompt}]})
  code = response['messages'][-1].content[-1]['text']
  return code

#=====FUNCTION-CALL=======
# code = main_agent(agent, "ALAN TURING, GEN AI EXPERT")
# from IPython import display as DISPLAY
# DISPLAY.HTML(code)

#=====Fetch_latest_domain_related_jobs_using_Tavily========

def get_jobs(agent, Location = "NOIDA, DELHI", Profile = "Data Analysts, AI Engineer"):

  Location = "NOIDA, DELHI"
  Profile = "Data Analysts, AI Engineer"

  prompt = f"""Based on user given Job profile, fetch latest jobs or job apply article using Naukri, LinkedIn, indeed, or all popular Job apply platforms, show results with JOB PROFILE NAME, LOCATION, SALARY, COMPANY NAME, Show jobs only related to given {Location} and {Profile} output must be in professional HTML Naukri theme cards with dynamic design, show atleast top 10-20 results with direct apply link"""

  response = agent.invoke({'messages':[{'role':'user', 'content': prompt}]})
  code = response['messages'][-1].content[-1]['text']
  return code

# code = get_jobs(agent)
# DISPLAY.HTML(code)

if st.button("Generate Resume"):
    with st.spinner("Agent Running"):
        code = main_agent(agent, user_info)
        st.html(code, width = "stretch",
                unsafe_allow_javascript = True)
        st.divider() # to give horizontal division
        job_code = get_jobs(agent, location, profile)
        st.html(job_code, width = "stretch", 
                unsafe_allow_javascript = True)

