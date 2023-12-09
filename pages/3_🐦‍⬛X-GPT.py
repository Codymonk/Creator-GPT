
# Bring in deps
import os 
from apikey import apikey 

import streamlit as st 
from langchain.llms import GooglePalm
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper 

os.environ['GOOGLE_API_KEY'] = apikey

# App framework
st.title('🐦‍⬛Twitter/X GPT')
st.subheader('Generate X threads title and Threads in just 20 sec. 😎 ')
prompt = st.text_input('Enter Your Prompt') 

# Prompt templates
title_template = PromptTemplate(
    input_variables = ['topic'], 
    template='write me a Twiiter Threads title about {topic}'
)

Threads_template = PromptTemplate(
    input_variables = ['title', 'wikipedia_research'], 
    template='write me a Twiiter threads  based on this title TITLE: {title} while leveraging this wikipedia reserch:{wikipedia_research} minimum 10 thread with numbering '
)
hashtag_template = PromptTemplate(
    input_variables = ['title', 'wikipedia_research'], 
    template='write me a Twitter hashtag based on this title TITLE: {title} while leveraging this wikipedia reserch:{wikipedia_research} '
)
# Memory 
title_memory = ConversationBufferMemory(input_key='topic', memory_key='chat_history')
Threads_memory = ConversationBufferMemory(input_key='title', memory_key='chat_history')
hashtag_memory = ConversationBufferMemory(input_key='title', memory_key='chat_history')



# Llms
llm = GooglePalm(temperature=0.6) 
title_chain = LLMChain(llm=llm, prompt=title_template, verbose=True, output_key='title', memory=title_memory)
Threads_chain = LLMChain(llm=llm, prompt=Threads_template, verbose=True, output_key='script', memory=Threads_memory)
hashtag_chain = LLMChain(llm=llm, prompt=hashtag_template, verbose=True, output_key='script', memory=hashtag_memory)


wiki = WikipediaAPIWrapper()

# Show stuff to the screen if there's a prompt
if prompt: 
    title = title_chain.run(prompt)
    wiki_research = wiki.run(prompt) 
    Threads = Threads_chain.run(title=title, wikipedia_research=wiki_research)
    hashtag = hashtag_chain.run(title=title, wikipedia_research=wiki_research)

    st.write(title) 
    st.write(Threads)
    st.write(hashtag) 

    with st.expander('Title History'): 
        st.info(title_memory.buffer)

    with st.expander('Threads History'): 
        st.info(Threads_memory.buffer)

    with st.expander('hashtag History'): 
        st.info(hashtag_memory.buffer)

    with st.expander('Wikipedia Research'): 
        st.info(wiki_research)
