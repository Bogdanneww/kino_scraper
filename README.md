# 🎬 Kino Scraper API

Asynchronous REST API service for scraping movie data from  
👉 https://ua.kinorium.com/

Built as a test task for a Trainee / Junior Python Developer position.

---

## 🚀 Features

- 🔎 Scrape movies by genre using simple HTTP requests
- 🎥 Scrape detailed movie information using a **headless browser** (Playwright)
- 🖥 Open movie page in a **non-headless browser**
- ⚡ Fully asynchronous FastAPI application
- 📦 Clean project structure (routers / services / schemas / crud)
- 🧪 Pydantic validation & OpenAPI documentation
- 📄 Swagger UI available at `/docs`

---

## 🧱 Tech Stack

- Python 3.11+
- FastAPI
- httpx + BeautifulSoup
- Playwright (Chromium)
- Pydantic v2
- pytest (async)

---

## 🛠 Installation (Local)
### 1️⃣ Create virtual environment
 
python -m venv .venv
### Windows
.venv\Scripts\activate

### macOS/Linux
source .venv/bin/activate

### 2️⃣ Install dependencies
pip install -r requirements.txt

playwright install
### 3️⃣ Run application
uvicorn app.main:app --reload


### API will be available at:
👉 http://127.0.0.1:8000

👉 Swagger docs: http://127.0.0.1:8000/docs

### 🐳 Run with Docker
docker-compose up --build

### 🔗 API Endpoints
### 🔹 GET /scrape/genre

Scrape movies by genre using simple HTTP requests.

Query params:

genre — movie genre (required)

page — page number (optional)

### 🔹 POST /scrape/movie/details

Scrape detailed movie information using headless Playwright.

Request body:

{
  "title": "Inception"
}

### 🔹 POST /scrape/movie/open

Open movie page in a visible browser window.

Request body:

{
  "title": "Inception"
}

### 🧪 Run Tests
pytest

### ⚠️ Notes

Non-headless browser requires GUI support on the host machine

Kinorium page structure may change over time

### 👤 Author

Developed by Bohdan Mykyichuk
