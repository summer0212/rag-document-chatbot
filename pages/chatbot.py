import streamlit as st
from src.load_file import load_file
from src.rewrite_query import rewrite_user_query
from src.retriever import build_vector, retrieve_chunks_from_vector_store, retrieve_history
from src.generator import generate_answer
from src.text_splitter import split_documents
from src.evaluator import evaluate_response
from src.memory import build_conversation_context


uploaded_file = st.sidebar.file_uploader(
    "Upload a PDF document",
    type=["pdf"],
    key="pdf_uploader"
)
# Reset vector store when a new file is uploaded
# Why? If the user uploads a new PDF, we need fresh embeddings.
# Without this, the old embeddings stay in session_state and the new PDF is ignored.
if uploaded_file and st.session_state.get("current_file_name") != uploaded_file.name:
    st.session_state.vector_store = None
    st.session_state.current_file_name = uploaded_file.name


#Load the PDF
user_manual_content = load_file(uploaded_file)

if user_manual_content:
    try:
        #-----STep 1 : SPlit the document into chunks
        chunks = split_documents(user_manual_content)
       

        #-------Step 3: Build vector store from chunks
        vector_store = build_vector(chunks)
      

        if uploaded_file:
            st.title(f":rainbow[Chat with:{uploaded_file.name}]")

        else:
            st.title(":rainbow[TOYOTA HIGHLANDER INTERACTIVE BOT]")
        # st.write('') #why are we writing this?

        clear_conversation = st.sidebar.button(label="Clear conversation",
        key = 'clear_conversation',use_container_width=True)

        if clear_conversation:
            st.session_state.messages = []

        user_input = st.chat_input(
            'Ask me a question about the Document...',
            max_chars=1500,
            key='user_input'
        )

        
        #------Show chat history
        history = retrieve_history()
        

        #-----Process user imput----
        if user_input:
            st.session_state.messages.append({"role":"user", "content":user_input})

            rewritten_query = rewrite_user_query(user_input)
         


            relevant_chunks = retrieve_chunks_from_vector_store(vector_store, rewritten_query)

            answer = generate_answer(rewritten_query, relevant_chunks)
            

            #-----Evaluate the response----
            with st.expander("📊 Answer Quality Evaluation", expanded=False):
                with st.spinner("Evaluating response quality"):
                    eval_scores = evaluate_response(user_input, answer, relevant_chunks)

                if eval_scores :
                    col1,col2 = st.columns(2)
                    
                    with col1:
                        faith_score = eval_scores["faithfulness"]
                        st.metric(label="Faithfulness",value=f"{faith_score}/5")
                        st.caption(eval_scores["faithfulness_reason"])
                    
                    with col2:
                        rel_score = eval_scores["relevancy"]
                        st.metric(label="Relevancy",value=f"{rel_score}/5")
                        st.caption(eval_scores["relevancy_reason"])
                else:
                    st.warning("Could not evaluate response.")

            # --- Show Memory Context (Debug) ---
            with st.expander("🧠 Conversation Memory", expanded=False):
                memory_context = build_conversation_context(st.session_state.messages)
                st.text(memory_context)
                st.caption(f"Total messages: {len(st.session_state.messages)} | Window size: 6")
    
                


            

            #-----Show Sources------------
            with st.expander("📚 Sources — Retrieved chunks from your document", expanded=False):
                for i ,(doc,score) in enumerate(relevant_chunks):
                    relevance = round((1 - score/2)*100,1)
                    st.markdown(f"**Chunk {i+1}** - Relevance:'{relevance}%'")
                    st.caption(doc.page_content[:500]) #Showing first 500 characters
                    st.divider()

            #Showing rewritten queries
            with st.expander("Re-written queries",expanded=False):
                for i, query in enumerate(rewritten_query):
                    st.markdown(f"{i+1}.{query}")
            
            
            #col_left, col_right = st.columns(2)
            # with col_left:
            #     with st.expander(label="Re-written user query", expanded=False):
            #         st.write(rewritten_query)
            
            # with col_right:
            #     with st.expander(label="Retrieved relevant text from the car user manual",expanded=False):
            #         st.write(relevant_chunks)

    except Exception as e:
        print(e)
        st.error("Sorry, an error occurred.")


                                               


