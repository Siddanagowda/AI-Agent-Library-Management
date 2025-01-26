import spacy

class AIAgentLibraryManagementSystem:
    def __init__(self):
        # Sample book collection with availability status
        self.books = {
            "1984": {"available": True},
            "To Kill a Mockingbird": {"available": True},
            "The Great Gatsby": {"available": False},
            "Moby Dick": {"available": True}
        }
        # Load spaCy NLP model for intent recognition
        self.nlp = spacy.load("en_core_web_sm")

    def check_availability(self, book_title):
        """Check if a book is available."""
        if book_title in self.books:
            return f"'{book_title}' is {'available' if self.books[book_title]['available'] else 'not available'}."
        else:
            return f"Sorry, '{book_title}' does not exist in the library."

    def borrow_book(self, book_title):
        """Borrow a book if available."""
        if book_title in self.books:
            if self.books[book_title]["available"]:
                self.books[book_title]["available"] = False
                return f"You have successfully borrowed '{book_title}'."
            else:
                return f"Sorry, '{book_title}' is currently not available."
        else:
            return f"'{book_title}' does not exist in the library."

    def return_book(self, book_title):
        """Return a borrowed book."""
        if book_title in self.books:
            if not self.books[book_title]["available"]:
                self.books[book_title]["available"] = True
                return f"Thank you for returning '{book_title}'."
            else:
                return f"'{book_title}' was not borrowed."
        else:
            return f"'{book_title}' does not exist in the library."

    def extract_intent_and_entity(self, user_input):
        #Use NLP to extract intent and book title from user input."""
      doc = self.nlp(user_input.lower())  # Lowercase the input for consistency
      intent = None
      book_title = None

        # Detect intent based on keywords
      if any(token.lemma_ in ["borrow", "take"] for token in doc):
          intent = "borrow"
      elif any(token.lemma_ in ["return", "give"] for token in doc):
          intent = "return"
      elif any(token.lemma_ in ["check", "available", "availability"] for token in doc):
          intent = "check_availability"

        # Match book title from the library directly
      book_title = next((book for book in self.books if book.lower() in user_input.lower()), None)

        # Use NLP only if direct matching fails
      if not book_title:
          for ent in doc.ents:
              if ent.label_ == "WORK_OF_ART":
                  book_title = ent.text
                  break

      return intent, book_title


    def respond(self, user_input):
        """Respond to user queries using AI-driven intent recognition."""
        intent, book_title = self.extract_intent_and_entity(user_input)

        if not intent:
            return "I'm sorry, I couldn't understand your request. Please ask about borrowing, returning, or checking availability of books."

        if not book_title:
            return "Could you please specify the name of the book?"

        # Execute actions based on detected intent
        if intent == "check_availability":
            return self.check_availability(book_title)
        elif intent == "borrow":
            return self.borrow_book(book_title)
        elif intent == "return":
            return self.return_book(book_title)
        else:
            return "I'm sorry, I couldn't process your request."

# Example usage
if __name__ == "__main__":
    ai_agent_lms = AIAgentLibraryManagementSystem()

    print(ai_agent_lms.respond("Is '1984' available?"))  # Output: '1984' is available.
    print(ai_agent_lms.respond("Can I borrow '1984'?"))  # Output: You have successfully borrowed '1984'.
    print(ai_agent_lms.respond("I'd like to return '1984'."))  # Output: Thank you for returning '1984'.
