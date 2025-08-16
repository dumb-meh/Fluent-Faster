# MenuGo

MenuGo is a modular FastAPI application for restaurant menu generation, chatbot interaction, and promotional offer creation using OpenAI APIs.

## Features

- **Menu Generator**: Generate creative restaurant menus using AI.
- **Chatbot**: Interact with an AI-powered chatbot.
- **Promotion Generator**: Create promotional offers for your restaurant.
- **Image Variation**: Upload an image and get a new, AI-generated variation in a slightly different style using OpenAI's DALL-E 2.

## Project Structure
- `main.py` – FastAPI entrypoint, includes all routers.
- `app/services/menu_generator/` – Menu generation logic and API.
- `app/services/promotion/` – Promotion offer and image prompt generation.
- `app/services/chatbot/` – Chatbot logic and API.
- `app/core/config.py` – App configuration using environment variables.

## API Endpoints

- `POST /api/menu-generator/generate-menu` – Generate a restaurant menu.
- `POST /api/chatbot/chat` – Interact with the chatbot.
- `POST /api/promotion/generate-offer/` – Generate a promotional offer.
- `POST /api/enhance-image` – Upload an image and receive a new, AI-generated variation in a slightly different style.

## Setup
1. **Clone the repository**
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set environment variables**
   - Create a `.env` file with your OpenAI API key:
     ```env
     OPENAI_API_KEY=your_openai_api_key
     ```
4. **Run locally**
   ```bash
   uvicorn main:app --reload
   ```
5. **Run with Docker**
   - Build and start:
     ```bash
     docker-compose up --build
     ```

## File Ignore
- `.gitignore` and `.dockerignore` are set up to exclude cache, logs, environments, and temp/static images.

## Notes
- Requires Python 3.11+
- Make sure Docker Desktop is running if using Docker on Windows.
- All AI features require a valid OpenAI API key.

---

For more details, see the code in each service directory.
