import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def assign_age_score(profile_age, desired_age):
    return 0 if abs(profile_age - desired_age) else 1

def assign_status_score(profile_status, desired_status):
    return 0 if profile_status == desired_status else 1

def assign_sex_score(profile_sex, desired_sex):
    return 0 if profile_sex.lower() == desired_sex.lower() else 1

def assign_orientation_score(profile_orientation, desired_orientation):
    return 0 if profile_orientation == desired_orientation else 1

def assign_relationship_score(profile_relationship, desired_relationship):
    return 0 if profile_relationship.lower() == desired_relationship.lower() else 1

def combine_scores(age_scores, status_scores, sex_scores, orientation_scores, relationship_scores, cosine_sim_scores):
    combined_scores = (
        age_scores +
        status_scores +
        sex_scores +
        orientation_scores +
        relationship_scores +
        cosine_sim_scores
    )
    return combined_scores

def calculate_match_percentage(combined_scores):
    max_score = combined_scores.max()
    match_percentage = ((max_score - combined_scores) / max_score * 100).round(2)  # Round to 2 decimal places
    return match_percentage

def rank_profiles(df, match_percentages):
    df['match_percentage'] = match_percentages
    ranked_profiles = df.sort_values(by='match_percentage', ascending=False).head(10)
    return ranked_profiles[['age', 'status', 'sex', 'orientation', 'relationship_type', 'essay0', 'match_percentage']]

def get_recomms(df, desired_age, desired_status, desired_sex, desired_orientation, desired_relationship, cosine_sim):
    age_scores = df['age'].apply(lambda x: assign_age_score(x, desired_age))
    status_scores = df['status'].apply(lambda x: assign_status_score(x, desired_status))
    sex_scores = df['sex'].apply(lambda x: assign_sex_score(x, desired_sex))
    orientation_scores = df['orientation'].apply(lambda x: assign_orientation_score(x, desired_orientation))
    relationship_scores = df['relationship_type'].apply(lambda x: assign_relationship_score(x, desired_relationship))
    cosine_sim_scores = cosine_sim[:, 0]
    combined_scores = combine_scores(age_scores, status_scores, sex_scores, orientation_scores, relationship_scores, cosine_sim_scores)
    match_percentages = calculate_match_percentage(combined_scores)
    ranked_profiles = rank_profiles(df, match_percentages)
    return ranked_profiles

def get_combined_recommendations(df_path, desired_age, desired_status, desired_sex, desired_orientation, desired_relationship):
    df_dataset = pd.read_csv(df_path, nrows=100)
    df_dataset['essay0'] = df_dataset['essay0'].fillna(" ")
    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(df_dataset['essay0'])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    recomm_profiles = get_recomms(df_dataset, desired_age, desired_status, desired_sex, desired_orientation, desired_relationship, cosine_sim)
    return recomm_profiles
