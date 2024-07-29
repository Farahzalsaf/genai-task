import React from 'react';

const BookCard = ({ book }) => {
  return (
    <div className="book-item">
      <div className="card">
        <div className="bg"></div>
        <div className="blob"></div>
        <div className="book-cover">
          <img src={book.thumbnail} alt={book.title} />
        </div>
        <p className="heading">{book.title}</p>
      </div>
    </div>
  );
};

export default BookCard;
