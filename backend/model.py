import os
import pandas as pd
from typing import Optional, List
from pydantic import BaseModel
from dotenv import load_dotenv

# 1. THE DATA CONTRACT (What the API accepts)
class RecommendationRequest(BaseModel):
    query: str
    category: Optional[str] = None
    emotion: Optional[str] = None
    k: int = 16

# 2. THE ENGINE SETUP (Lazy-loaded so uvicorn can bind the port first)
load_dotenv()
current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_dir, "data")

# Global references — initialized in init_models()
embeddings = None
db_books = None
books_emotions = None

def init_models():
    """Load AI models and data. Called once during FastAPI startup (after port is bound)."""
    global embeddings, db_books, books_emotions

    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain_chroma import Chroma

    print("Loading AI Models and Data...")
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")

    # Open the Vector DB we created in the notebook
    db_books = Chroma(
        persist_directory=os.path.join(data_path, "chroma_db_bge"), 
        embedding_function=embeddings
    )

    # Load the CSV with the pre-calculated emotion scores
    books_emotions = pd.read_csv(os.path.join(data_path, "books_with_emotions.csv"))
    placeholder = "https://www.forewordreviews.com/books/covers/28-business-thinkers-who-changed-the-world.jpg"
    books_emotions["thumbnail"] = books_emotions["thumbnail"].fillna(placeholder)
    print("Models and Data loaded successfully!")

# Predefined broad categories in the dataset
VALID_CATEGORIES = {'Fiction', 'Nonfiction', "Children's Fiction", "Children's Nonfiction"}

# 3. THE RECOMMENDATION FUNCTION
def get_recommendations(query, category=None, emotion=None, k=16):
    # STEP A: Semantic Search
    # If category is not a predefined one, enhance the query with it
    search_query = query
    filter_category = None
    if category:
        if category in VALID_CATEGORIES:
            filter_category = category
        else:
            # Use the category as part of the semantic search (e.g. "business", "science")
            search_query = f"{category} {query}"
    
    # Get the top 50 most similar books from the vector database
    docs = db_books.similarity_search(search_query, k=50)
    
    # STEP B: Extract ISBNs
    # In your DB, the ISBN is the first part of the page content
    isbns = [doc.page_content.split()[0].strip(' \"') for doc in docs]
    isbns = [int(isbn) for isbn in isbns if isbn.isdigit()]
    
    # STEP C: Retrieve Metadata & Emotions from DataFrame
    # Pull the full book details for these specific ISBNs
    recs = books_emotions[books_emotions["isbn13"].isin(isbns)].copy()
    
    # STEP D: Filtering (By Category — only if it's a predefined one)
    if filter_category:
        recs = recs[recs['simple_categories'] == filter_category]
    
    # STEP E: Sorting (By Emotional Tone)
    # If the user wants 'joyful' books, sort by the 'joy' column (highest score first)
    if emotion and emotion in recs.columns:
        recs = recs.sort_values(by=emotion, ascending=False)
        
    # returning k recommended books
    cols_to_return = ['title', 'authors', 'thumbnail']
    return recs.head(k)[cols_to_return].to_dict('records')