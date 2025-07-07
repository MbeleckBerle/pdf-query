# run "pip install -r requirements.txt"
import os
import cassio
import streamlit as st
from langchain.vectorstores.cassandra import Cassandra
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.text_splitter import CharacterTextSplitter
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings


# Load environment variables from the .env file
load_dotenv()

# Get the API keys and Astra DB details
ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_ID = os.getenv("ASTRA_DB_ID")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


# Function to read PDF and extract text
def read_pdf(file):
    pdfreader = PdfReader(file)
    raw_text = ""
    for page in pdfreader.pages:
        content = page.extract_text()
        if content:
            raw_text += content
    return raw_text


# Streamlit App
st.markdown(
    """
    <style>
        .main {background-color: #f0f4f8; padding: 20px;}
        .title-container {display: flex; justify-content: center; flex-direction: column; align-items: center;}
        .title-container img {height: 150px; width: 150px; margin-bottom: 20px;}
        .title-container h1 {text-align: center; color: #4CAF50; font-size: 36px; font-weight: bold;}
        .subheader {color: #6c757d; font-size: 24px;}
        .btn {background-color: #4CAF50; color: white; font-weight: bold; padding: 10px 20px; border-radius: 5px;}
        .btn:hover {background-color: #45a049;}
        .text-box {background-color: #ffffff; border: 2px solid #ddd; padding: 10px; border-radius: 5px;}
        .highlight {color: #0275d8; font-weight: bold;}
    </style>
    """,
    unsafe_allow_html=True,
)

# Streamlit layout - Centered image and title
st.markdown('<div class="title-container">', unsafe_allow_html=True)

# Add PNG Image (replace with your image path or URL)
st.image("mojo.png", use_container_width=False)

# Title with custom styling
st.markdown(
    '<h1 class="title-container">📄 **PDF Question Answering**</h1>',
    unsafe_allow_html=True,
)

st.markdown("</div>", unsafe_allow_html=True)

# Subheading and line separator
st.subheader("Ask questions based on the contents of your uploaded PDF file")
st.markdown("___")

# Upload PDF file with custom button
pdf_file = st.file_uploader(
    "Upload a PDF file", type="pdf", label_visibility="collapsed"
)
if pdf_file:
    st.success("PDF file uploaded successfully. 🎉")

    # Read and process the PDF
    raw_text = read_pdf(pdf_file)

    # Display a small preview of the extracted text
    st.text_area(
        "Extracted Text",
        raw_text[::],
        height=200,
        key="extracted_text",
        help="This is a preview of the first part of the extracted text. You can ask questions below.",
    )

    # Initialize Astra DB connection
    cassio.init(token=ASTRA_DB_APPLICATION_TOKEN, database_id=ASTRA_DB_ID)

    # Create embedding model
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    llm = GoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY)

    # Split the text and add to the vector store
    text_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=800, chunk_overlap=10, length_function=len
    )
    texts = text_splitter.split_text(raw_text)

    # Set up Cassandra vector store
    astra_vector_store = Cassandra(
        embedding=embeddings,
        table_name="qa_mini_demo",
        session=None,
        keyspace=None,
    )

    astra_vector_store.add_texts(
        texts
    )  # Add first 50 chunks of text to the vector store
    astra_vector_index = VectorStoreIndexWrapper(vectorstore=astra_vector_store)

    # Create two columns: one for the "Ask Question" input and another for the GIF
    col1, col2 = st.columns([3, 2])  # Adjust column width as needed

    with col1:
        query_text = st.text_input(
            "🔍 **Ask a question:**", help="Type a question related to the PDF content"
        )

    with col2:
        # Add smaller GIF
        st.image(
            "https://gist.githubusercontent.com/vininjr/d29bb07bdadb41e4b0923bc8fa748b1a/raw/88f20c9d749d756be63f22b09f3c4ac570bc5101/programming.gif",
            use_container_width=False,
            width=200,  # Set the GIF size here
        )

    # Process the question
    if query_text:
        st.write(f"**Question:** {query_text}")

        # Query the vector store
        answer = astra_vector_index.query(query_text, llm=llm).strip()
        st.write(f"**Answer:** {answer}")

        # Show relevant documents
        st.markdown("___")
        st.write("**Relevant Documents (by relevance):**")
        for doc, score in astra_vector_store.similarity_search_with_score(
            query_text, k=4
        ):
            st.write(f"**[{score:.4f}]**: {doc.page_content[:200]}...")