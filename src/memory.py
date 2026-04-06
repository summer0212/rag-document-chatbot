import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from src.config import get_api_key

load_dotenv()

#Number of recent messages to keep in full (6 messages = 3 Q&A pairs)
RECENT_WINDOW = 6

def build_conversation_context(messages):
    """
    Build a conversation context string with two parts:
    1. A summary of older messages (if any)
    2. Full text of recent messages
    
    Args:
        messages: List of {"role": ..., "content": ...} dicts from session_state
    
    Returns:
        A formatted string with summarized old context + recent messages
    """
    if not messages:
        return "No conversation history yet"

    #If we have fewer messages that window then we return them all
    if len(messages) <= RECENT_WINDOW:
        return format_messages(messages)

    #Split into old and recent messages
    old_messages = messages[:-RECENT_WINDOW]
    recent_messages = messages[-RECENT_WINDOW:]

    #Summarize old messages
    summary = summarize_messages(old_messages)

    #Combine Summary + Recent messages
    context = f"Summary of earlier conversation:\n{summary}\n\nRecent messages:\n{format_messages(recent_messages)}"

    return context

def format_messages(messages):
    '''Format a list of messages into a readable string.'''
    return "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])

def summarize_messages(messages):
    """Use the LLM to summarize older messages into a brief paragraph"""
    # groq_api_key = os.environ.get("GROQ_API_KEY")
    groq_api_key = get_api_key()
    if not groq_api_key:
        # Fallback: just truncate instead of summarizing
        return format_messages(messages[-4:])

    llm = ChatGroq(
        groq_api_key = groq_api_key,
        model_name = "llama-3.3-70b-versatile",
        temperature =0
    )
    
    conversation_text = format_messages(messages)

    template = '''Summarize the following conversation in 2-3 sentences. 
        Focus on the key topics discussed and any important information exchanged.
        Keep it brief and factual.
        Conversation:
        {conversation}
        Summary:'''

    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm | StrOutputParser()

    try:
        summary = chain.invoke({"conversation": conversation_text})
        return summary.strip()
    except Exception as e:
        print(f"Summarization error: {e}")
        # Fallback: return last few messages as-is
        return format_messages(messages[-4:])