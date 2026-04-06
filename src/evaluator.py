import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.config import get_api_key

load_dotenv()

def evaluate_response(question,answer,context_chunks):
    """
    Use LLM-as-Judge to evaluate the RAG response quality.
    
    Evaluates two metrics:
    1. Faithfulness — Is the answer grounded in the retrieved context?
    2. Answer Relevancy — Does the answer address the user's question?
    
    Args:
        question: The user's original question
        answer: The generated answer
        context_chunks: List of (doc, score) tuples from retrieval
    
    Returns:
        dict with 'faithfulness' and 'relevancy' scores and explanations
    """

    # groq_api_key = os.environ.get("GROQ_API_KEY")
    groq_api_key = get_api_key()

    if not groq_api_key:
        return None

    llm = ChatGroq(api_key=groq_api_key,model_name="llama-3.3-70b-versatile",temperature = 0)

    # Extract just the text from the context chunks
    context_text = "\n\n".join([doc.page_content for doc,score in context_chunks])

    eval_template = """You are an objective evaluator for a question-answering system.
        Given the following:
        - User Question: {question}
        - Retrieved Context: {context}
        - Generated Answer: {answer}
        Evaluate the answer on these two criteria:
        1. FAITHFULNESS (1-5): Is the answer factually supported by the retrieved context?
        - 5: Every claim in the answer is directly supported by the context
        - 3: Some claims are supported, some are not in the context
        - 1: The answer contains information not found in the context (hallucination)
        2. RELEVANCY (1-5): Does the answer actually address what the user asked?
        - 5: The answer directly and completely addresses the question
        - 3: The answer partially addresses the question
        - 1: The answer does not address the question at all
        Respond EXACTLY in this format (no other text):
        FAITHFULNESS: [score]
        FAITHFULNESS_REASON: [one sentence explanation]
        RELEVANCY: [score]
        RELEVANCY_REASON: [one sentence explanation]"""

    prompt = ChatPromptTemplate.from_template(eval_template)
    chain = prompt | llm | StrOutputParser()

    try:
        result = chain.invoke({
            "question" : question,
            "context":context_text,
            "answer":answer
        })

        #Parse the LLM response
        scores = parse_eval_response(result)
        return scores

    except Exception as e:
        print(f"Evaluation error: {e}")
        return None

def parse_eval_response(response):
    """Parse the evaluation LLM's response into a structured dict."""
    scores = {
        "faithfulness": 0,
        "faithfulness_reason": "",
        "relevancy": 0,
        "relevancy_reason": ""
    }

    for line in response.strip().split("\n"):
        line = line.strip()
        if line.startswith("FAITHFULNESS:"):
            try:
                scores["faithfulness"] = int(line.split(":")[1].strip())
            except ValueError:
                scores["faithfulness"] = 0

        elif line.startswith("FAITHFULNESS_REASON:"):
            # try:
            scores["faithfulness_reason"] = line.split("FAITHFULNESS_REASON:")[1].strip()
        elif line.startswith("RELEVANCY:"):
            try:
                scores["relevancy"] = int(line.split(":")[1].strip())
            except ValueError:
                scores["relevancy"] = 0
        elif line.startswith("RELEVANCY_REASON:"):
            scores["relevancy_reason"] = line.split(":",1)[1].strip()

    return scores






    