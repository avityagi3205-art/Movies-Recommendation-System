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

TMDB_API_KEY = "8bf153d798418499c6041b558a728ed6"


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













# import pickle
# import streamlit as st
# import requests

# def fetch_poster(movie_id):
#     url = "https://api.themoviedb.org/3/movie/{}?api_key=".format(movie_id)
#     data = requests.get(url)
#     data = data.json()
#     poster_path = data['poster_path']
#     full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
#     return full_path

# def recommend(movie):
#     index = movies[movies['title'] == movie].index[0]
#     distances = sorted(list(enumerate([index])), reverse=True, key=lambda x: x[1])
#     recommended_movie_names = []
#     recommended_movie_posters = []
#     for i in distances[1:6]:
#         # fetch the movie poster
#         movie_id = movies.iloc[i[0]].movie_id
#         recommended_movie_posters.append(fetch_poster(movie_id))
#         recommended_movie_names.append(movies.iloc[i[0]].title)

#     return recommended_movie_names,recommended_movie_posters


# st.header('Movie Recommender System')
# movies = pickle.load(open('model/movies.pkl','rb'))
# vectors = pickle.load(open('model/vectors.pkl','rb'))
# cv = pickle.load(open('model/cv.pkl','rb'))


# movie_list = movies['title'].values
# selected_movie = st.selectbox(
#     "Type or select a movie from the dropdown",
#     movie_list
# )

# if st.button('Show Recommendation'):
#     recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
#     col1, col2, col3, col4, col5 = st.beta_columns(5)
#     with col1:
#         st.text(recommended_movie_names[0])
#         st.image(recommended_movie_posters[0])
#     with col2:
#         st.text(recommended_movie_names[1])
#         st.image(recommended_movie_posters[1])

#     with col3:
#         st.text(recommended_movie_names[2])
#         st.image(recommended_movie_posters[2])
#     with col4:
#         st.text(recommended_movie_names[3])
#         st.image(recommended_movie_posters[3])
#     with col5:
#         st.text(recommended_movie_names[4])
#         st.image(recommended_movie_posters[4])




