import React, { useState, useEffect } from 'react';
import SearchBar from './components/SearchBar.jsx';
import BookCard from './components/BookCard.jsx';
import Loader from './components/Loader.jsx';
import './App.css';

function App() {
  const [books, setBooks] = useState([]);
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAllBooks();
  }, []);

  const fetchAllBooks = () => {
    setLoading(true);
    fetch('http://127.0.0.1:8000/books', {
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
      })
      .then((data) => {
        setBooks(data.books);
        setLoading(false);
      })
      .catch((error) => {
        console.error('Error fetching books:', error);
        setLoading(false);
      });
  };

  const fetchSearchedBooks = () => {
    if (!query) {
      fetchAllBooks();
      return;
    }
    setLoading(true);
    fetch(`http://127.0.0.1:8000/books/search/?q=${encodeURIComponent(query)}`, {
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
      })
      .then((data) => {
        setBooks(data.books);
        setLoading(false);
      })
      .catch((error) => {
        console.error('Error fetching books:', error);
        setLoading(false);
      });
  };

  return (
    <div className="App">
      <div className="page-title">Book Library</div>
      <SearchBar query={query} setQuery={setQuery} onSearch={fetchSearchedBooks} />
      {loading ? (
        <Loader />
      ) : (
        <div className="book-grid">
          {books.length > 0 ? (
            books.map((book) => <BookCard key={book.id} book={book} />)
          ) : (
            <p>No books found.</p>
          )}
        </div>
      )}
    </div>
  );
}

export default App;