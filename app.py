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
st.image("bg.png")

#========API-KEYS=========
GROQ_API_KEY = "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"
GOOGLE_API_KEY = "AQ.Ab8RN6KBx2HJbTgaa71A-bUEIt-hOSg10VSzcN6e6kvfgHVqOw"
TAVILY_API_KEY = "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"

#==========MODEL==========
model = ChatGoogleGenerativeAI(
    model = 'gemini-3.5-flash-lite',
    google_api_key = GOOGLE_API_KEY
)

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
  THE COLOUR THEME SHOULD BE VINTAGE ONLY,
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
