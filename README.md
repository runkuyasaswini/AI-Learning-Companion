# 🎓 AI Learning Companion

> An AI-powered personalized learning platform that combines **Generative AI, Retrieval-Augmented Generation (RAG), Machine Learning, and learner analytics** to provide an adaptive learning experience.

## 📌 Overview

**AI Learning Companion** is an intelligent learning platform designed to support learners throughout the learning lifecycle. Instead of simply presenting course material, the application combines structured courses and topics with AI-assisted learning, context-aware mentoring, dynamically generated quizzes, learning summaries, progress tracking, and performance prediction.

The application is implemented as a **Streamlit** web application with a **Python** backend, **SQLite** persistence, a **FAISS** vector store for semantic retrieval, **Hugging Face Sentence Transformers** for embeddings, and an OpenAI-compatible large language model accessed through environment-based configuration.

## 🎯 Problem Statement

Learners often have access to large amounts of technical content but may find it difficult to decide what to study next, understand material in context, assess their knowledge, and monitor their progress. The goal of this project is to bring these activities together in one learning platform and use AI/ML components to provide contextual assistance and learner insights.

## 💡 Solution

The platform follows a learning workflow that connects:

```text
Course
   ↓
Topic
   ↓
AI-Assisted Learning
   ↓
AI-Generated Quiz
   ↓
Quiz Evaluation
   ↓
Progress Tracking
   ↓
Performance Prediction
   ↓
Personalized AI Guidance
```

The RAG pipeline grounds AI responses in course-specific learning material, while the ML component predicts the probability of success on a learner's next quiz based on learning and assessment features.

## ✨ Key Features

### 👤 Learner Features

- User registration and login
- Learner profile
- Course and topic browsing
- AI-assisted learning experience
- Course/topic-specific AI mentoring
- AI-generated quizzes
- Quiz evaluation and history
- Learning summaries
- Upload-and-summarize PDF workflow
- Learning progress dashboard
- Learning streak tracking
- Course/domain progress tracking
- Achievement tracking
- Weak-topic identification
- Recent learning activity
- Learner performance prediction

### 🤖 AI & RAG Features

- Retrieval-Augmented Generation (RAG)
- PDF document loading and text cleaning
- Recursive document chunking
- Sentence Transformer embeddings
- FAISS vector database
- Semantic retrieval of relevant learning content
- Context-aware AI learning mentor
- Dynamic quiz generation
- Topic/course summaries
- Uploaded PDF summarization
- Configurable LLM endpoint and model through environment variables

### 📊 Machine Learning Features

- Synthetic learner dataset generation
- Data preprocessing
- Categorical feature encoding
- Train/test split
- Random Forest classification
- Learner performance prediction
- Prediction probability
- Model evaluation
- Persisted model and preprocessing artifacts

### 👨‍💼 Admin Features

- Admin dashboard
- Course management
- Topic management
- Learning material management
- Knowledge-base construction
- Platform analytics
- Course popularity analysis
- Quiz performance analysis
- Most-learned topic analysis
- Top learner analysis
- Weak-topic analysis
- Platform-level insights

## 🏗️ System Architecture

```text
                         ┌──────────────────────────┐
                         │       Streamlit UI       │
                         │                          │
                         │ Learner + Admin Modules  │
                         └────────────┬─────────────┘
                                      │
                                      ▼
                         ┌──────────────────────────┐
                         │    Application Router    │
                         │          app.py          │
                         └────────────┬─────────────┘
                                      │
             ┌────────────────────────┼────────────────────────┐
             │                        │                        │
             ▼                        ▼                        ▼
     ┌────────────────┐      ┌─────────────────┐      ┌─────────────────┐
     │ Service Layer  │      │  RAG / AI Layer │      │   ML Layer      │
     │                │      │                 │      │                 │
     │ Auth           │      │ Loader          │      │ Preprocessing   │
     │ Learning       │      │ Chunker         │      │ Random Forest   │
     │ Quiz           │      │ Embeddings      │      │ Prediction      │
     │ Progress       │      │ FAISS           │      │ Evaluation      │
     │ Courses        │      │ Retrieval       │      │                 │
     │ Topics         │      │ Coach / Quiz /  │      │                 │
     │ Materials      │      │ Summary         │      │                 │
     └───────┬────────┘      └────────┬────────┘      └────────┬────────┘
             │                        │                        │
             └────────────────────────┼────────────────────────┘
                                      ▼
                         ┌──────────────────────────┐
                         │        SQLite DB         │
                         │  Users / Learning /     │
                         │  Quizzes / Courses /    │
                         │  Topics / Materials     │
                         └──────────────────────────┘
```

