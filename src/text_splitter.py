from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_documents(content):
    """
    Split the loaded document pages into smaller chunks for better retrieval.
    
    Args:
        content: List of page text strings from load_file()
    
    Returns:
        List of text chunks
    """

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800, # each chunk with max ~800 characters
        chunk_overlap=100, #100 characters of overlap between chunks
        separators=["\n\n","\n",". "," ",""] #split priority: paragraphs -> lines -> sentences -> words
    )

#content is a list of page strings, join them into one document
    full_text = "\n\n".join(content)

    #split into chunks
    chunks = text_splitter.split_text(full_text)

    return chunks