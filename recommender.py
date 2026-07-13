"""
recommender.py
---------------
Loads the trained content-based recommendation model (movie metadata +
precomputed cosine similarity matrix) and exposes a simple function to
get the top-N most similar movies for a given title.
"""

import pickle
import pandas as pd
import streamlit as st

MOVIES_PATH = "data/movies.pkl"
SIMILARITY_PATH = "data/similarity.pkl"
TOP_N_RECOMMENDATIONS = 5


@st.cache_data
def load_data():
    """
    Loads the movie metadata DataFrame and the precomputed similarity matrix.
    Cached so this only runs once per app session, not on every interaction.
    """
    try:
        movies_df = pickle.load(open(MOVIES_PATH, "rb"))
        similarity_matrix = pickle.load(open(SIMILARITY_PATH, "rb"))
        return movies_df, similarity_matrix
    except FileNotFoundError:
        st.error(
            f"⚠️ Could not find `{MOVIES_PATH}` or `{SIMILARITY_PATH}`. "
            "Make sure both files are present in the `data/` folder."
        )
        return pd.DataFrame(columns=["title"]), []


def get_recommendations(movie_title: str, movies: pd.DataFrame, similarity) -> list[dict]:
    """
    Returns the top N most similar movies to `movie_title`, based on the
    precomputed cosine similarity matrix.

    Each item in the returned list is a dict: {"title": ..., "movie_id": ...}
    so the caller (app.py) can fetch posters/details separately.
    """
    matches = movies[movies["title"] == movie_title]
    if matches.empty:
        return []

    movie_index = matches.index[0]
    distances = similarity[movie_index]

    # Sort by similarity score, skip index 0 (the movie itself)
    ranked = sorted(
        enumerate(distances), key=lambda x: x[1], reverse=True
    )[1 : TOP_N_RECOMMENDATIONS + 1]

    id_column = "id" if "id" in movies.columns else (
        "movie_id" if "movie_id" in movies.columns else None
    )

    recommendations = []
    for idx, score in ranked:
        row = movies.iloc[idx]
        recommendations.append(
            {
                "title": row["title"],
                "movie_id": row[id_column] if id_column else None,
                "similarity_score": round(float(score), 3),
            }
        )
    return recommendations