## 🔍 RAG Pipeline

The Retrieval-Augmented Generation workflow is implemented as a reusable pipeline:

```text
PDF / Learning Material
          ↓
     Document Loader
          ↓
       Text Cleaning
          ↓
     Recursive Chunking
          ↓
   Sentence Transformer
       Embeddings
          ↓
      FAISS Index
          ↓
   Semantic Retrieval
          ↓
 Relevant Context Chunks
          ↓
   OpenAI-Compatible LLM
          ↓
 Context-Aware Response
```

The same retrieval approach supports multiple AI features, including the learning mentor, quiz generation, and summaries.

## 🧠 Machine Learning Workflow

The learner-performance module uses a supervised classification workflow:

```text
Learner Data
    ↓
Data Preparation
    ↓
Feature Encoding
    ↓
Train/Test Split
    ↓
Random Forest Classifier
    ↓
Model Evaluation
    ↓
Saved Model + Encoders
    ↓
Learner Input
    ↓
Prediction + Probability
```

The prediction target used by the project is the learner's **next quiz success outcome** (`next_quiz_pass`).

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Web Application | Streamlit |
| Database | SQLite |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn, Random Forest |
| LLM Integration | OpenAI-compatible API through LangChain |
| RAG Framework | LangChain |
| Vector Database | FAISS |
| Embeddings | Hugging Face Sentence Transformers |
| PDF Processing | PyPDF / LangChain PDF loaders |
| Authentication | bcrypt |
| Visualization | Plotly, Matplotlib |
| PDF Export | ReportLab |

## 📂 Project Structure

```text
AI-Learning-Companion/
│
├── app.py                         # Streamlit application entry point
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment-variable template
├── .gitignore                     # Git exclusions
│
├── data/
│   ├── learning_domains.py        # Courses/domains and topic definitions
│   └── knowledge_base/            # Learning documents used by RAG
│
├── database/
│   ├── db.py                      # SQLite connection utilities
│   ├── init_db.py                 # Database initialization
│   ├── seed_users.py              # Sample/user seed utilities
│   └── faiss_index/               # Persisted FAISS vector index
│
├── ml/
│   ├── generate_dataset.py        # Learner dataset generation
│   ├── preprocess.py              # Feature preprocessing
│   ├── train_model.py             # Random Forest training
│   ├── evaluate.py                # Model evaluation
│   ├── predictor.py               # Prediction service logic
│   ├── data/                      # ML dataset
│   └── models/                    # Saved model artifacts
│
├── rag/
│   ├── loader.py                  # Document loading and cleaning
│   ├── chunker.py                 # Document chunking
│   ├── embeddings.py              # Embedding model
│   ├── vector_store.py            # FAISS construction/loading
│   ├── retriever.py               # Semantic retrieval
│   ├── coach_rag.py               # AI mentor/RAG workflow
│   ├── quiz_generator.py          # AI quiz generation
│   └── summary_generator.py       # AI summary generation
│
├── services/
│   ├── auth_service.py            # Authentication and user management
│   ├── learning_service.py        # Learning history
│   ├── quiz_service.py            # Quiz generation/evaluation/history
│   ├── progress_service.py        # Progress and streaks
│   ├── prediction_service.py      # Learner prediction
│   ├── course_service.py          # Course management
│   ├── topic_service.py           # Topic management
│   ├── material_service.py        # Learning material management
│   ├── knowledge_base_service.py  # Knowledge-base construction
│   └── ...
│
├── ui/
│   ├── auth.py                    # Login/registration
│   ├── dashboard.py               # Learner dashboard
│   ├── learn.py                   # Learning interface
│   ├── coach.py                   # AI mentor interface
│   ├── quiz.py                    # Quiz interface
│   ├── progress.py                # Progress dashboard
│   ├── prediction.py              # Performance prediction
│   ├── profile.py                 # Learner profile
│   ├── learning_summary.py        # Learning summaries
│   └── admin_*.py                 # Administration interfaces
│
└── utils/
    ├── config.py                 # Environment/configuration
    ├── helpers.py                # Utility functions
    ├── pdf_export.py             # Summary PDF generation
    └── streak_calendar.py        # Learning streak utilities
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/runkuyasaswini/AI-Learning-Companion.git
cd AI-Learning-Companion
```

