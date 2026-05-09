# Movie Recommender System

Unlock Your Next Favorite Film! Our NLP-powered Movie Recommendation Web App delivers tailored suggestions based on cast, genres, and production companies. Explore a seamless Streamlit interface with personalized recommendations, movie details, and a comprehensive movie catalog.

## Video explaining the entire workflow of the project
https://drive.google.com/drive/folders/1WdkNkdDMB4G0c1nL6l0FuiSVmJESx8Tr?usp=drive_link

## Project Overview

Our Movie Recommender System, built using Python and Natural Language Processing (NLP), offers a user-friendly way to discover your next favorite movie. The system now features multiple recommendation engines:

- **Hybrid Recommendations**: Combines personal preferences with popular choices for the best of both worlds
- **Content-Based Filtering**: Suggests movies based on your favorite genres, directors, and movie styles
- **Collaborative Filtering**: Recommends movies enjoyed by users with similar taste

Key Features:
- Personalized movie recommendations based on your preferences and ratings
- Detailed movie information including cast, crew, and production details
- Similar movie suggestions based on various factors (tags, genres, production companies)
- Performance metrics to track recommendation accuracy
- User preference management and rating system
- Comprehensive movie catalog with easy navigation

## Sample Application Screenshots

### Recommendation Interface
![Home Screen](images/Screenshot%202025-03-08%20at%2019.32.16.png)
![Personalized Recommendations](images/Screenshot%202025-03-08%20at%2019.32.42.png)

**Recommendation Page:** Discover personalized movie suggestions based on your preferences and ratings.

### Movie Details
![Metrics Dashboard](images/Screenshot%202025-03-08%20at%2019.41.57.png)


**Description Page:** Explore essential movie details and information about the cast.

### Performance Dashboard
![Movie Information](images/Screenshot%202025-03-08%20at%2019.33.14.png)
![Cast Information](images/Screenshot%202025-03-08%20at%2019.33.34.png)

**Analytics Page:** Track recommendation performance and user engagement metrics.

## Quick Start with Docker (Recommended)

The fastest way to run the full stack — Streamlit app, MongoDB, and Mongo Express (database admin UI) — all wired together in containers.

**Prerequisites:** [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/vedvatsal3/MovieRecommenderSystem.git
   cd MovieRecommenderSystem
   ```

2. **Start everything:**
   ```bash
   docker compose up -d
   ```
   The first run pulls the prebuilt image from Docker Hub (`vved/movie-recommender`), MongoDB, and Mongo Express. Subsequent runs are instant.

3. **Open the app:**
   - Streamlit app → [http://localhost:8501](http://localhost:8501)
   - Mongo Express (database UI) → [http://localhost:8081](http://localhost:8081) (login: `admin` / `pass`)

4. **Stop the stack:**
   ```bash
   docker compose down        # stops containers, keeps your data
   docker compose down -v     # also removes data volumes (fresh slate)
   ```

User accounts, ratings, and preferences persist across restarts thanks to a named volume mounted at MongoDB's `/data/db`.

### Pull just the app image

The Streamlit image is published on Docker Hub:

```bash
docker pull vved/movie-recommender:latest
```

You'll still need MongoDB to run it usefully — the `docker-compose.yaml` in this repo handles that.

## Local Setup (Without Docker)

If you'd rather run the app directly on your machine — useful for development:

1. **Clone the Repository:** 
    ```bash
    git clone https://github.com/vedvatsal3/MovieRecommenderSystem.git
    ```

2. **Create a Virtual Environment:** 
   Set up a virtual environment to manage dependencies for your project:

   **For macOS/Linux:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   **For Windows:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application:**
   ```bash
   streamlit run main.py
   ```

If MongoDB isn't running locally on `mongodb://localhost:27017/`, the app falls back to file-based storage in `Files/`. To use MongoDB locally, either install it directly or run just the database container:

```bash
docker run -d -p 27017:27017 --name mongo \
  -e MONGO_INITDB_ROOT_USERNAME=vved \
  -e MONGO_INITDB_ROOT_PASSWORD=_____ \
  mongo
```

**Note:** First run takes a moment as it initializes recommendation models and downloads NLTK data.

## Features in Detail

### Recommendation Engines

1. **Hybrid Recommendations**
   - Combines collaborative and content-based filtering
   - Balances personal preferences with community favorites
   - Provides diverse and relevant suggestions

2. **Content-Based Filtering**
   - Analyzes movie attributes (genres, directors, cast)
   - Considers user-specified preferences
   - Matches movies based on similarity scores

3. **Collaborative Filtering**
   - Uses SVD (Singular Value Decomposition) for user-item interactions
   - Identifies similar user patterns
   - Suggests movies based on community ratings

### Performance Metrics

- Track recommendation accuracy
- Monitor user engagement
- Analyze rating patterns
- Measure system effectiveness

### User Features

- Personalized preference settings
- Movie rating system
- Watch history tracking
- Custom recommendation styles

Discover the joy of finding your next favorite movie with our Movie Recommender System!
