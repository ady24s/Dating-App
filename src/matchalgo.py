import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Scoring functions
def assign_age_score(profile_age, desired_age):
    return abs(profile_age - desired_age)

def assign_status_score(profile_status, desired_status):
    return 0 if profile_status == desired_status else 1

def assign_gender_score(profile_gender, desired_gender):
    return 0 if profile_gender.lower() == desired_gender.lower() else 1

def assign_orientation_score(profile_orientation, desired_orientation):
    return 0 if profile_orientation == desired_orientation else 1

def assign_relationship_score(profile_relationship, desired_relationship):
    return 0 if profile_relationship.lower() == desired_relationship.lower() else 1

# Retrieve user index given a user ID
def get_user_index(df, user_id):
    index_list = df.index[df['user_id'] == user_id].tolist()
    return index_list[0] if index_list else None

# Get similarity scores for a specific user index
def get_user_similarity_scores(user_index, similarity_matrix):
    return similarity_matrix[user_index]

def get_user_id_from_credentials(df, email, password):
    # Search for matching email and password
    user_row = df[(df['email'] == email) & (df['password'] == password)]

    # Check if any rows were returned
    if not user_row.empty:
        return user_row['user_id'].values[0]
    else:
        raise ValueError("Invalid email or password")

# Combine scores into one metric
def combine_scores(age_scores, status_scores, gender_scores,
                   orientation_scores, relationship_scores, cosine_sim_scores):
    combined_scores = (
        age_scores +
        status_scores +
        gender_scores +
        orientation_scores +
        relationship_scores +
        cosine_sim_scores
    )
    return combined_scores

# Calculate match percentage
def calculate_match_percentage(combined_scores):
    max_score = combined_scores.max()
    match_percentage = ((max_score - combined_scores) / max_score * 100).round(2)
    return match_percentage

# Rank profiles based on match percentages
def rank_profiles(df, match_percentages):
    # Add the match percentage to the DataFrame
    df['match_percentage'] = match_percentages

    # Sort by match percentage and select the top 10
    ranked_profiles = df.sort_values(by='match_percentage', ascending=False).head(10)

    # Include 'name' and 'user_id' in the final selection, along with other relevant fields
    return ranked_profiles[['user_id', 'name', 'age', 'status', 'gender', 'orientation', 'relationship_type', 'essay0', 'match_percentage']]

# Get recommendations with the appropriate user index
def get_recomms(df, user_index, desired_age, desired_status, desired_gender, desired_orientation, desired_relationship, cosine_sim):
    age_scores = df['age'].apply(lambda x: assign_age_score(x, desired_age))
    status_scores = df['status'].apply(lambda x: assign_status_score(x, desired_status))
    gender_scores = df['gender'].apply(lambda x: assign_gender_score(x, desired_gender))
    orientation_scores = df['orientation'].apply(lambda x: assign_orientation_score(x, desired_orientation))
    relationship_scores = df['relationship_type'].apply(lambda x: assign_relationship_score(x, desired_relationship))

    # Retrieve the similarity scores for the specific user
    cosine_sim_scores = get_user_similarity_scores(user_index, cosine_sim)

    combined_scores = combine_scores(age_scores, status_scores, gender_scores, orientation_scores, relationship_scores, cosine_sim_scores)
    match_percentages = calculate_match_percentage(combined_scores)
    ranked_profiles = rank_profiles(df, match_percentages)
    return ranked_profiles

# Wrapper function to find recommendations for a specific user
def get_combined_recommendations(df_path, user_id, desired_age, desired_status, desired_gender, desired_orientation, desired_relationship):
    df_dataset = pd.read_csv(df_path, nrows=100)
    df_dataset['essay0'] = df_dataset['essay0'].fillna(" ")

    # Retrieve the user's index
    user_index = get_user_index(df_dataset, user_id)
    if user_index is None:
        raise ValueError(f"User with ID {user_id} not found.")

    # Create TF-IDF matrix and cosine similarity matrix
    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(df_dataset['essay0'])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    # Pass the specific user index to get recommendations
    recomm_profiles = get_recomms(df_dataset, user_index, desired_age, desired_status, desired_gender, desired_orientation, desired_relationship, cosine_sim)
    return recomm_profiles
