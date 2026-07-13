# 🎬 Cinematique

A content-based movie recommendation web app that suggests similar movies using cosine similarity over vectorized movie metadata (genres, keywords, cast, crew, and plot overview).

**🔗 Live demo:** [cinematique-movie-recommender.streamlit.app](https://cinematique-movie-recommender.streamlit.app/)

![Cinematique screenshot](assets/screenshot.png)

---

## How it works

Cinematique uses **content-based filtering** — it recommends movies that are *structurally similar* to the one you pick, rather than relying on other users' ratings (collaborative filtering).

1. **Feature engineering** — each movie's genres, keywords, top cast, director, and overview are combined into a single "tags" string.
2. **Vectorization** — a `CountVectorizer` (bag-of-words) converts every movie's tags into a numeric vector.
3. **Similarity matrix** — cosine similarity is computed between every pair of movie vectors, producing a precomputed similarity matrix.
4. **Recommendation** — for a selected movie, the 5 movies with the highest cosine similarity score are returned.

At request time, the app also calls [The Movie Database (TMDB) API](https://www.themoviedb.org/documentation/api) to fetch each recommended movie's poster, release year, and rating, with a Wikipedia-based fallback for titles TMDB can't resolve.

---

## Tech stack

| Layer | Technology |
|---|---|
| Frontend / App framework | [Streamlit](https://streamlit.io/) |
| ML / Similarity engine | scikit-learn (`CountVectorizer`, cosine similarity), pandas |
| Poster & metadata source | [TMDB API](https://www.themoviedb.org/documentation/api) with Wikipedia fallback |
| Deployment | Streamlit Community Cloud |
| Dataset | [TMDB 5000 Movies Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) (Kaggle) |

---

## Features

- 🔍 Search and select from thousands of movies
- 🎯 Get 5 content-based recommendations per query, ranked by similarity score
- 🖼️ Live poster, release year, and rating for each recommendation, pulled from TMDB
- 🌐 Graceful fallback chain (TMDB → Wikipedia → local placeholder) so the UI never breaks if a poster can't be found
- ⚡ Cached lookups (24h) to minimize redundant API calls and keep the app fast

---

## Project structure

```
cinematique/
├── app.py              # Streamlit UI and page layout
├── recommender.py       # Recommendation engine (loads model, computes similarity)
├── poster_utils.py      # TMDB + Wikipedia poster/metadata fetching
├── styles.py             # Custom CSS
├── requirements.txt
├── assets/
│   └── poster_placeholder.png
├── data/
│   ├── movies.pkl        # Precomputed movie metadata
│   └── similarity.pkl    # Precomputed cosine similarity matrix
└── .streamlit/
    └── secrets.toml.example
```

---

## Running locally

**1. Clone the repository**
```bash
git clone https://github.com/Arushi1806/cinematique-movie-recommender.git
cd cinematique-movie-recommender
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Add your TMDB API key**

Copy the example secrets file and add your own [TMDB API key](https://www.themoviedb.org/settings/api) (free):
```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```
Then edit `.streamlit/secrets.toml`:
```toml
TMDB_API_KEY = "your_api_key_here"
```

**4. Run the app**
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## Model training

The recommendation model (`movies.pkl` and `similarity.pkl`) was trained offline on the TMDB 5000 Movies dataset:

- Merged movie and credits metadata (genres, keywords, cast, crew, overview)
- Cleaned and combined these fields into a single tags column per movie
- Vectorized tags using `CountVectorizer` (bag-of-words, top 5000 features, English stop words removed)
- Computed a full pairwise cosine similarity matrix across all movies
- Serialized both the movie metadata DataFrame and similarity matrix with `pickle` for fast loading at runtime

---

## Roadmap

- [ ] "Why this was recommended" — surface shared genres/keywords between the query movie and each result
- [ ] Movie detail view (overview, cast) on click
- [ ] Genre-based filtering before recommending
- [ ] Trending/popular row on initial load

---

## Author

Built by **Arushi** — [GitHub](https://github.com/Arushi1806)

---

## Acknowledgements

- Movie data from [TMDB](https://www.themoviedb.org/) — this product uses the TMDB API but is not endorsed or certified by TMDB.
- Dataset: [TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) on Kaggle.
