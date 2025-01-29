from app import app, db
from models import Book
import pandas as pd
import os
from datetime import datetime

def create_sample_books():
    """Create a list of sample books"""
    return [
        Book(
            book_id="PRG001",
            title="Python Programming",
            author="John Smith",
            category="Programming",
            location="Shelf A1",
            quantity=3,
            available=3
        ),
        Book(
            book_id="PRG002",
            title="Java Fundamentals",
            author="Jane Doe",
            category="Programming",
            location="Shelf A2",
            quantity=2,
            available=2
        ),
        Book(
            book_id="FIC001",
            title="The Great Gatsby",
            author="F. Scott Fitzgerald",
            category="Fiction",
            location="Shelf B1",
            quantity=4,
            available=4
        ),
        Book(
            book_id="FIC002",
            title="To Kill a Mockingbird",
            author="Harper Lee",
            category="Fiction",
            location="Shelf B2",
            quantity=3,
            available=3
        ),
        Book(
            book_id="SCI001",
            title="A Brief History of Time",
            author="Stephen Hawking",
            category="Science",
            location="Shelf C1",
            quantity=2,
            available=2
        )
    ]

def save_books_to_excel(books, excel_path):
    """Save books to Excel file with proper formatting"""
    try:
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(excel_path), exist_ok=True)
        
        # Convert books to DataFrame
        df = pd.DataFrame([{
            'book_id': book.book_id,
            'title': book.title,
            'author': book.author,
            'category': book.category,
            'location': book.location,
            'quantity': book.quantity,
            'available': book.available,
            'created_at': datetime.utcnow().isoformat()
        } for book in books])
        
        print("Creating new Excel template...")
        # Save to Excel with proper formatting
        with pd.ExcelWriter(excel_path, engine='openpyxl', mode='w') as writer:
            df.to_excel(writer, index=False, sheet_name='Books')
            # Auto-adjust columns' width
            worksheet = writer.sheets['Books']
            for idx, col in enumerate(df.columns):
                max_length = max(
                    df[col].astype(str).apply(len).max(),
                    len(col)
                )
                worksheet.column_dimensions[chr(65 + idx)].width = max_length + 2
        
        print(f"Excel template created at: {excel_path}")
        return True
    except Exception as e:
        print(f"Error saving Excel file: {str(e)}")
        return False

def init_db():
    """Initialize the database with books from Excel or create sample books"""
    with app.app_context():
        try:
            # Drop all tables and create new ones
            print("Dropping existing tables...")
            db.drop_all()
            print("Creating new tables...")
            db.create_all()
            
            # Read books from Excel file
            excel_path = os.path.join(os.path.dirname(__file__), 'data', 'books.xlsx')
            books_to_add = []
            
            if os.path.exists(excel_path):
                try:
                    print("Reading existing Excel file...")
                    df = pd.read_excel(excel_path, engine='openpyxl')
                    
                    # Validate required columns
                    required_columns = ['book_id', 'title', 'author', 'category', 'location', 'quantity', 'available']
                    missing_columns = [col for col in required_columns if col not in df.columns]
                    
                    if missing_columns:
                        raise ValueError(f"Excel file is missing required columns: {', '.join(missing_columns)}")
                    
                    # Add each book from the Excel file
                    for _, row in df.iterrows():
                        book = Book(
                            book_id=str(row['book_id']),
                            title=row['title'],
                            author=row['author'],
                            category=row['category'],
                            location=row['location'],
                            quantity=int(row['quantity']),
                            available=int(row['available'])
                        )
                        books_to_add.append(book)
                    
                    print("Books loaded successfully from Excel!")
                    
                except Exception as e:
                    print(f"Error reading Excel file: {str(e)}")
                    print("Falling back to sample books...")
                    books_to_add = create_sample_books()
            else:
                print("Excel file not found. Creating sample books...")
                books_to_add = create_sample_books()
            
            # Add books to database
            for book in books_to_add:
                db.session.add(book)
            
            db.session.commit()
            print(f"Added {len(books_to_add)} books to database")
            
            # If we used sample books or had to recreate the Excel file, save it
            if not os.path.exists(excel_path) or len(books_to_add) == len(create_sample_books()):
                save_books_to_excel(books_to_add, excel_path)
            
        except Exception as e:
            print(f"Error initializing database: {str(e)}")
            db.session.rollback()
            raise e

if __name__ == '__main__':
    init_db()
