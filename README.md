# Overview
"Chat with Lucky" is an interactive AI chatbot application that retrieves and displays book information. Built with FastAPI for backend and Streamlit for frontend, this application leverages LangChain for embeddings and Chroma for vector database management.


# Features
- Add new books to the database.
- Retrieve book recommendations based on user queries.
- Filter books by categories, authors, and dates.
- Provide summaries of books.
- Interactive chat interface built with Streamlit.


# Running the Application
## Start the FastAPI server
- uvicorn main:app --reload
## Start the Streamlit app
- streamlit run streamlit.py

# Usage
## Adding a Book
- To add a book, you can send a message in the chat like:
I want to add a book title: The Great Gatsby, authors: F. Scott Fitzgerald, categories: Fiction, description: A classic novel set in the 1920s.


## getting summaries 
- To get a summary you can simply ask in the chat like:
I want a summary of the five people you meet in heaven 

## Retrieving Recommendations
To get book recommendations, you can ask:
- I want books on AI

## Getting Summaries
To get a summary of a book, you can ask:

Give me a summary of The five people you meet in heaven.
