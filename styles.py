"""
styles.py
---------
Holds the app's custom CSS as a single string, kept out of app.py to keep
the main file focused on logic and layout rather than styling.
"""

CUSTOM_CSS = """
<style>
    :root {
        --netflix-red: #E50914;
        --netflix-red-hover: #F40612;
        --bg-dark: #0f0f12;
        --card-bg: #1e1e24;
        --card-border: #2d2d34;
        --text-muted: #9ca3af;
    }

    .stApp {
        background-color: var(--bg-dark);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    h1, h2, h3, h4, h5, h6, p, span, label {
        font-family: 'Inter', sans-serif !important;
    }

    .main-title {
        background: linear-gradient(135deg, #FFF 0%, #A5A5AB 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        letter-spacing: -1.5px;
        margin-bottom: 5px !important;
        text-align: left;
    }

    .brand-accent {
        color: var(--netflix-red);
        font-weight: 900;
    }

    .subtitle-text {
        color: var(--text-muted);
        font-size: 1.15rem;
        margin-bottom: 2rem !important;
        font-weight: 400;
        line-height: 1.6;
    }

    div[data-baseweb="select"] {
        background-color: #1a1a1f !important;
        border-radius: 10px !important;
        border: 1px solid #33333b !important;
    }
    div[data-baseweb="select"] * {
        color: #ffffff !important;
    }
    label[data-testid="stWidgetLabel"] {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        margin-bottom: 0.5rem !important;
    }

    .recommendation-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 20px;
        margin-top: 1.5rem;
    }

    @media (max-width: 1024px) {
        .recommendation-grid { grid-template-columns: repeat(3, 1fr); }
    }

    @media (max-width: 640px) {
        .recommendation-grid { grid-template-columns: 1fr; }
    }

    .movie-card {
        background: linear-gradient(145deg, #18181c 0%, #111114 100%);
        border: 1px solid var(--card-border);
        border-radius: 16px;
        padding: 14px;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;
        min-height: 420px;
        height: 100%;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        position: relative;
    }

    .movie-card:hover {
        transform: translateY(-8px);
        border-color: var(--netflix-red);
        box-shadow: 0 12px 30px rgba(229, 9, 20, 0.25);
    }

    .poster-container {
        width: 100%;
        height: 250px;
        overflow: hidden;
        border-radius: 12px;
        margin-bottom: 12px;
        background: linear-gradient(135deg, #1f1114 0%, #0c0c0e 100%);
        border: 1px solid rgba(255, 255, 255, 0.05);
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
    }

    .poster-fallback-watermark {
        position: absolute;
        font-size: 3.5rem;
        color: var(--netflix-red);
        opacity: 0.12;
        z-index: 1;
        user-select: none;
    }

    .movie-poster {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.5s ease;
        position: relative;
        z-index: 2;
    }

    .movie-card:hover .movie-poster {
        transform: scale(1.08);
    }

    .movie-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, var(--netflix-red), #ff4d4d);
        opacity: 0.8;
    }

    .card-title {
        color: #FFFFFF !important;
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        margin: 8px 0 0 0 !important;
        line-height: 1.4 !important;
        height: 48px;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
    }

    .card-meta {
        color: var(--text-muted);
        font-size: 0.8rem;
        margin-top: 4px;
    }

    .card-badge {
        font-size: 0.72rem;
        text-transform: uppercase;
        color: var(--netflix-red);
        font-weight: 800;
        letter-spacing: 1px;
        margin-top: auto;
        padding-top: 8px;
    }

    .stButton>button {
        background: linear-gradient(135deg, var(--netflix-red) 0%, #b20710 100%) !important;
        color: #ffffff !important;
        width: 100% !important;
        height: 52px !important;
        border-radius: 12px !important;
        border: none !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(229, 9, 20, 0.4) !important;
    }

    .stButton>button:hover {
        background: linear-gradient(135deg, var(--netflix-red-hover) 0%, var(--netflix-red) 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(229, 9, 20, 0.6) !important;
    }

    .stButton>button:active {
        transform: translateY(0) !important;
    }

    section[data-testid="stSidebar"] {
        background: #09090b !important;
        border-right: 1px solid #1a1a1f !important;
    }

    section[data-testid="stSidebar"] hr {
        border-color: #1a1a1f !important;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
"""
