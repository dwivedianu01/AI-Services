# RAG PDF Reader 🤖📄

A powerful Retrieval-Augmented Generation (RAG) system that allows you to chat with your PDF documents using AI. Upload PDFs and ask questions to get intelligent answers based on the document content.

![RAG PDF Reader](https://img.shields.io/badge/RAG-PDF--Reader-blue?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

## 🌟 Features

- **Document Q&A**: Ask questions about your PDF documents and get AI-powered answers
- **Multiple PDF Support**: Index and query across multiple PDF files simultaneously
- **Modern UI**: Beautiful, responsive React interface with glassmorphism design
- **Real-time Chat**: Interactive chat interface for natural conversation with your documents
- **Docker Ready**: Easy deployment with Docker Compose
- **FastAPI Backend**: High-performance Python backend with automatic API documentation
- **Vector Search**: FAISS-powered semantic search for accurate information retrieval
- **CORS Enabled**: Seamless frontend-backend communication

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **LangChain** - Framework for developing applications powered by language models
- **OpenAI GPT** - Large language model for generating responses
- **FAISS** - Efficient similarity search and clustering of dense vectors
- **PyPDF** - Pure-Python PDF toolkit
- **Sentence Transformers** - State-of-the-art sentence embeddings

### Frontend
- **React** - Declarative JavaScript library for building user interfaces
- **CSS3** - Modern styling with gradients, animations, and responsive design
- **Axios** - Promise-based HTTP client for API calls

### Infrastructure
- **Docker** - Containerization platform
- **Docker Compose** - Multi-container Docker applications

## � Installation & Setup

Choose your preferred setup method:

### Option 1: Docker (Recommended - Easiest)

#### Quick Docker Setup
```bash
# Clone the repository
git clone https://github.com/your-username/rag-pdf-reader.git
cd rag-pdf-reader

# Set up environment variables
cd backend
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
cd ..

# Add your PDF files to backend/test-data/
# Then run with Docker Compose
docker-compose up --build
```

**That's it!** Your application will be running at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

#### Docker Files Explained
- **`docker-compose.yaml`** - Orchestrates backend and frontend services with proper networking
- **`backend/Dockerfile`** - Python container with FastAPI, LangChain, and all ML dependencies
- **`frontend/Dockerfile`** - Node.js container with React and optimized build process

**Benefits of Docker Setup:**
- ✅ No dependency conflicts
- ✅ Consistent environment across machines
- ✅ Easy scaling and deployment
- ✅ Isolated development environment

### Option 2: Manual Setup (For Development)

#### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirement.txt

# Set up environment
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env

# Add PDF files to test-data/ directory
```

#### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Set up environment
echo "REACT_APP_API_URL=http://localhost:8000" > .env

# Start development server
npm start
```

#### Running Manually
```bash
# Terminal 1: Start backend
cd backend
source venv/bin/activate
uvicorn api:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Start frontend
cd frontend
npm start
```

## 📖 Usage

### Web Interface

1. Open http://localhost:3000 in your browser
2. You'll see a beautiful chat interface
3. Ask questions about your PDF documents
4. Get AI-powered answers based on the document content

### API Usage

#### Chat Endpoint

```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"question": "What is the main topic of the document?"}'
```

**Response:**
```json
{
  "question": "What is the main topic of the document?",
  "answer": "The document discusses..."
}
```

## 🏗️ Project Structure

```
rag-pdf-reader/
├── backend/                    # FastAPI backend
│   ├── api.py                 # Main API endpoints
│   ├── main.py                # Script version
│   ├── config.py              # Configuration
│   ├── requirement.txt        # Python dependencies
│   ├── Dockerfile             # Backend container config
│   ├── .env                   # Environment variables (create this)
│   └── test-data/             # PDF storage and utilities
│       ├── animals_database.txt          # Generated animal data
│       ├── generate_animals_pdf.py       # PDF generation script
│       ├── generate_animals_text.py      # Text generation script
│       ├── ABCmouse-A-Z-Animal-Names-List.pdf
│       ├── dinosaurs-by-d-k-publishing.pdf
│       ├── Giant-Pandas.pdf
│       └── wwf_tigers_e_1.pdf
├── frontend/                  # React frontend
│   ├── src/
│   │   ├── App.js            # Main app component
│   │   ├── Chatbot.js        # Chat interface
│   │   ├── index.js          # App entry point
│   │   └── index.css         # Styling
│   ├── public/
│   ├── package.json          # Node dependencies
│   ├── Dockerfile            # Frontend container config
│   └── .env                  # Environment variables (create this)
├── docker-compose.yaml       # Multi-container orchestration
└── README.md                # This file
```

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

#### Frontend (.env)
```bash
REACT_APP_API_URL=http://localhost:8000
```

### Adding More PDFs

1. Place PDF files in `backend/test-data/`
2. Restart the backend service: `docker-compose restart backend`
3. The system will automatically re-index all PDFs

## 🧪 Testing

### Sample Data

The project includes sample animal data and generation scripts in `backend/test-data/`:

- **`animals_database.txt`** - Text file with 200 animals (Name, Living Places, Max Height, Max Weight, Food)
- **`generate_animals_pdf.py`** - Script to create PDF from animal data
- **`generate_animals_text.py`** - Script to generate animal text data
- **Sample PDFs**: ABCmouse animals, dinosaurs, pandas, and tigers

### Generate More Test Data

```bash
cd backend/test-data
python generate_animals_text.py  # Creates animals_database.txt
python generate_animals_pdf.py   # Creates animals_database.pdf (requires reportlab)
```

### Test Questions

Try asking questions like:
- "What animals live in the African Savannah?"
- "Which animal can reach a height of over 15 meters?"
- "Tell me about carnivorous animals in this database"
- "What is the maximum weight of a Blue Whale?"
- "Which animals are herbivores?"

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Areas for Contribution

- [ ] Add support for more document formats (DOCX, TXT, etc.)
- [ ] Implement user authentication
- [ ] Add document upload via web interface
- [ ] Improve UI/UX design
- [ ] Add support for multiple languages
- [ ] Implement conversation history
- [ ] Add export functionality for chat logs

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI** for providing the GPT models
- **LangChain** for the RAG framework
- **FastAPI** for the excellent web framework
- **React** for the frontend library
- **FAISS** for vector search capabilities

## 📞 Support

If you have any questions or issues:

1. Check the [Issues](https://github.com/your-username/rag-pdf-reader/issues) page
2. Create a new issue with detailed information
3. Join our community discussions

## 🔄 Updates

Stay tuned for updates! We're continuously improving the RAG PDF Reader with new features and enhancements.

---

**Made with ❤️ for document analysis and AI-powered Q&A**

⭐ Star this repo if you find it helpful!</content>
<parameter name="filePath">c:\Users\dwive\AI-Python\AI-Services\rag-pdf-reader\README.md