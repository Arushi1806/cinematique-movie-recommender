"""
app.py
------
Cinematique: a content-based movie recommendation web app.
This file handles page layout and user interaction only — the
recommendation logic lives in recommender.py, and poster/detail
fetching lives in poster_utils.py.
"""

import streamlit as st

from recommender import load_data, get_recommendations
from poster_utils import fetch_poster_data, DEFAULT_POSTER_PATH
from styles import CUSTOM_CSS

# -----------------------------------------------------------------------------
# Page configuration (must be first Streamlit call)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Cinematique - Premium Movie Recommendations",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Data loading
# -----------------------------------------------------------------------------
movies, similarity = load_data()

# -----------------------------------------------------------------------------
# Sidebar
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("<div style='padding-top: 20px;'></div>", unsafe_allow_html=True)
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg",
        use_container_width=True,
    )
    st.markdown("<div style='margin-top:25px;'></div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div style='background: rgba(255,255,255,0.03); padding: 15px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);'>
            <p style='margin: 0; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; color: #85858b; font-weight: bold;'>Framework</p>
            <p style='margin: 5px 0 0 0; font-size: 1rem; color: #ffffff; font-weight: bold;'>Content-Based Engine</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown("<h4 style='color: #ffffff; font-weight: bold; margin-bottom: 15px;'>Engine Architecture</h4>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style='display: flex; flex-direction: column; gap: 8px;'>
            <span style='color: #a5a5ab; font-size: 0.95rem;'>⚡ &nbsp; Cosine Similarity Metric</span>
            <span style='color: #a5a5ab; font-size: 0.95rem;'>🧬 &nbsp; Bag-of-Words Vectorizer</span>
            <span style='color: #a5a5ab; font-size: 0.95rem;'>🤖 &nbsp; High-performance ML Engine</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown(
        """
        <div style='color: #85858b; font-size: 0.85rem;'>
            Developed with ❤️ by <span style='color:#E50914; font-weight:bold;'>Arushi</span><br>
            Version 3.0 (Refactored Edition)
        </div>
        """,
        unsafe_allow_html=True,
    )

# -----------------------------------------------------------------------------
# Hero header
# -----------------------------------------------------------------------------
col_main_left, col_main_right = st.columns([7, 5])

with col_main_left:
    st.markdown('<h1 class="main-title">CINEMATIQUE</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="subtitle-text">Next-gen hyper-personalized cinema indexing model. '
        "Analyze, filter, and recommend contextual blockbusters matching your taste signature instantly.</p>",
        unsafe_allow_html=True,
    )

with col_main_right:
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, rgba(229, 9, 20, 0.15) 0%, rgba(15, 15, 18, 0.9) 100%),
                        url('https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=800');
            background-size: cover;
            background-position: center;
            border-radius: 16px;
            height: 130px;
            border: 1px solid rgba(229, 9, 20, 0.3);
            display: flex;
            align-items: center;
            padding-left: 25px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
        ">
            <div>
                <span style="background-color: #E50914; color: white; padding: 4px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 800; letter-spacing: 1px;">MACHINE LEARNING ACTIVE</span>
                <h3 style="color: white; margin: 5px 0 0 0; font-size: 1.3rem; font-weight: bold;">Cos-Sim Vector Engine v2</h3>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Movie selection + recommendation trigger
# -----------------------------------------------------------------------------
if movies.empty:
    st.warning("⚠️ No movie data loaded. Make sure `data/movies.pkl` and `data/similarity.pkl` are present.")
else:
    movie_list = movies["title"].values

    select_col, btn_col = st.columns([8, 4])

    with select_col:
        selected_movie = st.selectbox(
            "🎥 TYPE OR CHOOSE YOUR BASE MOVIE",
            movie_list,
            index=0,
            help="Select a reference movie to find its closest structural matches.",
        )

    with btn_col:
        st.markdown("<div style='padding-top: 31px;'></div>", unsafe_allow_html=True)
        trigger_recommendation = st.button("🍿 RUN RECOMMENDATION ENGINE")

    st.markdown("<div style='margin-bottom: 2.5rem;'></div>", unsafe_allow_html=True)

    if trigger_recommendation:
        with st.spinner("⚡ Mapping vectors and fetching movie data..."):
            recommendations = get_recommendations(selected_movie, movies, similarity)

            # Attach poster + detail data to each recommendation
            for rec in recommendations:
                rec.update(fetch_poster_data(rec["title"], rec["movie_id"]))

        if not recommendations:
            st.error("Couldn't generate recommendations for that title. Try another movie.")
        else:
            st.markdown(
                """
                <h3 style='color: #ffffff; font-weight: 800; letter-spacing: -0.5px; margin-bottom: 20px; display: flex; align-items: center;'>
                    <span style='color: #E50914; margin-right: 10px;'>✦</span> 5 Matching Targets Identified For You
                </h3>
                """,
                unsafe_allow_html=True,
            )

            badges = ["Match #1", "Match #2", "Match #3", "Match #4", "Match #5"]

            grid_html = '<div class="recommendation-grid">'
            for idx, rec in enumerate(recommendations):
                poster_url = rec.get("poster_url") or DEFAULT_POSTER_PATH
                meta_parts = []
                if rec.get("release_year"):
                    meta_parts.append(rec["release_year"])
                if rec.get("rating"):
                    meta_parts.append(f"⭐ {rec['rating']:.1f}")
                meta_line = " • ".join(meta_parts)

                grid_html += f"""
                <div class="movie-card">
                    <div class="poster-container">
                        <div class="poster-fallback-watermark">🎬</div>
                        <img class="movie-poster" src="{poster_url}" alt="{rec['title']}" onerror="this.src='{DEFAULT_POSTER_PATH}';">
                    </div>
                    <div class="card-title">{rec['title']}</div>
                    <div class="card-meta">{meta_line}</div>
                    <div class="card-badge">{badges[idx]}</div>
                </div>
                """
            grid_html += "</div>"

            clean_grid_html = "\n".join(line.strip() for line in grid_html.split("\n"))
            st.markdown(clean_grid_html, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Footer
# -----------------------------------------------------------------------------
st.markdown("<div style='margin-top: 5rem;'></div>", unsafe_allow_html=True)
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; padding: 20px 0; color: #52525b; font-size: 0.9rem;">
        🎬 Cinematique Recommendation Platform • Engineered by <b>Arushi</b><br>
        <span style="font-size: 0.8rem; color: #3f3f46; margin-top: 5px; display: block;">Content-Based Filtering with Cosine Similarity & Vectorized Feature Matrices</span>
    </div>
    """,
    unsafe_allow_html=True,
)
