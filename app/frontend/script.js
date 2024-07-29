document.addEventListener('DOMContentLoaded', function () {
    const searchButton = document.getElementById('search-button');
    const searchInput = document.getElementById('search-input');

    searchButton.addEventListener('click', function () {
        const query = searchInput.value;
        if (query) {
            fetchSearchedBooks(query);
        } else {
            fetchAllBooks();
        }
    });

    // Fetch all books on page load
    fetchAllBooks();

    function fetchAllBooks() {
        console.log('Fetching all books');
        fetch('http://127.0.0.1:8000/books', {
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            displayBooks(data);
        })
        .catch(error => console.error('Error fetching books:', error));
    }

    function fetchSearchedBooks(query) {
        console.log('Fetching books with query:', query);
        fetch(`http://127.0.0.1:8000/books/search/?q=${encodeURIComponent(query)}`, {
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            displayBooks(data);
        })
        .catch(error => console.error('Error fetching books:', error));
    }

    function displayBooks(data) {
        console.log('Books data:', data);
        const bookGrid = document.getElementById('book-grid');
        bookGrid.innerHTML = '';  // Clear any existing content

        if (data.books && data.books.length > 0) {
            data.books.forEach((metadata) => {
                console.log('Creating book item for:', metadata.title);
                const bookItem = document.createElement('div');
                bookItem.classList.add('book-item');
                bookItem.innerHTML = `
                    <div class="card">
                        <div class="bg"></div>
                        <div class="blob"></div>
                        <div class="book-cover">
                            <img src="${metadata.thumbnail}" alt="${metadata.title}">
                        </div>
                        <p class="heading">${metadata.title}</p>
                    </div>
                `;
                bookGrid.appendChild(bookItem);
                console.log('Appended book item for:', metadata.title);
            });
        } else {
            console.log('No books found');
            bookGrid.innerHTML = '<p>No books found.</p>';
        }
    }
});
