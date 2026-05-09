import streamlit as st
import pandas as pd
import json
import os
from pathlib import Path
from processing.database import Database

class UserAuth:
    def __init__(self):
        self.db = Database()

    def register_user(self, username, password):
        return self.db.register_user(username, password)

    def login_user(self, username, password):
        return self.db.login_user(username, password)

    def save_user_preferences(self, username, preferences):
        return self.db.save_user_preferences(username, preferences)

    def get_user_preferences(self, username):
        return self.db.get_user_preferences(username)

    def save_user_rating(self, username, movie_id, rating):
        old_rating = self.db.get_user_ratings(username).get(str(movie_id), 0)
        is_new_rating = old_rating == 0
        result = self.db.save_user_rating(username, movie_id, rating)

        try:
            st.session_state.refresh_recommendations = True
            for key in ('loaded_movies_count', 'cached_recommendations',
                        'cached_model_type', 'cached_timestamp'):
                if key == 'loaded_movies_count':
                    if key in st.session_state:
                        st.session_state.loaded_movies_count = 10
                elif key in st.session_state:
                    del st.session_state[key]

            rating_change = abs(rating - old_rating) if not is_new_rating else rating
            if rating_change > 0:
                from processing.metrics import RecommendationMetrics
                metrics = RecommendationMetrics()
                for model_type in ['content_based', 'collaborative', 'hybrid']:
                    metrics.record_rating_change(model_type, username, movie_id, old_rating, rating)
        except Exception as e:
            print(f"Error updating recommendation models: {e}")

        return result

    def get_user_ratings(self, username):
        return self.db.get_user_ratings(username)

    def needs_onboarding(self, username):
        user = self.db.get_user(username)
        if not user:
            return True
        return not user.get('completed_onboarding', False)

def render_auth_page():
    if 'user' not in st.session_state:
        st.session_state.user = None

    auth = UserAuth()

    if not st.session_state.user:
        tab1, tab2 = st.tabs(['Login', 'Register'])
        
        with tab1:
            st.subheader('Login')
            login_username = st.text_input('Username', key='login_username')
            login_password = st.text_input('Password', type='password', key='login_password')
            
            if st.button('Login'):
                success, message = auth.login_user(login_username, login_password)
                if success:
                    st.session_state.user = login_username
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)

        with tab2:
            st.subheader('Register')
            reg_username = st.text_input('Username', key='reg_username')
            reg_password = st.text_input('Password', type='password', key='reg_password')
            
            if st.button('Register'):
                success, message = auth.register_user(reg_username, reg_password)
                if success:
                    st.success(message)
                    st.session_state.user = reg_username
                    st.rerun()
                else:
                    st.error(message)

    return auth

def render_onboarding(suffix=''):
    # Generate a truly unique suffix for widget keys
    import time
    import random
    
    # Create a unique identifier based on timestamp and random number
    if '_onboarding_key' not in st.session_state:
        st.session_state['_onboarding_key'] = f"{suffix}_{time.time()}_{random.randint(1000, 9999)}"
    
    # Use the stored unique key
    unique_suffix = st.session_state['_onboarding_key']
    
    st.title('Welcome! Let\'s Get to Know Your Movie Preferences')
    
    # Collect user preferences through 5 questions
    preferences = {}
    
    # Question 1: Favorite Genres
    preferences['favorite_genres'] = st.multiselect(
        'What are your favorite movie genres? (Select up to 3)',
        ['Action', 'Adventure', 'Comedy', 'Drama', 'Horror', 'Romance', 'Sci-Fi', 'Thriller'],
        max_selections=3,
        key=f'onboarding_genres{unique_suffix}'
    )
    
    # Question 2: Movie Era Preference
    preferences['preferred_era'] = st.select_slider(
        'Which era of movies do you prefer?',
        options=['Classic (Pre-1970)', '1970s-1990s', '1990s-2010s', 'Modern (2010+)'],
        value='1990s-2010s',
        key=f'onboarding_era{unique_suffix}'
    )
    
    # Question 3: Preferred Directors
    preferences['preferred_directors'] = st.text_input(
        'Who are your favorite directors? (Separate names with commas)',
        placeholder='e.g. Christopher Nolan, Steven Spielberg, Quentin Tarantino',
        key=f'onboarding_directors{unique_suffix}'
    )
    
    # Question 4: Mood Preference
    preferences['preferred_mood'] = st.select_slider(
        'What type of movie mood do you typically enjoy?',
        options=['Light & Funny', 'Thought-provoking', 'Intense & Thrilling', 'Emotional & Dramatic', 'Escapist & Fantasy'],
        value='Thought-provoking',
        key=f'onboarding_mood{unique_suffix}'
    )
    
    # Question 5: Content Language
    preferences['preferred_languages'] = st.multiselect(
        'What languages do you prefer for movies? (Select all that apply)',
        ['English', 'Spanish', 'French', 'Hindi', 'Japanese', 'Korean', 'Chinese'],
        default=['English'],
        key=f'onboarding_languages{unique_suffix}'
    )
    
    return preferences