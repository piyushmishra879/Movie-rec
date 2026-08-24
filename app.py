import requests
import streamlit as st

# =============================
# CONFIG & PAGE SETUP
# =============================
API_BASE = "https://movie-rec-utmu.onrender.com"
TMDB_IMG = "https://image.tmdb.org/t/p/w500"

st.set_page_config(
    page_title="CineMatch AI — Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =============================
# MODERN CINEMA THEME (CSS)
# =============================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

.block-container {
    padding-top: 1.2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

/* Hero Banner */
.hero-card {
    background: linear-gradient(135deg, rgba(229, 9, 20, 0.12) 0%, rgba(20, 24, 38, 0.9) 100%);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 18px;
    padding: 1.8rem 2.2rem;
    margin-bottom: 1.5rem;
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.hero-title {
    font-size: 2.3rem;
    font-weight: 800;
    color: #FFFFFF;
    margin-bottom: 0.3rem;
    letter-spacing: -0.5px;
}

.hero-subtitle {
    color: #94A3B8;
    font-size: 1rem;
    margin-bottom: 0;
}

/* Movie Card */
.movie-card {
    background: #151922;
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 14px;
    padding: 10px;
    margin-bottom: 0.6rem;
    transition: transform 0.22s ease, border-color 0.22s ease, box-shadow 0.22s ease;
}

.movie-card:hover {
    transform: translateY(-4px);
    border-color: rgba(229, 9, 20, 0.4);
    box-shadow: 0 12px 28px rgba(0, 0, 0, 0.5);
}

.movie-card-title {
    font-size: 0.92rem;
    font-weight: 600;
    color: #F8FAFC;
    margin-top: 8px;
    margin-bottom: 4px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.movie-card-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.8rem;
    margin-bottom: 4px;
}

.rating-badge {
    color: #FBBF24;
    font-weight: 600;
    background: rgba(251, 191, 36, 0.12);
    padding: 2px 6px;
    border-radius: 6px;
    font-size: 0.78rem;
}

.year-badge {
    color: #94A3B8;
    background: rgba(255, 255, 255, 0.06);
    padding: 2px 6px;
    border-radius: 6px;
    font-size: 0.78rem;
}

/* Genre Pills */
.genre-pill {
    display: inline-block;
    background: rgba(229, 9, 20, 0.15);
    color: #FF5A5F;
    border: 1px solid rgba(229, 9, 20, 0.3);
    padding: 5px 14px;
    border-radius: 20px;
    font-size: 0.88rem;
    font-weight: 600;
    margin-right: 8px;
    margin-bottom: 8px;
}

/* Detail Card */
.detail-card {
    background: #151922;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 18px;
    padding: 24px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
}

.detail-title {
    font-size: 2.3rem;
    font-weight: 800;
    color: #FFFFFF;
    margin-bottom: 6px;
    letter-spacing: -0.5px;
}

.detail-meta {
    color: #94A3B8;
    font-size: 0.95rem;
    margin-bottom: 16px;
}

.detail-overview {
    color: #CBD5E1;
    font-size: 1.02rem;
    line-height: 1.65;
    margin-top: 14px;
}

/* Section Title */
.section-title {
    font-size: 1.4rem;
    font-weight: 700;
    color: #F8FAFC;
    margin-top: 1.8rem;
    margin-bottom: 0.3rem;
    display: flex;
    align-items: center;
    gap: 8px;
}

.section-desc {
    color: #94A3B8;
    font-size: 0.88rem;
    margin-bottom: 1.2rem;
}

/* Buttons */
div.stButton > button {
    width: 100%;
    border-radius: 10px;
    font-weight: 600;
    font-size: 0.88rem;
    transition: all 0.2s ease;
    background-color: #1E2433;
    border: 1px solid rgba(255, 255, 255, 0.12);
    color: #F1F5F9;
}

div.stButton > button:hover {
    border-color: #E50914;
    color: #FFFFFF;
    background-color: #E50914;
    box-shadow: 0 4px 14px rgba(229, 9, 20, 0.4);
}
</style>
""",
    unsafe_allow_html=True,
)

# =============================
# STATE & NAVIGATION
# =============================
if "view" not in st.session_state:
    st.session_state.view = "home"
if "selected_tmdb_id" not in st.session_state:
    st.session_state.selected_tmdb_id = None
if "active_category" not in st.session_state:
    st.session_state.active_category = "trending"

qp_view = st.query_params.get("view")
qp_id = st.query_params.get("id")
if qp_view in ("home", "details"):
    st.session_state.view = qp_view
if qp_id:
    try:
        st.session_state.selected_tmdb_id = int(qp_id)
        st.session_state.view = "details"
    except Exception:
        pass


def goto_home():
    st.session_state.view = "home"
    st.query_params["view"] = "home"
    if "id" in st.query_params:
        del st.query_params["id"]
    st.rerun()


def goto_details(tmdb_id: int):
    st.session_state.view = "details"
    st.session_state.selected_tmdb_id = int(tmdb_id)
    st.query_params["view"] = "details"
    st.query_params["id"] = str(int(tmdb_id))
    st.rerun()


# =============================
# API CLIENT
# =============================
@st.cache_data(ttl=60, show_spinner=False)
def api_get_json(path: str, params: dict | None = None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=60)
        if r.status_code >= 400:
            return None, f"HTTP {r.status_code}: {r.text[:300]}"
        return r.json(), None
    except requests.exceptions.Timeout:
        return None, "Backend server is waking up. Please wait a moment and try again."
    except requests.exceptions.ConnectionError:
        return None, "Unable to reach backend server. Please verify API is online."
    except Exception as e:
        return None, f"Request failed: {e}"


# =============================
# UI COMPONENTS
# =============================
def poster_grid(cards, cols=6, key_prefix="grid"):
    if not cards:
        st.info("No movies found.")
        return

    rows = (len(cards) + cols - 1) // cols
    idx = 0
    for r in range(rows):
        colset = st.columns(cols)
        for c in range(cols):
            if idx >= len(cards):
                break
            m = cards[idx]
            idx += 1

            tmdb_id = m.get("tmdb_id")
            title = m.get("title", "Untitled")
            poster = m.get("poster_url")
            year = (m.get("release_date") or "")[:4] or "—"
            rating = m.get("vote_average")
            rating_str = f"★ {round(float(rating), 1)}" if rating else "★ —"

            with colset[c]:
                poster_html = (
                    f'<img src="{poster}" style="width: 100%; border-radius: 10px; aspect-ratio: 2/3; object-fit: cover; box-shadow: 0 4px 12px rgba(0,0,0,0.3); margin-bottom: 6px;">'
                    if poster
                    else '<div style="width: 100%; aspect-ratio: 2/3; background: #232936; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: #64748B; font-size: 0.85rem; margin-bottom: 6px;">🎬 No Poster</div>'
                )

                st.markdown(
                    f"""
                    <div class="movie-card">
                        {poster_html}
                        <div class="movie-card-title" title="{title}">{title}</div>
                        <div class="movie-card-meta">
                            <span class="year-badge">{year}</span>
                            <span class="rating-badge">{rating_str}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                if st.button("Explore ➔", key=f"{key_prefix}_{r}_{c}_{idx}_{tmdb_id}"):
                    if tmdb_id:
                        goto_details(tmdb_id)


def to_cards_from_tfidf_items(tfidf_items):
    cards = []
    for x in tfidf_items or []:
        tmdb = x.get("tmdb") or {}
        if tmdb.get("tmdb_id"):
            cards.append(
                {
                    "tmdb_id": tmdb["tmdb_id"],
                    "title": tmdb.get("title") or x.get("title") or "Untitled",
                    "poster_url": tmdb.get("poster_url"),
                    "release_date": tmdb.get("release_date", ""),
                    "vote_average": tmdb.get("vote_average", None),
                }
            )
    return cards


def parse_tmdb_search_to_cards(data, keyword: str, limit: int = 24):
    keyword_l = keyword.strip().lower()

    if isinstance(data, dict) and "results" in data:
        raw = data.get("results") or []
        raw_items = []
        for m in raw:
            title = (m.get("title") or "").strip()
            tmdb_id = m.get("id")
            poster_path = m.get("poster_path")
            if not title or not tmdb_id:
                continue
            raw_items.append(
                {
                    "tmdb_id": int(tmdb_id),
                    "title": title,
                    "poster_url": f"{TMDB_IMG}{poster_path}" if poster_path else None,
                    "release_date": m.get("release_date", ""),
                    "vote_average": m.get("vote_average", None),
                }
            )
    elif isinstance(data, list):
        raw_items = []
        for m in data:
            tmdb_id = m.get("tmdb_id") or m.get("id")
            title = (m.get("title") or "").strip()
            poster_url = m.get("poster_url")
            if not title or not tmdb_id:
                continue
            raw_items.append(
                {
                    "tmdb_id": int(tmdb_id),
                    "title": title,
                    "poster_url": poster_url,
                    "release_date": m.get("release_date", ""),
                    "vote_average": m.get("vote_average", None),
                }
            )
    else:
        return [], []

    matched = [x for x in raw_items if keyword_l in x["title"].lower()]
    final_list = matched if matched else raw_items

    suggestions = []
    for x in final_list[:10]:
        year = (x.get("release_date") or "")[:4]
        rating = f"★ {round(x['vote_average'], 1)}" if x.get("vote_average") else ""
        label_parts = [x["title"]]
        if year:
            label_parts.append(f"({year})")
        if rating:
            label_parts.append(f"[{rating}]")
        suggestions.append((" ".join(label_parts), x["tmdb_id"]))

    cards = [
        {
            "tmdb_id": x["tmdb_id"],
            "title": x["title"],
            "poster_url": x["poster_url"],
            "release_date": x.get("release_date", ""),
            "vote_average": x.get("vote_average", None),
        }
        for x in final_list[:limit]
    ]
    return suggestions, cards


# =============================
# SIDEBAR
# =============================
with st.sidebar:
    st.markdown("### 🎬 CineMatch AI")
    if st.button("🏠 Home Feed", key="sb_home"):
        goto_home()

    st.markdown("---")
    st.markdown("⚙️ **Display Settings**")
    grid_cols = st.slider("Grid columns", min_value=3, max_value=8, value=6)
    st.caption("Customize how many movie posters to show per row.")


# ==========================================================
# VIEW: HOME
# ==========================================================
if st.session_state.view == "home":
    # Hero Section
    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-title">🎬 CineMatch AI</div>
            <div class="hero-subtitle">Smart Content-Based Movie Recommendations & Real-Time Discovery</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Search Bar
    typed = st.text_input(
        "Search Movies",
        placeholder="🔍 Type movie title (e.g. Inception, Dhoom, Avengers, Interstellar)...",
        label_visibility="collapsed",
    )

    # SEARCH MODE
    if typed.strip():
        if len(typed.strip()) < 2:
            st.caption("Type at least 2 characters to search.")
        else:
            with st.spinner("Searching movies..."):
                data, err = api_get_json("/tmdb/search", params={"query": typed.strip()})

            if err or data is None:
                st.error(f"Search failed: {err}")
            else:
                suggestions, cards = parse_tmdb_search_to_cards(
                    data, typed.strip(), limit=24
                )

                # Suggestions Dropdown
                if suggestions:
                    labels = ["-- Quick Pick from Suggestions --"] + [
                        s[0] for s in suggestions
                    ]
                    selected = st.selectbox(
                        "Suggestions", labels, index=0, label_visibility="collapsed"
                    )

                    if selected != "-- Quick Pick from Suggestions --":
                        label_to_id = {s[0]: s[1] for s in suggestions}
                        goto_details(label_to_id[selected])

                st.markdown(
                    f'<div class="section-title">🔍 Search Results for "{typed.strip()}" ({len(cards)})</div>',
                    unsafe_allow_html=True,
                )
                poster_grid(cards, cols=grid_cols, key_prefix="search_results")

        st.stop()

    # HOME DISCOVERY FEED
    st.markdown(
        '<div class="section-title">🔥 Discover Movies</div><div class="section-desc">Browse trending and top-rated movies across categories</div>',
        unsafe_allow_html=True,
    )

    category_map = {
        "🔥 Trending": "trending",
        "⭐ Popular": "popular",
        "🏆 Top Rated": "top_rated",
        "🍿 Now Playing": "now_playing",
        "🚀 Upcoming": "upcoming",
    }

    selected_tab = st.radio(
        "Feed Category",
        list(category_map.keys()),
        horizontal=True,
        label_visibility="collapsed",
    )
    current_category = category_map[selected_tab]

    with st.spinner("Loading movies..."):
        home_cards, err = api_get_json(
            "/home", params={"category": current_category, "limit": 24}
        )

    if err or not home_cards:
        st.error(f"Could not load movies: {err or 'Unknown error'}")
        if st.button("🔄 Retry Loading"):
            st.rerun()
    else:
        poster_grid(home_cards, cols=grid_cols, key_prefix=f"feed_{current_category}")


# ==========================================================
# VIEW: DETAILS
# ==========================================================
elif st.session_state.view == "details":
    tmdb_id = st.session_state.selected_tmdb_id
    if not tmdb_id:
        st.warning("No movie selected.")
        if st.button("← Back to Home"):
            goto_home()
        st.stop()

    # Back button bar
    top_col1, top_col2 = st.columns([1.5, 6])
    with top_col1:
        if st.button("← Back to Discovery", key="back_btn"):
            goto_home()

    # Load Details
    with st.spinner("Loading movie details..."):
        data, err = api_get_json(f"/movie/id/{tmdb_id}")

    if err or not data:
        st.error(f"Could not load details: {err or 'Unknown error'}")
        st.stop()

    # Backdrop banner if available
    backdrop = data.get("backdrop_url")
    if backdrop:
        st.markdown(
            f"""
            <div style="width: 100%; height: 260px; overflow: hidden; border-radius: 16px; margin: 12px 0 24px 0; position: relative; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
                <img src="{backdrop}" style="width: 100%; height: 100%; object-fit: cover; filter: brightness(0.6);">
                <div style="position: absolute; bottom: 18px; left: 24px; color: white;">
                    <div style="font-size: 2rem; font-weight: 800; text-shadow: 0 2px 10px rgba(0,0,0,0.9);">{data.get('title','')}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Details Layout: Poster + Metadata
    left, right = st.columns([1, 2.5], gap="large")

    with left:
        poster_url = data.get("poster_url")
        if poster_url:
            st.markdown(
                f'<img src="{poster_url}" style="width: 100%; border-radius: 14px; box-shadow: 0 10px 25px rgba(0,0,0,0.5);">',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div style="width: 100%; aspect-ratio: 2/3; background: #232936; border-radius: 14px; display: flex; align-items: center; justify-content: center; color: #64748B;">🎬 No Poster</div>',
                unsafe_allow_html=True,
            )

    with right:
        st.markdown('<div class="detail-card">', unsafe_allow_html=True)
        st.markdown(
            f'<div class="detail-title">{data.get("title","")}</div>',
            unsafe_allow_html=True,
        )

        release_date = data.get("release_date") or "Unknown"
        year = release_date[:4] if release_date != "Unknown" else "—"
        st.markdown(
            f'<div class="detail-meta">📅 Release: <b>{release_date}</b> ({year})</div>',
            unsafe_allow_html=True,
        )

        # Genres
        genres = data.get("genres", [])
        if genres:
            pills = "".join([f'<span class="genre-pill">{g["name"]}</span>' for g in genres])
            st.markdown(f'<div style="margin-bottom: 14px;">{pills}</div>', unsafe_allow_html=True)

        st.markdown("### 📖 Overview")
        st.markdown(
            f'<div class="detail-overview">{data.get("overview") or "No overview available for this movie."}</div>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    # =============================
    # RECOMMENDATIONS SECTION
    # =============================
    title = (data.get("title") or "").strip()
    if title:
        with st.spinner("Finding AI & genre recommendations..."):
            bundle, err2 = api_get_json(
                "/movie/search",
                params={"query": title, "tfidf_top_n": 12, "genre_limit": 12},
            )

        if not err2 and bundle:
            # 1. TF-IDF AI Matches
            tfidf_cards = to_cards_from_tfidf_items(bundle.get("tfidf_recommendations"))
            if tfidf_cards:
                st.markdown(
                    """
                    <div class="section-title">🤖 Similar Movies (Content AI Match)</div>
                    <div class="section-desc">Computed using TF-IDF & Cosine Similarity on plots, themes, and keywords</div>
                    """,
                    unsafe_allow_html=True,
                )
                poster_grid(tfidf_cards, cols=grid_cols, key_prefix="rec_tfidf")

            # 2. Genre Matches
            genre_cards = bundle.get("genre_recommendations", [])
            if genre_cards:
                st.markdown(
                    """
                    <div class="section-title">🎭 More Like This (Genre Discovery)</div>
                    <div class="section-desc">Popular titles matching the genres of this movie</div>
                    """,
                    unsafe_allow_html=True,
                )
                poster_grid(genre_cards, cols=grid_cols, key_prefix="rec_genre")

        else:
            # Fallback to genre only
            genre_only, err3 = api_get_json(
                "/recommend/genre", params={"tmdb_id": tmdb_id, "limit": 18}
            )
            if not err3 and genre_only:
                st.markdown(
                    """
                    <div class="section-title">🎭 Genre Recommendations</div>
                    <div class="section-desc">Popular titles matching this genre</div>
                    """,
                    unsafe_allow_html=True,
                )
                poster_grid(
                    genre_only, cols=grid_cols, key_prefix="rec_genre_fallback"
                )
            else:
                st.info("No recommendations available for this title.")
    else:
        st.warning("No title available to compute recommendations.")
