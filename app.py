from flask import Flask, request, jsonify, render_template
from models import db, Book, BorrowRecord
import os
from ai_agent import GeminiLibraryAgent
from dotenv import load_dotenv
import asyncio
from functools import wraps
from datetime import datetime, timedelta

load_dotenv()

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Initialize AI agent
library_agent = GeminiLibraryAgent()

def async_route(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return wrapped

def search_books(query_params):
    """Helper function to search books based on query parameters"""
    books = []
    
    # If we have a specific title, search by title first
    if query_params['title']:
        title_query = query_params['title'].strip()
        title_matches = Book.query.filter(
            Book.title.ilike(f"%{title_query}%")
        ).all()
        books.extend(title_matches)
    
    # If no title matches or no title provided, try category
    if not books and query_params['category']:
        category_query = query_params['category'].strip()
        category_matches = Book.query.filter(
            Book.category.ilike(f"%{category_query}%")
        ).all()
        books.extend(category_matches)
    
    # If still no matches, try author
    if not books and query_params['author']:
        author_query = query_params['author'].strip()
        author_matches = Book.query.filter(
            Book.author.ilike(f"%{author_query}%")
        ).all()
        books.extend(author_matches)
    
    # If still no matches and we have a search term, try general search
    if not books and query_params['search_term']:
        search_query = query_params['search_term'].strip()
        matches = Book.query.filter(
            db.or_(
                Book.title.ilike(f"%{search_query}%"),
                Book.author.ilike(f"%{search_query}%"),
                Book.category.ilike(f"%{search_query}%")
            )
        ).all()
        books.extend(matches)
    
    # If still no matches and it's a return query, try searching in borrow records
    if not books and 'return' in query_params.get('intent', '').lower():
        unreturned_records = BorrowRecord.query.filter_by(returned=False).all()
        for record in unreturned_records:
            book = Book.query.get(record.book_id)
            if book and book not in books:
                books.append(book)
    
    return books

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/query', methods=['POST'])
@async_route
async def process_query():
    try:
        data = request.json
        query = data.get('query', '')
        
        # Process query using Gemini AI
        result = await library_agent.process_query(query)
        
        response = {
            'intent': result['intent'],
            'entities': {
                'title': result['title'],
                'author': result['author'],
                'category': result['category'],
                'search_term': result['search_term']
            },
            'message': 'Query processed successfully'
        }
        
        try:
            # Search for books
            books = search_books(result)
            
            # Convert books to dictionary format
            unique_books = []
            seen = set()
            for book in books:
                if book.id not in seen:
                    seen.add(book.id)
                    unique_books.append({
                        'book_id': book.book_id,
                        'title': book.title,
                        'author': book.author,
                        'available': book.available,
                        'quantity': book.quantity,
                        'category': book.category,
                        'location': book.location
                    })
            
            response['books'] = unique_books
            response['natural_response'] = library_agent.format_response(unique_books, result['intent'])
            
            return jsonify(response)
            
        except Exception as e:
            return jsonify({'error': f'Error searching books: {str(e)}'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Error processing query: {str(e)}'}), 500

@app.route('/api/books/<string:book_id>/borrow', methods=['POST'])
def borrow_book(book_id):
    try:
        book = Book.query.filter_by(book_id=book_id).first_or_404()
        
        if book.available <= 0:
            return jsonify({'error': 'Book is not available for borrowing'}), 400
        
        book.available -= 1
        
        # Get borrower details from request
        data = request.json
        borrow_record = BorrowRecord(
            book_id=book.id,
            borrower_name=data['borrower_name'],
            borrower_email=data.get('borrower_email'),
            borrower_phone=data.get('borrower_phone'),
            borrower_id=data.get('borrower_id'),
            due_date=datetime.utcnow() + timedelta(days=14),  # 2 weeks loan period
            condition_on_borrow='Good'
        )
        
        db.session.add(borrow_record)
        db.session.commit()
        
        return jsonify({
            'message': f'Successfully borrowed "{book.title}". Due date: {borrow_record.due_date}',
            'due_date': borrow_record.due_date.isoformat()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error borrowing book: {str(e)}'}), 500

@app.route('/api/books/<string:book_id>/return', methods=['POST'])
def return_book(book_id):
    try:
        book = Book.query.filter_by(book_id=book_id).first_or_404()
        
        if book.available >= book.quantity:
            return jsonify({'error': 'All copies of this book are already returned'}), 400
        
        # Find the active borrow record
        borrow_record = BorrowRecord.query.filter_by(
            book_id=book.id,
            returned=False
        ).first()
        
        if not borrow_record:
            return jsonify({'error': 'No active borrow record found for this book'}), 404
        
        book.available += 1
        borrow_record.returned = True
        borrow_record.return_date = datetime.utcnow()
        
        # Get return condition from request
        data = request.json
        borrow_record.condition_on_return = data.get('condition', 'Good')
        
        # Calculate any fines
        fine = borrow_record.calculate_fine()
        borrow_record.fine_amount = fine
        
        db.session.commit()
        
        response = {
            'message': f'Successfully returned "{book.title}"',
            'fine_amount': fine
        }
        
        if fine > 0:
            response['fine_message'] = f'Late return fine: ${fine:.2f}'
        
        return jsonify(response)
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error returning book: {str(e)}'}), 500

@app.route('/api/books', methods=['GET'])
def get_books():
    try:
        books = Book.query.all()
        return jsonify([{
            'book_id': book.book_id,
            'title': book.title,
            'author': book.author,
            'available': book.available,
            'quantity': book.quantity,
            'category': book.category,
            'location': book.location
        } for book in books])
    except Exception as e:
        return jsonify({'error': f'Error fetching books: {str(e)}'}), 500

@app.route('/api/books', methods=['POST'])
def add_book():
    try:
        data = request.json
        required_fields = ['title', 'author', 'quantity']
        
        # Check for required fields
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Generate a unique book ID (format: LIB-YYYY-XXXX)
        year = datetime.utcnow().year
        last_book = Book.query.order_by(Book.book_id.desc()).first()
        if last_book and last_book.book_id.startswith(f'LIB-{year}-'):
            last_num = int(last_book.book_id.split('-')[-1])
            new_num = str(last_num + 1).zfill(4)
        else:
            new_num = '0001'
        book_id = f'LIB-{year}-{new_num}'
        
        # Create new book
        new_book = Book(
            book_id=book_id,
            title=data['title'],
            author=data['author'],
            isbn=data.get('isbn'),
            quantity=int(data['quantity']),
            available=int(data['quantity']),  # Initially all copies are available
            category=data.get('category', 'Uncategorized'),
            location=data.get('location', 'General Collection')
        )
        
        db.session.add(new_book)
        db.session.commit()
        
        return jsonify({
            'message': 'Book added successfully',
            'book': {
                'book_id': new_book.book_id,
                'title': new_book.title,
                'author': new_book.author,
                'isbn': new_book.isbn,
                'quantity': new_book.quantity,
                'available': new_book.available,
                'category': new_book.category,
                'location': new_book.location
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Error adding book: {str(e)}')
        return jsonify({'error': f'Error adding book: {str(e)}'}), 500

@app.route('/api/books/<string:book_id>/history', methods=['GET'])
def get_book_history(book_id):
    try:
        book = Book.query.filter_by(book_id=book_id).first_or_404()
        records = BorrowRecord.query.filter_by(book_id=book.id).all()
        
        return jsonify([{
            'borrower_name': record.borrower_name,
            'borrowed_date': record.borrowed_date.isoformat(),
            'due_date': record.due_date.isoformat(),
            'return_date': record.return_date.isoformat() if record.return_date else None,
            'returned': record.returned,
            'fine_amount': record.fine_amount
        } for record in records])
    except Exception as e:
        return jsonify({'error': f'Error fetching book history: {str(e)}'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
