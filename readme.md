# Fluent Faster API Backend

A comprehensive FastAPI backend service designed for language learning applications, providing multiple AI-powered features including pronunciation analysis, custom phrase generation, shadowing exercises, recall training, and association learning.

## 🚀 Features

### Core Services
- **Pronunciation Analysis** (`/api/pronunciation`) - Analyze and evaluate pronunciation accuracy
- **Custom Phrases** (`/api/phrases`) - Generate custom phrases for language learning
- **Shadowing Exercises** (`/api/shadowing`) - Interactive shadowing practice sessions
- **Recall Training** (`/api/recall`) - Memory and recall exercises
- **Association Learning** (`/api/association`) - Word and concept association training

### Utility Services
- **Text-to-Speech** (`/api/text-to-speech`) - Convert text to speech using Azure Cognitive Services
- **Translation** (`/api/translate`) - Multi-language translation capabilities
- **Sentence Regeneration** (`/api/regenerate-sentence`) - AI-powered sentence reconstruction

## 🛠 Tech Stack

- **Framework**: FastAPI
- **Language**: Python 3.11
- **AI/ML**: Google Generative AI, Groq
- **Text-to-Speech**: Azure Cognitive Services
- **Cloud Storage**: Google Cloud Storage
- **Containerization**: Docker & Docker Compose
- **Server**: Uvicorn ASGI

## 📋 Prerequisites

- Python 3.11+
- Docker (optional, for containerized deployment)
- Google Cloud credentials (for storage and AI services)
- Azure Speech Services credentials
- Groq API key

## 🔧 Installation

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/LucasHernanGames/FFapi-backend.git
   cd FFapi-backend
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install azure-cognitiveservices-speech
   ```

4. **Environment Configuration**
   
   Create a `.env` file in the root directory:
   ```env
   AZURE_SPEECH_KEY=your_azure_speech_key
   AZURE_SPEECH_REGION=your_azure_region
   GROQ_API_KEY=your_groq_api_key
   GOOGLE_APPLICATION_CREDENTIALS=path/to/your/service-account.json
   ```

5. **Run the application**
   ```bash
   python main.py
   ```
   
   The API will be available at `http://127.0.1.0:8000`

### Docker Deployment

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```
   
   The API will be available at `http://localhost:8080`

2. **Or build manually**
   ```bash
   docker build -t fluent-faster-api .
   docker run -p 8080:8080 --env-file .env fluent-faster-api
   ```

## 📚 API Documentation

### Interactive API Documentation
- **Swagger UI**: `http://localhost:8080/docs`
- **ReDoc**: `http://localhost:8080/redoc`

### Main Endpoints

#### Pronunciation Analysis
```http
POST /api/pronunciation
Content-Type: application/json

{
  "text": "Hello world",
  "language": "en-US"
}
```

#### Custom Phrases Generation
```http
POST /api/phrases
Content-Type: application/json

{
  "topic": "travel",
  "difficulty": "intermediate",
  "count": 5
}
```

#### Text-to-Speech
```http
POST /api/text-to-speech
Content-Type: application/json

{
  "text": "Hello, how are you?",
  "language": "en-US",
  "voice_name": "en-US-ChristopherNeural",
  "gender": "Male"
}
```

#### Translation
```http
POST /api/translate
Content-Type: application/json

{
  "text": "Hello world",
  "target_language": "es"
}
```

## 🏗 Project Structure

```
├── app/
│   ├── core/
│   │   └── config.py           # Configuration settings
│   ├── services/
│   │   ├── association/        # Word association learning
│   │   ├── custom_phrases/     # Custom phrase generation
│   │   ├── pronunciation/      # Pronunciation analysis
│   │   ├── recall/            # Memory recall exercises
│   │   └── shadowing/         # Shadowing practice
│   └── utils/
│       ├── regenerate_phrase.py
│       ├── regenerate_sentence.py
│       ├── text_to_speech.py
│       └── translate.py
├── temp_audio/                # Temporary audio files storage
├── docker-compose.yml
├── Dockerfile
├── main.py                   # FastAPI application entry point
├── requirements.txt
└── README.md
```

## 🔐 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `AZURE_SPEECH_KEY` | Azure Cognitive Services Speech key | Yes |
| `AZURE_SPEECH_REGION` | Azure region for speech services | Yes |
| `GROQ_API_KEY` | Groq AI API key | Yes |
| `GOOGLE_APPLICATION_CREDENTIALS` | Path to Google Cloud service account JSON | Yes |

## 🚦 CORS Configuration

The API is configured to accept requests from all origins with the following settings:
- **Origins**: `*` (all origins)
- **Methods**: All HTTP methods
- **Headers**: All headers
- **Credentials**: Enabled

For production deployment, consider restricting CORS origins to your frontend domain.

## 📁 Static Files

The application serves static audio files from the `/temp_audio` directory at the `/temp_audio` endpoint for temporary audio file access.

## 🐳 Docker Configuration

The application runs on:
- **Development**: `127.0.1.0:8000`
- **Docker**: `0.0.0.0:8080`

The Docker container includes optimized installation of Azure Cognitive Services with extended timeouts and retry mechanisms.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is part of the Fluent Faster language learning platform.

## 🛠 Development

### Running Tests
```bash
# Add test commands here when test suite is implemented
pytest
```

### Code Formatting
```bash
# Use black for code formatting
black .
```

### Linting
```bash
# Use flake8 or pylint for linting
flake8 .
```

