import pandas as pd
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings
import sys
import contextlib

class Book(BaseModel):
    title: str
    authors: str
    categories: str
    description: str
    thumbnail: str

# Initialize the ChromaDB PersistentClient
client = chromadb.PersistentClient(
    path="chroma_db", 
    settings=Settings(),
    tenant=DEFAULT_TENANT,
    database=DEFAULT_DATABASE,
)
collection = client.get_or_create_collection(name="collection_name")

# Created a Context Manager (suppress_output):
@contextlib.contextmanager
def suppress_output():
    with open('/dev/null', 'w') as devnull:
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = devnull
        sys.stderr = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

def store_books_in_vectorDB():
    model = SentenceTransformer('all-MiniLM-L6-v2')

    df = pd.read_csv("books_cleaned.csv", usecols=['title', 'authors', 'categories', 'description', 'thumbnail'])
    documents = []
    embeddings_list = []
    IDs = []
    metadatas = []

    for index, row in df.iterrows():
        text = ' '.join(row.astype(str).values)
        documents.append(text)
        embedding = model.encode(text).tolist()
        embeddings_list.append(embedding)
        IDs.append(str(index))
        metadata = {
            'title': row['title'],
            'authors': row['authors'],
            'categories': row['categories'],
            'description': row['description'],
            'thumbnail': row['thumbnail']
        }
        metadatas.append(metadata)

    try:
        print(f"Adding {len(documents)} documents to the collection.")
        with suppress_output():
            collection.add(
                documents=documents,
                embeddings=embeddings_list,
                ids=IDs,
                metadatas=metadatas
            )
    except Exception as e:
        print(f"Error occurred while adding documents: {e}")

    return "Documents added to the collection successfully."

def add_book_to_vectorDB(title, authors, categories, description, thumbnail):
    text = f"{title} {authors} {categories} {description}"
    model = SentenceTransformer('all-MiniLM-L6-v2')

    embedding = model.encode(text).tolist()
    metadata = {
        'title': title,
        'authors': authors,
        'categories': categories,
        'description': description,
        'thumbnail': thumbnail
    }

    with suppress_output():
        collection.add(
            documents=[text],
            embeddings=[embedding],
            ids=[title],
            metadatas=[metadata]
        )

def similarity_text(query_text: str):
    print(f"Querying for text: {query_text}")
    results = collection.query(
        query_texts=[query_text],
        n_results=2,
        include=['metadatas', 'documents']
    )
    print(f"Query results: {results}")
    return results['metadatas'], results['documents']

def get_books():
    results = collection.query(
        query_texts=[''], 
        n_results=3000,  
        include=['metadatas']
    )
    books = []
    for meta_list in results['metadatas']:
        for meta in meta_list:
            book = {
                "title": meta['title'],
                "thumbnail": meta.get('thumbnail', 'https://via.placeholder.com/150')
            }
            books.append(book)
    return books

def update_book(title, new_data):
    # Delete the old entry
    collection.delete(ids=[title])
    # Add new entry
    add_book_to_vectorDB(**new_data)
    return "Book updated successfully!"

def delete_book(title):
    collection.delete(ids=[title])
    return "Book deleted successfully!"

def search_books(query: str):
    print(f"Searching for books with query: {query}")
    results = collection.query(
        query_texts=[query],
        n_results=10,  # Adjust the number of results as needed
        include=['metadatas']
    )
    print(f"Search results: {results}")
    books = []
    for meta_list in results['metadatas']:
        for meta in meta_list:
            book = {
                "title": meta['title'],
                "thumbnail": meta.get('thumbnail', 'https://via.placeholder.com/150')
            }
            books.append(book)
    print(f"Books found: {books}")
    return books
