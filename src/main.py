import os
import pandas as pd
from flask import Flask, request, render_template, redirect, url_for, session, flash
from matchalgo import get_combined_recommendations, get_user_id_from_credentials

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session security

# Resolve the base directory and absolute path for `data.csv`
base_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_dir, 'data', 'data.csv')

# Load user data using the absolute path
user_data = pd.read_csv(data_path)

@app.route('/')
def homepage():
    """ Render the homepage """
    return render_template('homepage.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Login route for user authentication """
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            # Retrieve user data based on credentials
            user_row = user_data[(user_data['email'] == email) & (user_data['password'] == password)]
            if user_row.empty:
                raise ValueError("Invalid email or password")

            # Extract user ID and gender for session storage
            user_id = int(user_row['user_id'].values[0])
            user_gender = user_row['gender'].values[0].lower()

            # Store user details in session
            session['user_id'] = user_id
            session['gender'] = user_gender

            return redirect(url_for('preferences'))
        except ValueError:
            flash('Invalid email or password. Please try again.')
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/preference', methods=['GET', 'POST'])
def preferences():
    """ Set user preferences with automatic orientation determination """
    if 'user_id' not in session or 'gender' not in session:
        return redirect(url_for('login'))

    user_gender = session['gender']
    desired_gender = ''
    orientation = ''
    age = status = relationship = ''

    if request.method == 'POST':
        desired_gender = request.form['gender'].lower()
        age = request.form.get('age', '')
        status = request.form.get('status', '')
        relationship = request.form.get('relationship', '')

    return render_template('preference.html', age=age, status=status, desired_gender=desired_gender, orientation=orientation, relationship=relationship)


@app.route('/match', methods=['POST'])
def match():
    """ Match profiles based on preferences provided """
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Retrieve preferences from the form
    desired_age = int(request.form['age'])
    desired_status = request.form['status']
    desired_gender = request.form['gender'].lower()
    desired_relationship = request.form['relationship']
    desired_orientation = request.form['orientation']

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
        return redirect(url_for('preferences'))

    # Convert profiles DataFrame to HTML with the index hidden
    return render_template('match.html', profiles=recomm_profiles.to_html(index=False))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
