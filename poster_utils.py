"""
poster_utils.py
----------------
Handles fetching movie poster images from TMDB, with a Wikipedia-based
fallback for titles TMDB can't resolve, and a final static placeholder
if both sources fail.
"""

import base64
import os
import re
import requests
import streamlit as st

TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"
WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"

# Local placeholder shipped with the repo — used only if every fetch attempt fails.
_PLACEHOLDER_FILE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "assets", "poster_placeholder.png"
)


@st.cache_resource
def _load_placeholder_data_uri() -> str:
    """
    Reads the local placeholder image from disk and encodes it as a base64
    data URI, so it can be embedded directly in HTML <img> tags. Plain file
    paths like 'assets/poster_placeholder.png' don't work as <img src=...>
    because the browser tries to fetch them as a URL, not a local file —
    Streamlit doesn't serve arbitrary project folders as static assets.
    """
    try:
        with open(_PLACEHOLDER_FILE_PATH, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
        return f"data:image/png;base64,{encoded}"
    except FileNotFoundError:
        # If even the placeholder is missing, fall back to a tiny inline
        # gray rectangle so the layout doesn't break.
        return (
            "data:image/svg+xml;base64,"
            + base64.b64encode(
                b'<svg xmlns="http://www.w3.org/2000/svg" width="500" height="750">'
                b'<rect width="100%" height="100%" fill="#1e1e24"/></svg>'
            ).decode("utf-8")
        )


DEFAULT_POSTER_PATH = _load_placeholder_data_uri()

REQUEST_HEADERS = {"User-Agent": "Mozilla/5.0 (Cinematique Movie Recommender)"}
REQUEST_TIMEOUT = 6


def _get_api_key() -> str:
    """
    Reads the TMDB API key from Streamlit secrets.
    Configure this in .streamlit/secrets.toml (locally) or in the
    Streamlit Cloud app settings (in production) — never hardcode it.
    """
    try:
        return st.secrets["TMDB_API_KEY"]
    except (KeyError, FileNotFoundError):
        st.error(
            "⚠️ TMDB API key not found. Add TMDB_API_KEY to your "
            "`.streamlit/secrets.toml` file (see secrets.toml.example)."
        )
        return ""


def clean_movie_title(title: str) -> str:
    """Strips trailing year info like 'Avatar (2009)' -> 'Avatar'."""
    cleaned = re.sub(r"\s*\(\d{4}\)", "", str(title))
    return cleaned.strip()


def _fetch_from_tmdb_by_id(movie_id: int, api_key: str) -> dict | None:
    """Looks up a movie directly by TMDB ID. Returns the full movie dict or None."""
    try:
        url = f"{TMDB_BASE_URL}/movie/{movie_id}"
        response = requests.get(
            url,
            params={"api_key": api_key, "language": "en-US"},
            headers=REQUEST_HEADERS,
            timeout=REQUEST_TIMEOUT,
        )
        if response.status_code == 200:
            return response.json()
        print(f"[TMDB by ID] movie_id={movie_id} -> HTTP {response.status_code}: {response.text[:200]}")
    except requests.RequestException as e:
        print(f"[TMDB by ID] movie_id={movie_id} -> {type(e).__name__}: {e}")
    return None


def _fetch_from_tmdb_by_search(title: str, api_key: str) -> dict | None:
    """
    Searches TMDB by title and returns the most popular matching result
    that actually has a poster (avoids obscure/foreign same-title mismatches).
    """
    try:
        url = f"{TMDB_BASE_URL}/search/movie"
        response = requests.get(
            url,
            params={"api_key": api_key, "query": title},
            headers=REQUEST_HEADERS,
            timeout=REQUEST_TIMEOUT,
        )
        if response.status_code == 200:
            results = response.json().get("results", [])
            results_with_posters = [r for r in results if r.get("poster_path")]
            if results_with_posters:
                return max(results_with_posters, key=lambda r: r.get("popularity", 0))
            print(f"[TMDB search] '{title}' -> no results with posters ({len(results)} raw results)")
        else:
            print(f"[TMDB search] '{title}' -> HTTP {response.status_code}: {response.text[:200]}")
    except requests.RequestException as e:
        print(f"[TMDB search] '{title}' -> {type(e).__name__}: {e}")
    return None


def _fetch_from_wikipedia(title: str) -> str | None:
    """
    Two-step Wikipedia fallback: search for '{title} film', then fetch that
    page's original image. Used only when TMDB has no match at all.
    """
    cleaned = clean_movie_title(title)
    try:
        search_response = requests.get(
            WIKIPEDIA_API_URL,
            params={
                "action": "query",
                "list": "search",
                "srsearch": f"{cleaned} film",
                "format": "json",
            },
            timeout=REQUEST_TIMEOUT,
        )
        if search_response.status_code != 200:
            return None

        search_results = search_response.json().get("query", {}).get("search", [])
        if not search_results:
            return None

        best_page_title = search_results[0]["title"]

        image_response = requests.get(
            WIKIPEDIA_API_URL,
            params={
                "action": "query",
                "prop": "pageimages",
                "format": "json",
                "piprop": "original",
                "titles": best_page_title,
                "redirects": 1,
            },
            timeout=REQUEST_TIMEOUT,
        )
        if image_response.status_code != 200:
            return None

        pages = image_response.json().get("query", {}).get("pages", {})
        for page_info in pages.values():
            if "original" in page_info:
                return page_info["original"]["source"]
    except requests.RequestException:
        pass
    return None


@st.cache_data(show_spinner=False, ttl=60 * 60 * 24)  # cache each poster for 24h
def fetch_poster_data(movie_title: str, movie_id: int | None = None) -> dict:
    """
    Main entry point. Returns a dict with poster_url, rating, release_year,
    and overview — so the UI can show more than just an image (see app.py).
    Falls back gracefully: TMDB by ID -> TMDB by search -> Wikipedia -> placeholder.
    """
    print(f"[fetch_poster_data] Fetching '{movie_title}' (movie_id={movie_id})")
    api_key = _get_api_key()
    print(f"[fetch_poster_data] API key loaded: {'yes' if api_key else 'NO - MISSING'}")
    cleaned_title = clean_movie_title(movie_title)

    movie_data = None
    if api_key:
        if movie_id is not None:
            try:
                movie_data = _fetch_from_tmdb_by_id(int(float(movie_id)), api_key)
            except (ValueError, TypeError):
                movie_data = None
        if movie_data is None:
            movie_data = _fetch_from_tmdb_by_search(cleaned_title, api_key)

    if movie_data and movie_data.get("poster_path"):
        return {
            "poster_url": f"{TMDB_IMAGE_BASE}{movie_data['poster_path']}",
            "rating": movie_data.get("vote_average"),
            "release_year": (movie_data.get("release_date") or "")[:4],
            "overview": movie_data.get("overview", ""),
            "source": "tmdb",
        }

    wiki_poster = _fetch_from_wikipedia(movie_title)
    if wiki_poster:
        return {
            "poster_url": wiki_poster,
            "rating": None,
            "release_year": None,
            "overview": "",
            "source": "wikipedia",
        }

    return {
        "poster_url": None,  # app.py renders the local placeholder for this
        "rating": None,
        "release_year": None,
        "overview": "",
        "source": "placeholder",
    }
