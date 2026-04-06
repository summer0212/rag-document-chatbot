import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from src.config import get_api_key

load_dotenv()

def rewrite_user_query(user_query):
    with st.container(border=True):
        st.markdown(user_query)

    # groq_api_key = os.environ["GROQ_API_KEY"]
    groq_api_key = get_api_key()
    model_name = "llama-3.3-70b-versatile"
    llm = ChatGroq(groq_api_key=groq_api_key,model_name=model_name)

    template = """Provide three better search queries for the web search engine to answer the given query.
    Strictly output the queries without anything else.
    
    Example:
    
    User query:
    I have a red light on my dashboard
    
    Answer:
    1. Red dashboard light meaning.
    2. Car dashboard red light symptoms.
    3. Red warning light on dashboard diagnosis

    
    {user_query}
    Answer:"""

    rewrite_prompt = ChatPromptTemplate.from_template(template)

    rewriter = rewrite_prompt | llm | StrOutputParser()

    with st.spinner("Generating queries..."):
        rewritten_query = rewriter.invoke({'user_query':user_query})

    # Parse the 3 queries into a list
    # The LLM outputs something like "1. query one\n2. query two\n3. query three"


    query_list =[]
    for line in rewritten_query.strip().split("\n"):
        cleaned = line.strip()
        if cleaned and cleaned[0].isdigit():
            cleaned = cleaned.split(". ",1)[-1]
        if cleaned:
            query_list.append(cleaned)
    return query_list
    '''
    STEP 1 :- 
    rewritten_query = "1. Definition of software developer\n2. Role and responsibilities of software developer\n3. Software developer job description and skills"

    STEP 2 :- rewritten_query.strip().split("\n") — split by newlines:
    [
    "1. Definition of software developer",
    "2. Role and responsibilities of software developer",
    "3. Software developer job description and skills"
]

    STEP 3 :-  remove the "1. " / "2. " / "3. " prefix using cleaned.split(". ", 1)[-1]:
    "1. Definition of software developer"
                    ↓ split(". ", 1)
          ["1", "Definition of software developer"]
                    ↓ [-1] (take last part)
          "Definition of software developer"

    STEP 4 :- 
    query_list = ["Definition of software developer", "Role and responsibilities of software developer", "Software developer job description and skills"]
'''



    # return rewritten_query