### 2. Create a virtual environment

#### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 🔐 Environment Configuration

The application reads configuration from a local `.env` file. **Do not commit `.env` to GitHub.**

Create a local `.env` file using `.env.example` as a template:

```env
GENAI_API_KEY=your_api_key_here
GENAI_BASE_URL=your_base_url_here
GENAI_MODEL=your_model_here

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K=6
FETCH_K=20
```

Use your own authorized API credentials and endpoint values. The repository intentionally contains only `.env.example`, not the actual secret configuration.

## ▶️ Run the Application

From the project root:

```bash
streamlit run app.py
```

Streamlit will start the application locally and provide a browser URL, normally similar to:

```text
http://localhost:8501
```

## 🗃️ Database

The application uses SQLite for persistent application data. Database initialization is handled by `database/init_db.py` and is triggered when the application starts.

The database layer stores application entities such as users, learning history, quiz history, courses, topics, and learning materials.

The local SQLite database file is intentionally excluded from Git using `.gitignore` so that local application state is not committed to the repository.

## 📚 Knowledge Base and RAG

The project supports course-specific learning material and knowledge-base construction. Documents are loaded, cleaned, split into chunks, embedded, and stored in FAISS for semantic retrieval.

The retrieval layer is then used to provide relevant context to the LLM before generating responses.

> **Note:** If the repository's learning documents are sourced from proprietary or restricted training material, verify that you have permission to redistribute them publicly before publishing or sharing the repository.

## 🔒 Security Notes

- Never commit `.env` or API keys.
- Use `.env.example` to document required configuration variables.
- Do not commit passwords or other credentials.
- Review uploaded documents before making a repository public.
- Do not rely on client-side hiding of secrets; keep credentials in environment variables.

## 📸 Screenshots

Add screenshots of the running application here. Suggested screenshots:

```text
screenshots/
├── login.png
├── dashboard.png
├── learning.png
├── ai-coach.png
├── quiz.png
├── progress.png
├── prediction.png
└── admin-dashboard.png
```

Example Markdown:

```markdown
## 📸 Screenshots

### Learner Dashboard
![Learner Dashboard](screenshots/dashboard.png)

### AI Learning Coach
![AI Learning Coach](screenshots/ai-coach.png)

### AI Quiz
![AI Quiz](screenshots/quiz.png)

### Progress Dashboard
![Progress Dashboard](screenshots/progress.png)
```

## 🚀 Future Enhancements

Potential future improvements include:

- Adaptive learning paths
- Voice-based AI tutoring
- AI-generated flashcards
- Coding practice and evaluation
- Certificates and badges
- Mobile-responsive experience
- Multi-language learning support
- Collaborative learning features
- More advanced agentic workflows
- Improved model monitoring and evaluation

## 📌 Project Highlights

This project demonstrates practical integration of:

- Full-stack Python application development with Streamlit
- Authentication and role-based application routing
- Relational data persistence with SQLite
- Retrieval-Augmented Generation
- Vector search with FAISS
- Transformer-based embeddings
- LLM-powered mentoring, quiz generation, and summarization
- Supervised machine learning for learner-performance prediction
- Modular service-layer architecture
- Separate UI, service, RAG, ML, database, and utility components

## 👥 Project

**AI Learning Companion**

An AI/ML learning-platform case study combining personalized learning, RAG, Generative AI, and machine-learning-based learner analytics.

## 📄 License

No license has been specified for this repository yet. If you intend to allow others to reuse, modify, or distribute the code, add an appropriate open-source license after reviewing the licensing requirements for all project components and included materials.
