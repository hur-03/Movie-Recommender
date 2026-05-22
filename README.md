# Movie Recommendation System

## Project Overview

This project is a Movie Recommendation System built using Python, Flask, and Machine Learning techniques. The system recommends movies using:

- Content-Based Filtering
- User-Based Collaborative Filtering
- Hybrid Recommendation System

The application is deployed using Flask and containerised with Docker.

---

## Recommender Types

### 1. Content-Based Filtering

The content-based recommender suggests movies similar to a selected movie using:
- genres
- user tags
- movie metadata

Movie features are vectorised using CountVectorizer and compared using cosine similarity.

---

### 2. User-Based Collaborative Filtering

The collaborative filtering recommender suggests movies based on users with similar rating behaviour.

This is implemented using:
- user-movie rating matrix
- cosine similarity between users

---

### 3. Hybrid Recommender System

The hybrid recommender combines:
- content similarity scores
- collaborative filtering scores

Final recommendations are generated using weighted averaging of both methods.

---

## Technologies Used

- Python
- Flask
- Pandas
- NumPy
- Scikit-learn
- NLTK
- Docker
- HTML / Bootstrap

---

## Dataset Used

This project uses the MovieLens Latest Small Dataset.

Files used:
- movies.csv
- ratings.csv
- tags.csv
- links.csv

---

## How to Run
### 1. Clone the repository
### 2. Install dependecies: pip install -r requirements.txt
### 3. Run the notebook to generate files (movies.pkl, content_similarity.pkl, user_movie_matrix.pkl, user_similarity.pkl) locally
### 4. Run the Flask app: python app.py


<img width="1280" height="710" alt="image" src="https://github.com/user-attachments/assets/1d620656-1779-4c0f-8c8e-20515b495873" />
