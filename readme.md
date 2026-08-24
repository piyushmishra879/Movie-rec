# 🎬 Movie Recommendation System

A full-stack movie recommendation system combining **Machine Learning (TF-IDF & Cosine Similarity)**, **FastAPI**, **TMDB API**, and a modern **Streamlit** user interface.

---

## 🚀 Features
- **Smart Search & Autocomplete**: Search movies by title with instant TMDB suggestions.
- **Content-Based Recommendations**: Recommends similar movies using TF-IDF and Cosine Similarity on movie overviews and genres.
- **Genre-Based Discoveries**: Recommends popular movies matching the genre of the selected movie.
- **Home Feed**: Browse *Trending*, *Popular*, *Top Rated*, *Now Playing*, and *Upcoming* movies.
- **Responsive Movie Details**: Shows release date, genres, overview, high-resolution posters, and backdrops.

---

## 🛠 Tech Stack
- **Frontend**: Streamlit, Requests
- **Backend API**: FastAPI, Uvicorn, HTTPX, Pydantic
- **ML / Data**: Scikit-learn, Pandas, NumPy, Scipy
- **External Data**: TMDB (The Movie Database) API

---

## 📂 Project Structure
```text
├── app.py                   # Streamlit Frontend application
├── main.py                  # FastAPI Backend application
├── requirements.txt         # Frontend dependencies (for Streamlit Cloud)
├── requirements-backend.txt # Backend dependencies (for FastAPI / Render)
├── df.pkl                   # Processed movies DataFrame
├── indices.pkl              # Movie title to index mapping
├── tfidf.pkl                # Fitted TF-IDF vectorizer
├── tfidf_matrix.pkl         # TF-IDF feature matrix
└── readme.md                # Documentation
```

---

## ⚙️ Local Setup & How to Run

### 1. Prerequisites
- Python 3.10+
- TMDB API Key (Get a free key from [themoviedb.org](https://www.themoviedb.org/settings/api))

### 2. Run the Backend (FastAPI)
```bash
# 1. Create virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate

# 2. Install backend dependencies
pip install -r requirements-backend.txt

# 3. Create a .env file with your TMDB API key
echo TMDB_API_KEY=your_tmdb_api_key_here > .env

# 4. Start the FastAPI server
uvicorn main:app --reload --port 8000
```
FastAPI documentation will be available at `http://127.0.0.1:8000/docs`.

### 3. Run the Frontend (Streamlit)
```bash
# 1. Install frontend dependencies
pip install -r requirements.txt

# 2. (Optional) In app.py, point API_BASE to local backend:
# API_BASE = "http://127.0.0.1:8000"

# 3. Launch Streamlit
streamlit run app.py
```

---

## 🌐 Deployment Architecture

- **Frontend**: Hosted on [Streamlit Community Cloud](https://streamlit.io/cloud).
- **Backend**: Hosted on [Render](https://render.com).

> 💡 **Tip for Render Free Tier**: Render free instances go to sleep after 15 minutes of inactivity. To keep your backend awake 24/7 without cold-start delays, set up a free monitor on [cron-job.org](https://cron-job.org) or [UptimeRobot](https://uptimerobot.com) to ping `https://<your-render-app>.onrender.com/health` every 10 minutes.
