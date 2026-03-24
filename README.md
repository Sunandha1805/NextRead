# 📚 NextRead

> **Discover books that match your curiosity and mood.**

NextRead is an ML-powered book recommendation engine that combines **semantic search**, **category filtering**, and **emotion-based sorting** to surface the perfect next book for any reader. Type a natural language query, optionally pick a category and mood, and get personalised recommendations in seconds.

---

## ✨ Features

- **Semantic Search** — Uses [BAAI/bge-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5) sentence embeddings with ChromaDB to find books by meaning, not just keywords.
- **Category Filtering** — Filter results by broad categories (Fiction, Nonfiction, Children's Fiction, Children's Nonfiction) or use free-text categories (Business, Science, Philosophy, etc.) to refine the semantic search.
- **Emotion Sorting** — Sort recommendations by emotional tone — joy, sadness, surprise, fear, anger, or neutral — using pre-computed sentiment scores.
- **Modern Frontend** — Clean, responsive React UI with a glassmorphism-inspired dark theme.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | React 19 · TypeScript · Vite · Axios |
| **Backend** | Python 3.11 · FastAPI · Uvicorn |
| **ML / NLP** | Sentence-Transformers · LangChain · HuggingFace Embeddings |
| **Vector DB** | ChromaDB (via LangChain-Chroma) |
| **Data** | Pandas · NumPy |
| **Deployment** | Render (backend) · Vite static build (frontend) |

---

## 📂 Project Structure

```
NextRead/
├── backend/
│   ├── data/                   # Pre-built ChromaDB + emotion-scored CSV
│   │   ├── chroma_db_bge/      # Vector database (BGE embeddings)
│   │   └── books_with_emotions.csv
│   ├── main.py                 # FastAPI app & API routes
│   ├── model.py                # Recommendation engine (search + filter + sort)
│   ├── requirements.txt        # Python dependencies
│   ├── .env.example            # Environment variable template
│   └── .python-version         # Python 3.11.12
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── SearchForm.tsx   # Search bar + category/emotion filters
│   │   │   ├── BookList.tsx     # Grid layout for book cards
│   │   │   └── BookCard.tsx     # Individual book card (cover, title, author)
│   │   ├── App.tsx              # Root component & API integration
│   │   └── App.css              # Global styles & dark theme
│   ├── package.json
│   └── index.html
├── notebook/                    # Jupyter notebooks (data pipeline)
│   ├── data-exploration.ipynb   # Dataset cleaning & analysis
│   ├── sentiment-analysis.ipynb # Emotion score computation
│   └── vector-search.ipynb      # Embedding generation & ChromaDB creation
├── requirements.txt             # Root-level Python dependencies
└── .gitignore
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.11+**
- **Node.js 18+** and **npm**
- A **Hugging Face** token (for downloading the embedding model)

### 1. Clone the repository

```bash
git clone https://github.com/your-username/NextRead.git
cd NextRead
```

### 2. Backend setup

```bash
cd backend

# Create and activate a virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and add your HF_TOKEN
```

### 3. Frontend setup

```bash
cd frontend
npm install
```

### 4. Run the app

**Start the backend** (from `backend/`):

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

**Start the frontend** (from `frontend/`):

```bash
npm run dev
```

The UI will be available at `http://localhost:5173`.

---

## ⚙️ Environment Variables

### Backend (`backend/.env`)

| Variable | Description | Default |
|---|---|---|
| `HF_TOKEN` | Hugging Face API token (model download) | — |
| `OPENAI_API_KEY` | OpenAI key (optional, for future GPT features) | — |
| `FRONTEND_URL` | Allowed CORS origin | `http://localhost:5173` |

### Frontend (`frontend/.env`)

| Variable | Description | Default |
|---|---|---|
| `VITE_API_URL` | Backend API base URL | `http://127.0.0.1:8000` |

---

## 📡 API Reference

### `GET /`

Health check — returns a welcome message.

### `POST /recommend`

Returns book recommendations based on the request body.

**Request Body:**

```json
{
  "query": "books about time travel and adventure",
  "category": "Fiction",
  "emotion": "joy",
  "k": 16
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `query` | string | ✅ | Natural language description of desired books |
| `category` | string | ❌ | Category filter or search refinement |
| `emotion` | string | ❌ | Emotion to sort by (`joy`, `sadness`, `fear`, `surprise`, `anger`, `neutral`) |
| `k` | integer | ❌ | Number of results to return (default: `16`) |

**Response:**

```json
{
  "recommendations": [
    {
      "title": "The Time Machine",
      "authors": "H.G. Wells",
      "thumbnail": "https://..."
    }
  ]
}
```

---

## 🔬 How It Works

1. **Data Pipeline** (Jupyter notebooks) — The raw book dataset is cleaned, enriched with category tags, and scored for emotional tone using NLP models. Book descriptions are embedded with `BAAI/bge-small-en-v1.5` and stored in a ChromaDB vector database.

2. **Semantic Search** — When a user submits a query, the backend embeds it with the same model and retrieves the top 50 most similar books from ChromaDB.

3. **Category Filtering** — If the user selects a predefined category (Fiction, Nonfiction, etc.), results are filtered. Free-text categories (e.g., "Business") are appended to the query to boost semantic relevance.

4. **Emotion Sorting** — If a mood is selected, results are sorted by the corresponding pre-computed emotion score (highest first).

5. **Results** — The top `k` books (title, author, cover image) are returned to the frontend and displayed in a responsive card grid.

---

## 📓 Notebooks

The `notebook/` directory contains the data science pipeline:

| Notebook | Purpose |
|---|---|
| `data-exploration.ipynb` | Dataset cleaning, deduplication, and exploratory analysis |
| `sentiment-analysis.ipynb` | Emotion classification using NLP — generates emotion scores per book |
| `vector-search.ipynb` | Generates BGE embeddings and builds the ChromaDB vector database |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
