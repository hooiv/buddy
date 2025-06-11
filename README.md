# Buddy - Your Virtual Chat Companion 🤖

A fun chat website where you can talk to your virtual "buddy" - a lovable, slang-talking friend who knows all about you but is hilariously clueless about general knowledge!

## Features

- 💬 Real-time chat with your virtual buddy
- 🗣️ Slang-heavy, casual conversation style
- 👤 Personalized responses based on your background and interests
- 🤪 Hilariously fails at general knowledge questions
- 📱 Responsive design for all devices
- 🚀 Modern tech stack (React + FastAPI)

## Tech Stack

**Frontend:**
- React 18 with Vite
- Modern CSS with responsive design
- Axios for API communication

**Backend:**
- Python FastAPI
- Groq AI API integration
- CORS middleware for cross-origin requests

## Setup Instructions

### Prerequisites
- Node.js (v16 or higher)
- Python 3.8+
- Groq API key

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your Groq API key:
```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

5. Run the backend server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

4. Open your browser and go to `http://localhost:5173`

## Environment Variables

Create a `.env` file in the backend directory with:
```
GROQ_API_KEY=your_groq_api_key_here
```

## Usage

1. Start both backend and frontend servers
2. Open the website in your browser
3. Start chatting with your buddy!
4. Try asking personal questions vs general knowledge questions to see the difference

## Demo

Your buddy will:
- ✅ Answer questions about your life, hobbies, and interests
- ✅ Give advice and suggestions in a friendly, casual tone
- ❌ Hilariously fail at general knowledge questions
- 🎭 Always respond with slang and casual language

## Contributing

Feel free to fork this project and make it your own! Customize the buddy's personality and knowledge base to match your preferences.

## License

MIT License - feel free to use this project however you'd like!
