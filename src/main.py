import os
import pandas as pd
from flask import Flask, request, render_template, redirect, url_for
from matchalgo import get_combined_recommendations

app = Flask(__name__)

# Resolve the base directory and absolute path for `data.csv`
base_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_dir, 'data', 'data.csv')

# Load user data for authentication using the absolute path
user_data = pd.read_csv(data_path)

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/preferences', methods=['POST'])
def preferences():
    email = request.form['email']
    password = request.form['password']

    # Check if the email and password match any in the dataset
    matched = user_data[(user_data['email'] == email) & (user_data['password'] == password)]
    if not matched.empty:
        return render_template('preference.html')
    else:
        # If incorrect, redirect to login
        return redirect(url_for('login'))

@app.route('/match', methods=['POST'])
def match():
    desired_age = int(request.form['age'])
    desired_status = request.form['status']
    desired_gender = request.form['gender']
    desired_orientation = request.form['orientation']
    desired_relationship = request.form['relationship']

    # Generate matching profiles with the absolute path to `data.csv`
    recomm_profiles = get_combined_recommendations(
        data_path,
        desired_age,
        desired_status,
        desired_gender,
        desired_orientation,
        desired_relationship
    )

    return render_template('match.html', profiles=recomm_profiles.to_html(index=False))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
