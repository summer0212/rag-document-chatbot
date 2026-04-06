import os
import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import SKLearnVectorStore

import warnings

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ["TOKENIZERS_PARALLELISM"] = "false"


def build_vector(chunks):
    """Build vector store from text chunks.
    
    Args:
        chunks: List of text strings from the text splitter
    
    Returns:
        SKLearnVectorStore ready for similarity search
    """
    if chunks:
        if not st.session_state.vector_store:
            with st.spinner(text = ":red[Building vector store from your document... This may take a moment.]"):

                embedding = HuggingFaceEmbeddings()
                # THIS IS THE KEY CHANGE:
                # Instead of downloading pre-built embeddings,
                # we create them from our chunks using .from_texts()
                
                # vector_store = SKLearnVectorStore.from_texts(texts = chunks, #text from splitter,  e.g., ["Check brake pads every...", "Tire pressure should...", ...]

                # embedding=embedding 
                # )#model that converts text -> vector,  HuggingFace model that converts each chunk → 384-dim vector
                vector_store = SKLearnVectorStore.from_texts(texts=chunks, embedding=embedding)

                st.session_state.vector_store = vector_store
                return vector_store

        else:

            return st.session_state.vector_store
    else:
        st.error("No content was found......")
            


def retrieve_chunks_from_vector_store(vector_store, re_written_query_list):
    """Search the vector store with multiple queries and merge results.
    
    Args:
        vector_store: The SKLearnVectorStore
        query_list: List of rewritten query strings
    
    Returns:
        List of (document, score) tuples, deduplicated and sorted by relevance
    """

    with st.spinner(text=":red[Please wait while we fetch the information...]"):
        all_results = []
        seen_content = set() # To avoid duplicate chunks
        
        for query in re_written_query_list:
            results = vector_store.similarity_search_with_score(query=query, k=3)
            for doc,score in results:
                #Deduplicate: skip if we've already found this exact chunk
                if doc.page_content not in seen_content:
                    seen_content.add(doc.page_content)
                    all_results.append((doc,score))

        all_results.sort(key=lambda x: x[1])
        
        return all_results[:5]

'''Note :-
Document object — has a .page_content attribute (the actual text)
score — a distance score (lower = more similar, which is counterintuitive!)'''

        
    
def retrieve_history():
    for message in st.session_state.messages:
        with st.container(border=True):
            with st.chat_message(message['role']):
                st.markdown(message['content'])
            







