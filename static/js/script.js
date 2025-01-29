// Function to handle adding a new book
async function addBook() {
    const title = document.getElementById('bookTitle').value;
    const author = document.getElementById('bookAuthor').value;
    const isbn = document.getElementById('bookISBN').value;
    const quantity = parseInt(document.getElementById('bookQuantity').value);
    const category = document.getElementById('bookCategory').value;

    if (!title || !author || !quantity) {
        showError('Please fill in all required fields');
        return;
    }

    try {
        const response = await fetch('/api/books', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                title,
                author,
                isbn,
                quantity,
                category
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Error adding book');
        }

        // Show success message
        showSuccess('Book added successfully');
        
        // Clear the form
        document.getElementById('addBookForm').reset();
        
        // Close the modal
        const modal = document.getElementById('addBookModal');
        if (modal) {
            modal.style.display = 'none';
        }

    } catch (error) {
        showError(error.message);
    }
}

// Function to show error message
function showError(message) {
    const errorDiv = document.getElementById('errorMessage');
    if (errorDiv) {
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
        setTimeout(() => {
            errorDiv.style.display = 'none';
        }, 5000);
    }
}

// Function to show success message
function showSuccess(message) {
    const successDiv = document.getElementById('successMessage');
    if (successDiv) {
        successDiv.textContent = message;
        successDiv.style.display = 'block';
        setTimeout(() => {
            successDiv.style.display = 'none';
        }, 5000);
    }
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    const addBookForm = document.getElementById('addBookForm');
    if (addBookForm) {
        addBookForm.addEventListener('submit', (e) => {
            e.preventDefault();
            addBook();
        });
    }
});
