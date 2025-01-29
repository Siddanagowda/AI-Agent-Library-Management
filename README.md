# 🤖 AI-Powered Library Management System

A modern, web-based library management system powered by Google's Gemini AI that helps manage books, borrowing, and returns with natural language processing capabilities. 📚

## ✨ Features

- 🔍 **Natural Language Search**: Ask for books in plain English
- 📚 **Smart Book Management**: 
  - 📊 Excel-based book database
  - 🔄 Automatic book tracking
  - 📍 Location management
- 📖 **Borrowing System**:
  - 📝 Track borrowed books
  - ⏰ Automatic due date calculation
  - 💰 Late return fine calculation ($1/day)
- 🧠 **AI-Powered Assistance**:
  - 💬 Natural language understanding
  - 📋 Smart book recommendations
  - 🎯 Context-aware responses

## 🛠️ Technology Stack

- 🔙 **Backend**: Python, Flask
- 🗄️ **Database**: SQLite, SQLAlchemy
- 🎨 **Frontend**: HTML, JavaScript, Bootstrap
- 🤖 **AI**: Google Gemini AI
- 💾 **Data Storage**: Excel (openpyxl)

## 📋 Prerequisites

- 🐍 Python 3.8 or higher
- 🔑 Google Gemini API key

## 🚀 Installation

1. 📥 Clone the repository:
```bash
git clone https://github.com/Siddanagowda/AI-Agent-Library-Management.git
cd AI-Agent-Library-Management
```

2. 📦 Install dependencies:
```bash
pip install -r requirements.txt
```

3. ⚙️ Set up environment variables:
Create a `.env` file in the root directory:
```
GOOGLE_API_KEY=your_gemini_api_key_here
```

4. 🗃️ Initialize the database:
```bash
python init_db.py
```

5. 🚀 Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000` 🌐

## 📖 Usage

### 📚 Managing Books

1. 📝 **Adding Books**:
   - Update the `data/books.xlsx` file
   - Run `python init_db.py` to update the database

2. 🔍 **Searching Books**:
   - Use natural language: "Find me programming books"
   - Search by title: "Do you have Brief History of Time?"
   - Search by author: "Books by Stephen Hawking"

3. 📚 **Borrowing Books**:
   - Click "Borrow" on any available book
   - Fill in borrower details
   - Note the due date (14 days from borrowing)

4. 📬 **Returning Books**:
   - Click "Return" on borrowed books
   - Note the book's condition
   - Pay any applicable late fees

### 💰 Fine System

- ⏰ Late returns incur a $1/day fine
- 🧮 Fines are automatically calculated
- 📊 Fine history is maintained in the system

## 📁 Project Structure

```
AI-Agent-Library-Management/
├── 🐍 app.py              # Main Flask application
├── 📊 models.py           # Database models
├── 🤖 ai_agent.py         # Gemini AI integration
├── 🗃️ init_db.py          # Database initialization
├── 📋 requirements.txt    # Python dependencies
├── 📁 data/
│   └── 📚 books.xlsx     # Book database
└── 📁 templates/
    └── 🎨 index.html     # Web interface
```

## 🔌 API Endpoints

- 🏠 `GET /`: Home page
- 💬 `POST /api/query`: Process natural language queries
- 📚 `GET /api/books`: List all books
- 📤 `POST /api/books/<book_id>/borrow`: Borrow a book
- 📥 `POST /api/books/<book_id>/return`: Return a book
- 📊 `GET /api/books/<book_id>/history`: Get book history

## 🤝 Contributing

1. 🔀 Fork the repository
2. 🌿 Create a feature branch
3. ✍️ Commit your changes
4. 🚀 Push to the branch
5. 📬 Create a Pull Request

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- 🤖 Google Gemini AI for natural language processing
- 🌐 Flask team for the web framework
- 🎨 Bootstrap team for the UI components
