# Kinorium Scraper API

**Asynchronous FastAPI service for scraping movies from Kinorium.**

---

## 🚀 Features

- Async scraping of movies by genre
- Fetch movie details via headless browser (Playwright)
- Pydantic validation for API responses
- Automatic Swagger docs (`/docs`)

---

## 🛠 Installation

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
playwright install

▶️ Run
uvicorn app.main:app --reload

API available at http://127.0.0.1:8000

Swagger docs at http://127.0.0.1:8000/docs
