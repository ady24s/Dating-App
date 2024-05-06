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
    """Login route for user authentication."""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        aadhaar = int(request.form['aadhaar'])

        try:
            # Retrieve user data based on credentials and Aadhaar number
            user_row = user_data[
                (user_data['email'] == email) &
                (user_data['password'] == password) &
                (user_data['aadhaar'] == aadhaar)
            ]

            if user_row.empty:
                raise ValueError("Invalid email, password, or Aadhaar number")

            # Extract user details for session storage
            user_id = int(user_row['user_id'].values[0])
            user_gender = user_row['gender'].values[0].lower()

            # Store user details in session
            session['user_id'] = user_id
            session['gender'] = user_gender

            # Redirect to the preference page after a successful login
            return redirect(url_for('preferences'))
        except ValueError:
            flash('Invalid email, password, or Aadhaar number. Please try again.')
            return render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/preference', methods=['GET', 'POST'])
def preferences():
    """ Set user preferences with automatic relationship determination """
    if 'user_id' not in session or 'gender' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    user_gender = session['gender']
    desired_gender = ''
    desired_orientation = ''
    desired_age = ''
    desired_status = ''
    desired_relationship = ''

    # Get the logged-in user's actual status from the data
    user_row = user_data[user_data['user_id'] == user_id]
    if not user_row.empty:
        actual_status = user_row['status'].values[0].lower()
        # Automatically set relationship to "Friendship" if actual status is "taken"
        if actual_status == 'taken':
            desired_relationship = 'Friendship'

    if request.method == 'POST':
        desired_gender = request.form['gender'].lower()
        desired_orientation = request.form.get('orientation', '')
        desired_age = request.form.get('age', '')
        desired_status = request.form.get('status', '')  # Let the user input their desired status
        # If the user has chosen something other than "taken," retain their input
        if actual_status != 'taken':
            desired_relationship = request.form.get('relationship', '')

    return render_template('preference.html', age=desired_age, status=desired_status, desired_gender=desired_gender, orientation=desired_orientation, relationship=desired_relationship)



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
