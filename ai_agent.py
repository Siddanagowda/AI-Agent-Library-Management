import google.generativeai as genai
from typing import Dict, List
import os
from dotenv import load_dotenv

load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

class GeminiLibraryAgent:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-pro')
        self.context = """
        You are a library assistant. Your task is to help users find books and understand their queries.
        Extract the following information from user queries:
        - Intent (search, borrow, return, availability)
        - Book title (if mentioned)
        - Author name (if mentioned)
        - Category (if mentioned)
        - General search term (if no specific title/author/category)
        
        Format your response as a JSON-like structure with these fields.
        """

    async def process_query(self, query: str) -> Dict:
        try:
            # Default response structure
            response = {
                'intent': 'search',
                'title': None,
                'author': None,
                'category': None,
                'search_term': None
            }
            
            # Process with Gemini
            prompt = f"{self.context}\nAnalyze this query: {query}"
            result = self.model.generate_content(prompt)
            
            # Extract information from Gemini's response
            if result.text:
                if "borrow" in query.lower():
                    response['intent'] = 'borrow'
                elif "return" in query.lower():
                    response['intent'] = 'return'
                elif "available" in query.lower():
                    response['intent'] = 'availability'
                
                # Look for title in quotes
                if '"' in query:
                    parts = query.split('"')
                    if len(parts) >= 3:
                        response['title'] = parts[1]
                
                # Look for author after "by"
                if 'by' in query.lower():
                    parts = query.lower().split('by')
                    if len(parts) >= 2:
                        response['author'] = parts[1].strip()
                
                # Check for common categories
                categories = ['fiction', 'non-fiction', 'programming', 'science', 'history']
                for category in categories:
                    if category in query.lower():
                        response['category'] = category
                        break
                
                # If no specific fields found, use as general search term
                if not any([response['title'], response['author'], response['category']]):
                    response['search_term'] = query
            
            return response
            
        except Exception as e:
            print(f"Error processing query with Gemini: {str(e)}")
            # Fallback to basic processing
            return {
                'intent': 'search',
                'title': None,
                'author': None,
                'category': None,
                'search_term': query
            }

    def format_response(self, books: List[Dict], intent: str) -> str:
        if not books:
            return "I couldn't find any books matching your query."
        
        if intent == 'availability':
            book = books[0]  # Take the first book for availability check
            if book['available'] > 0:
                return f"Yes, '{book['title']}' is available! There are {book['available']} copies available out of {book['quantity']}. You can find it at {book['location']}."
            else:
                return f"Sorry, '{book['title']}' is currently not available. All {book['quantity']} copies are borrowed."
        
        elif intent == 'search':
            if len(books) == 1:
                book = books[0]
                return f"I found '{book['title']}' by {book['author']}. It's located at {book['location']}."
            else:
                return f"I found {len(books)} books that match your query. You can see them listed below."
        
        elif intent == 'borrow':
            book = books[0]
            if book['available'] > 0:
                return f"You can borrow '{book['title']}'. Please click the Borrow button and fill in your details."
            else:
                return f"Sorry, '{book['title']}' is not available for borrowing at the moment."
        
        elif intent == 'return':
            return "To return a book, please visit the library desk with your book and borrower ID."
        
        return "How can I help you find books today?"
