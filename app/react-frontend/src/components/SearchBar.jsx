import React from 'react';
import PropTypes from 'prop-types';

const SearchBar = ({ query, setQuery, onSearch }) => {
  return (
    <div className="search-bar-container">
      <div className="search-bar">
        <input
          type="text"
          placeholder="Search for books..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button className="button" onClick={onSearch}>
          <span style={{ position: 'relative', zIndex: 1 }}>Search</span>
          <div className="bg"></div>
          <div className="blob"></div>
        </button>
      </div>
    </div>
  );
};

SearchBar.propTypes = {
  query: PropTypes.string.isRequired,
  setQuery: PropTypes.func.isRequired,
  onSearch: PropTypes.func.isRequired,
};

export default SearchBar;
