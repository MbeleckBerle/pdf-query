# PDF Question Answering with Cassandra and Google Generative AI

This project is a Streamlit-based web application that allows users to upload a PDF file and ask questions based on its contents. The PDF is processed, and the text is embedded into a vector store (using Cassandra) to enable relevant question-answering capabilities with the help of Google Generative AI.

## Features
- **PDF Upload**: Users can upload a PDF file.
- **Text Extraction**: The text content of the PDF is extracted.
- **Question Answering**: Users can ask questions based on the uploaded PDF.
- **Vector Search**: The extracted text is indexed using a Cassandra vector store, allowing for efficient and relevant question answering.
- **AI-powered Responses**: The application uses Google Generative AI for question answering.

## Requirements
Make sure to install the required dependencies before running the application. You can install them via `pip` using the `requirements.txt` file.

```bash
pip install -r requirements.txt


## Setup
- **Clone this repository to your local machine.
- **Navigate to the project folder and install the dependencies.
cd <project-folder>
- **pip install -r requirements.txt
- **Create a .env file in the project root and add your environment variables. For example:

ASTRA_DB_APPLICATION_TOKEN=<your-astra-db-application-token>
ASTRA_DB_ID=<your-astra-db-id>
GOOGLE_API_KEY=<your-google-api-key>
Make sure to replace the placeholders with your actual API keys and database information.

## Running the Application
- **After installing the dependencies and setting up your environment variables, you can run the Streamlit app with the following command:

streamlit run app.py

- **This will launch the app in your browser, where you can upload a PDF file and start asking questions related to its content.

How It Works
PDF Upload: The user uploads a PDF file.
Text Extraction: The PDF content is extracted using PyPDF2.
Text Splitting: The extracted text is split into chunks using the CharacterTextSplitter.
Vector Store: The chunks are embedded using Google Generative AI embeddings and added to the Cassandra vector store.
Querying: The user types a question, and the relevant documents are retrieved from the vector store and used to generate an answer with Google Generative AI.


License
This project is open-source and available under the MIT License. See the LICENSE file for more details.

Made with ❤️ using Streamlit, LangChain, and Google Generative AI.


This README provides an overview of the project, setup instructions, and an explanation of how th