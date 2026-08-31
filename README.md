# Movies-Recommendation-System
Content Based Recommendation Engine : Uses NLP techniques, Count Vectorizer and  Cosine similarity to find similar movies Based on plot and attributes.
Postal Retrieval : Fetches official movies poster graphics dynamically using the TMDB API.
Interactive Web UI : Simple and user interface built with Streamlit.
Precomputed Similarity Matrix : Efficient recommendation lookup using pre-trained files generated with pickle.

# Architecture & How It Works
Data Processing : Merges movie Metadata and credits datasets, drop null values, and parses JSON columns (genres, keywords, casts, crew).
Tags Creation : Concatenates plots overview, genres, keywords. top 3 actors, and director inti a unified text column.
Text Vectorization : Convert text tags into numerical features vectors (up to 5000 top features ) using Count Vectorization.
Similarity Matrix : Computes pairwise cosine similarity between features vectors to generates a similarity matrix.
Recommendation Generation : Return the top N most similar movies based on the calculated cosine distance ranking.

# Tech Stack
Language : Python.
Data Processing : Pandas, Numpy.
Machine Learning & NLP : SCIKIT Learn (count vectorizer, cosine similarity).
Web Framework : Streamlit.
API & Requests : TMDB APIs.
Model Serialization : Pickle/Joblib.

# Dataset Information
Dataset : TMDB 5000 Movies dataset (via kaggle)
Records : 5000 movies containing budget, genres, homepage, keywords, original language, overview, popularity, cast, crew, release date, and vote average.

# Future Improvement 
Implement Collaborative Filtering using matrix factorization or surprise library.
Create a hybrid system combining both content and user interaction data.
Deploy the web app using Docker /Render / Heroku.
