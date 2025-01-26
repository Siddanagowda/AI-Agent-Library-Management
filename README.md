# 🤖 AI-Powered Library Management System

A smart library management system that uses Natural Language Processing (NLP) to understand and process user requests for borrowing, returning, and checking the availability of books. 📚

## ✨ Features

- 🧠 Natural language understanding for user queries
- 📊 Book availability checking
- 📖 Book borrowing system
- 🔄 Book return processing
- 🎯 Intelligent intent recognition using spaCy NLP

## 🛠️ Requirements

- Python 3.x
- spaCy
- spaCy English language model (`en_core_web_sm`)

## 🚀 Installation

1. Install the required packages:
```bash
pip install spacy
python -m spacy download en_core_web_sm
```

2. Clone this repository or download the source code.

## 💡 Usage

The system can process natural language queries for the following operations:

1. **Check Book Availability**
   ```python
   "Is '1984' available?" 
   ```

2. **Borrow a Book**
   ```python
   "Can I borrow '1984'?"
   ```

3. **Return a Book**
   ```python
   "I'd like to return '1984'."
   ```

## ⚙️ How it Works

The system uses spaCy's NLP capabilities to:
- Extract user intent (borrow, return, or check availability)
- Identify book titles in natural language queries
- Process requests and maintain book availability status

## 🧩 AI Agent Capabilities

The system is powered by an intelligent AI agent that enhances the library management experience:

### 🗣️ Natural Language Understanding
- Processes user queries in natural language format
- Uses spaCy's advanced NLP model for intent recognition
- Understands various ways of expressing the same request (e.g., "Can I borrow", "I want to take", "Let me have")

### 🎯 Smart Intent Detection
- Automatically identifies three main types of intents:
  - 📋 Book availability checks
  - 📤 Borrowing requests
  - 📥 Return requests
- Uses lemmatization to understand different word forms (e.g., "borrow", "borrowing", "borrowed")

### 🔍 Entity Recognition
- Identifies book titles within natural language queries
- Uses both direct matching and spaCy's entity recognition for book title extraction
- Handles cases where book titles might be mentioned in different formats

### ⚡ Error Handling
- Provides helpful feedback when requests are unclear
- Prompts for missing information (e.g., when book title is not specified)
- Maintains accurate tracking of book availability status

## 💻 Example

```python
from app import AIAgentLibraryManagementSystem

ai_agent_lms = AIAgentLibraryManagementSystem()
response = ai_agent_lms.respond("Is '1984' available?")
print(response)  # Output: '1984' is available.
```

## 📚 Current Book Collection

The system comes with a sample collection of books:
- 1984
- To Kill a Mockingbird
- The Great Gatsby
- Moby Dick

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.
