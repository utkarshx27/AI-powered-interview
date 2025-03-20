# AI Powered Interview

## Overview
AI Powered Interview is an intelligent job interviewing system that leverages AI to conduct structured, real-time interviews with candidates. The system interacts with the candidate, asks tailored technical questions based on their provided skills, and securely stores interview data for further review.

## Features
- AI-driven job interview simulation.
- Tailored technical questions based on the candidate's skill set.
- Secure encryption and storage of candidate data.
- Conversational interview experience with follow-up questions.
- Automated interview flow with clear guidance.
- Data persistence using CSV storage (future integration with databases like MongoDB/SQL planned).

## Tech Stack
- **Backend:** Python, LangChain, OpenAI API
- **Frontend:** Streamlit / FastAPI
- **Security:** Cryptography (Fernet encryption)
- **Data Storage:** CSV (Future plans for MongoDB/SQL)
- **Environment Management:** dotenv

## Installation
### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- pip
- Virtual Environment (optional but recommended)

### Steps
1. Clone the repository:
   ```sh
   git clone <repo-url>
   cd AI-Powered-Interview
   ```
2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   - Create a `.env` file and add your OpenAI API key:
     ```
     OPENAI_API_KEY=your-api-key-here
     ```

## Usage
Run the Streamlit application:
```sh
streamlit run main_streamlit.py
```

### How It Works
1. Start the AI interview process.
2. The AI asks the candidate for basic details (name, email, experience, tech stack, etc.).
3. Based on the provided tech stack, AI generates and asks tailored technical questions.
4. The conversation history is stored securely with encryption.
5. The interview concludes, and data is saved for future reference.

## Future Enhancements
- **Integration with MongoDB/SQL** for structured candidate data storage.
- **Code evaluation** by integrating a compiler.
- **RAG (Retrieval-Augmented Generation) model** for handling out-of-scope questions.
- **Resume parsing with vector search.**
- **Computer Vision Analysis** for body language evaluation.
- **Text-to-Speech and Speech-to-Text** for voice-based interviews.
- **Fine-tuned AI model** for human-like interview interactions.
- **Pydantic-based Input Validation** for better data consistency.

## Security Considerations
- Uses **Fernet encryption** to protect candidate data.
- Ensures limited file permissions for saved data.
- Secure API key handling with dotenv.

## Contributing
Contributions are welcome! Feel free to fork this repository, create a branch, and submit a pull request.

---
For questions or support, contact **Utkarsh Singh** at [utkarshsinghx27@gmail.com](mailto:utkarshsinghx27@gmail.com).

