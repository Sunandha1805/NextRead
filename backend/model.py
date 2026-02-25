import os
import pandas as pd
from typing import Optional, List
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# 1. THE DATA CONTRACT (What the API accepts)
class RecommendationRequest(BaseModel):
    query: str
    category: Optional[str] = None
    emotion: Optional[str] = None
    k: int = 10

# 2. THE ENGINE SETUP (Runs once when server starts)
load_dotenv()
current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_dir, "data")

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

# 3. THE RECOMMENDATION FUNCTION
def get_recommendations(query, category=None, emotion=None, k=10):
    # STEP A: Semantic Search
    # Get the top 50 most similar books from the vector database
    docs = db_books.similarity_search(query, k=50)
    
    # STEP B: Extract ISBNs
    # In your DB, the ISBN is the first part of the page content
    isbns = [doc.page_content.split()[0].strip(' \"') for doc in docs]
    isbns = [int(isbn) for isbn in isbns if isbn.isdigit()]
    
    # STEP C: Retrieve Metadata & Emotions from DataFrame
    # Pull the full book details for these specific ISBNs
    recs = books_emotions[books_emotions["isbn13"].isin(isbns)].copy()
    
    # STEP D: Filtering (By Category)
    if category:
        recs = recs[recs['simple_categories'] == category]
    
    # STEP E: Sorting (By Emotional Tone)
    # If the user wants 'joyful' books, sort by the 'joy' column (highest score first)
    if emotion and emotion in recs.columns:
        recs = recs.sort_values(by=emotion, ascending=False)
        
    # returning k recommended books
    cols_to_return = ['title', 'authors', 'thumbnail']
    return recs.head(k)[cols_to_return].to_dict('records')