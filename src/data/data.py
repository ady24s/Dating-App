import pandas as pd
import numpy as np

# Setting seed for reproducibility
np.random.seed(42)

# Generate random names
def generate_names(n):
    first_names = ["Amit", "Priya", "Deepak", "Anjali", "Rajesh", "Sunita", "Vijay", "Deepika", "Karan", "Pooja",
                   "Sanjay", "Rani", "Arjun", "Meera", "Suresh", "Kavita", "Nikhil", "Simran", "Rahul", "Neha",
                   "Manish", "Asha", "Ajay", "Geeta", "Ravi", "Lata", "Anil", "Shreya", "Gautam", "Anita"]
    last_names = ["Sharma", "Patel", "Mehta", "Singh", "Gupta", "Kumar", "Joshi", "Reddy", "Ali", "Das",
                  "Paul", "Bose", "Nair", "Rao", "Chowdhury", "Mishra", "Verma", "Iyer", "Malhotra", "Seth"]
    names = [np.random.choice(first_names) + " " + np.random.choice(last_names) for _ in range(n)]
    return names

# Generate random emails
def generate_emails(names):
    domains = ["example.com", "mail.com", "provider.org"]
    emails = [name.replace(" ", ".").lower() + "@" + np.random.choice(domains) for name in names]
    return emails

# Generate random passwords
def generate_passwords(n):
    return ['password' + str(i).zfill(3) for i in range(1, n + 1)]

# Generate random ages
def generate_ages(n):
    return np.random.randint(35, 60, n)

# Generate random statuses
def generate_statuses(n):
    statuses = ["single", "taken"]
    return np.random.choice(statuses, n)

# Generate random genders
def generate_genders(n):
    genders = ["male", "female"]
    return np.random.choice(genders, n)

# Generate random orientations
def generate_orientations(n):
    orientations = ["straight", "homo"]
    return np.random.choice(orientations, n)

# Generate random essays
def generate_essays(n):
    themes = ["enjoys cricket and Bollywood movies",
              "likes cooking traditional Indian dishes and exploring new cuisines",
              "appreciates classical music and dance performances",
              "loves traveling within India and learning about different cultures",
              "is a tech enthusiast and enjoys discussing emerging technologies",
              "practices yoga and meditation for wellness",
              "is passionate about education and lifelong learning",
              "enjoys reading historical novels and writing",
              "is active in local community services and social causes",
              "has a keen interest in politics and social issues"]
    return ["Looking for a kind-hearted person who " + np.random.choice(themes) for _ in range(n)]

# Generate random relationship types
def generate_relationship_types(n):
    relationship_types = ["friendship", "relationship"]
    return np.random.choice(relationship_types, n)

# Create a DataFrame with appropriate columns
names = generate_names(100)
data = {
    'user_id': range(1, 101),
    'name': names,
    'email': generate_emails(names),
    'password': generate_passwords(100),
    'age': generate_ages(100),
    'status': generate_statuses(100),
    'sex': generate_genders(100),
    'orientation': generate_orientations(100),
    'essay0': generate_essays(100),
    'relationship_type': generate_relationship_types(100)
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Display the DataFrame
print(df.head(10))  # Displaying only the first 10 for brevity

# Optionally save to CSV
df.to_csv('src/data/data.csv', index=False)
