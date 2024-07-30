import React from 'react';
import PropTypes from 'prop-types';

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

BookCard.propTypes = {
  book: PropTypes.shape({
    thumbnail: PropTypes.element.isRequired,
    title: PropTypes.string.isRequired,
  }).isRequired,
};

export default BookCard;
