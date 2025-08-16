import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.services.promotion.promotion_route import router as promotion_router
from app.services.menu_generator.menu_generator_route import router as menu_generator_router
from app.services.chatbot.chatbot_route import router as chatbot_router
from app.services.enhanceImage.enhanceImage_route import router as image_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(promotion_router, prefix="/api")
app.include_router(menu_generator_router, prefix="/api")
app.include_router(chatbot_router, prefix="/api")
app.include_router(image_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI application!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.1.0", port=8000, reload=True)

