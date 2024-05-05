import os
import pandas as pd
from flask import Flask, request, render_template, redirect, url_for, session, flash
from matchalgo import get_combined_recommendations, get_user_id_from_credentials

app = Flask(__name__)
app.secret_key = 'some_secret_key'  # For session management

# Resolve the base directory and absolute path for `data.csv`
base_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_dir, 'data', 'data.csv')

# Load user data for authentication using the absolute path
user_data = pd.read_csv(data_path)

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            # Retrieve the user ID based on credentials
            user_id = get_user_id_from_credentials(user_data, email, password)
            session['user_id'] = int(user_id) # Store the user ID in the session
            return render_template('preference.html')
        except ValueError:
            flash('Invalid email or password. Please try again.')
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/preference')
def preferences():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if user is not logged in

    # Add a debug statement to check session information
    print(f"User ID from session: {session['user_id']}")

    # Render the preference page
    return render_template('preference.html')


@app.route('/match', methods=['POST'])
def match():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Get preferences from the form
    desired_age = int(request.form['age'])
    desired_status = request.form['status']
    desired_gender = request.form['gender']
    desired_orientation = request.form['orientation']
    desired_relationship = request.form['relationship']

    # Retrieve the user ID from the session
    user_id = session['user_id']

    # Generate matching profiles
    try:
        recomm_profiles = get_combined_recommendations(
            data_path,
            user_id,
            desired_age,
            desired_status,
            desired_gender,
            desired_orientation,
            desired_relationship
        )
    except Exception as e:
        flash(str(e))
        return redirect(url_for('preference'))

    return render_template('match.html', profiles=recomm_profiles.to_html(index=False))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
