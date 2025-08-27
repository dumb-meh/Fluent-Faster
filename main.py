import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.services.pronunciation.pronunciation_route import router as pronunciation_router 
from app.services.recall.recall_route import router as recall_router
from app.services.association.association_route import router as association_router
from app.services.shadowing.shadowing_route import router as shadowing_router
from app.utils.regenerate_sentence import router as regenerate_sentence_router
from app.utils.text_to_speech import router as text_to_speech_router
from app.utils.translate import router as translate_router
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(pronunciation_router , prefix="/api")
app.include_router(recall_router, prefix="/api")
app.include_router(association_router, prefix="/api")
app.include_router(shadowing_router, prefix="/api")
app.include_router(regenerate_sentence_router, prefix="/api")
app.include_router(text_to_speech_router, prefix="/api")
app.include_router(translate_router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI application!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.1.0", port=8000, reload=True)

