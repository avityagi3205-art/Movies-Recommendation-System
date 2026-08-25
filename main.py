import pickle
import streamlit as st
import requests
from sklearn.metrics.pairwise import cosine_similarity


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)


# ==================================================
# TMDB API
# ==================================================

# Recommended:
# Put your API key in .streamlit/secrets.toml
#
# TMDB_API_KEY = st.secrets["TMDB_API_KEY"]

TMDB_API_KEY = "use your api key"


# ==================================================
# FETCH POSTER
# ==================================================

@st.cache_data(ttl=3600)
def fetch_poster(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}"

    params = {
        "api_key": TMDB_API_KEY
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        # Request failed
        if response.status_code != 200:
            return None

        data = response.json()

        poster_path = data.get("poster_path")

        if poster_path:

            return (
                "https://image.tmdb.org/t/p/w500"
                + poster_path
            )

        return None

    except requests.exceptions.ConnectionError:

        return None

    except requests.exceptions.Timeout:

        return None

    except requests.exceptions.RequestException:

        return None

    except Exception:

        return None


# ==================================================
# LOAD MODEL
# ==================================================

@st.cache_resource
def load_data():

    with open("model/movies.pkl", "rb") as f:
        movies = pickle.load(f)

    with open("model/vectors.pkl", "rb") as f:
        vectors = pickle.load(f)

    with open("model/cv.pkl", "rb") as f:
        cv = pickle.load(f)

    return movies, vectors, cv


movies, vectors, cv = load_data()


# ==================================================
# RECOMMENDATION FUNCTION
# ==================================================

def recommend(movie):

    # Find selected movie
    movie_index = movies[
        movies["title"] == movie
    ].index[0]

    # Calculate similarity
    distances = cosine_similarity(
        vectors[movie_index],
        vectors
    ).flatten()

    # Get top 5 movies
    movie_indices = distances.argsort()[::-1][1:6]

    recommended_movie_names = []
    recommended_movie_posters = []

    for index in movie_indices:

        movie_id = movies.iloc[index]["movie_id"]

        movie_name = movies.iloc[index]["title"]

        poster = fetch_poster(movie_id)

        recommended_movie_names.append(
            movie_name
        )

        recommended_movie_posters.append(
            poster
        )

    return (
        recommended_movie_names,
        recommended_movie_posters
    )


# ==================================================
# UI
# ==================================================

st.title("🎬 Movie Recommender System")

st.write(
    "Select a movie and discover similar movies."
)


# Movie dropdown
movie_list = movies["title"].dropna().values


selected_movie = st.selectbox(
    "🎥 Select a movie",
    movie_list
)


# ==================================================
# RECOMMEND BUTTON
# ==================================================

if st.button(
    "🚀 Show Recommendation",
    use_container_width=True
):

    with st.spinner("Finding similar movies..."):

        recommended_movie_names, recommended_movie_posters = recommend(
            selected_movie
        )

    st.subheader(
        f"Movies similar to **{selected_movie}**"
    )

    cols = st.columns(5)

    for i in range(5):

        with cols[i]:

            st.markdown(
                f"### {recommended_movie_names[i]}"
            )

            poster = recommended_movie_posters[i]

            if poster:

                st.image(
                    poster,
                    use_container_width=True
                )

            else:

                st.info(
                    "Poster unavailable"
                )

















