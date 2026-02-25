from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from model import get_recommendations, RecommendationRequest

app = FastAPI(title="NextRead API", description="ML based book recommender")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to the NextRead API"}

@app.post("/recommend")
async def recommend_books(request: RecommendationRequest):
    try:
        results = get_recommendations(
            query=request.query,
            category=request.category,
            emotion=request.emotion,
            k=request.k
        )

        if not results:
            return {"error": "No books found !!!", "recommendations": []}

        return {"recommendations": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

    