from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.String(20), unique=True, nullable=False)  # Custom book ID (e.g., LIB-2024-001)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100))
    isbn = db.Column(db.String(13), unique=True)
    quantity = db.Column(db.Integer, default=1)
    available = db.Column(db.Integer)
    category = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    location = db.Column(db.String(50))  # Physical location in library
    
    def __repr__(self):
        return f'<Book {self.book_id}: {self.title}>'

class BorrowRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    borrower_name = db.Column(db.String(100), nullable=False)
    borrower_email = db.Column(db.String(120))
    borrower_phone = db.Column(db.String(20))
    borrower_id = db.Column(db.String(50))  # Student/Member ID
    borrowed_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime)
    returned = db.Column(db.Boolean, default=False)
    condition_on_borrow = db.Column(db.String(100))  # Book condition when borrowed
    condition_on_return = db.Column(db.String(100))  # Book condition when returned
    notes = db.Column(db.Text)
    fine_amount = db.Column(db.Float, default=0.0)  # For late returns
    
    book = db.relationship('Book', backref=db.backref('borrow_records', lazy=True))

    def __repr__(self):
        return f'<BorrowRecord {self.borrower_name} - {self.book.title}>'

    def calculate_fine(self, return_date=None):
        if not return_date:
            return_date = datetime.utcnow()
        if return_date > self.due_date:
            days_late = (return_date - self.due_date).days
            return max(0, days_late * 1.0)  # $1 per day
        return 0.0
