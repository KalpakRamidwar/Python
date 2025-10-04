import tkinter as tk
from tkinter import messagebox
from textblob import TextBlob
import sqlite3

# Function to analyze sentiment
def analyze_sentiment(tweet):
    analysis = TextBlob(tweet)
    polarity = analysis.sentiment.polarity
    
    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

# Function to perform sentiment analysis
def perform_analysis():
    user_tweet = tweet_entry.get()
    sentiment = analyze_sentiment(user_tweet)
    
    # Store the tweet and its sentiment in the database
    store_tweet(user_tweet, sentiment)
    
    result_label.config(text=f"The sentiment of the entered tweet is: {sentiment}")

# Function to validate login
def validate_login():
    username = username_entry.get()
    password = password_entry.get()

    # Connect to the SQLite database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Check if the user exists with the provided credentials
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    
    if user:
        messagebox.showinfo("Login Success", "You have logged in successfully!")
        login_frame.pack_forget()  # Hide the login frame
        main_frame.pack(pady=20)   # Show the main frame for sentiment analysis
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

    conn.close()

# Function to store tweet and sentiment in the database
def store_tweet(tweet, sentiment):
    conn = sqlite3.connect('tweets.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tweets (
            id INTEGER PRIMARY KEY,
            tweet TEXT NOT NULL,
            sentiment TEXT NOT NULL
        )
    ''')
    
    cursor.execute("INSERT INTO tweets (tweet, sentiment) VALUES (?, ?)", (tweet, sentiment))
    conn.commit()
    conn.close()

# Function to set up the user database (if needed)
def setup_user_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    # Insert dummy user for testing
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('sentiment', 'analyse'))
    conn.commit()
    conn.close()

# Creating the main application window
root = tk.Tk()
root.title("Sentiment Analysis App")
root.geometry("400x300")

# Set up the user database
setup_user_database()

# Login Frame
login_frame = tk.Frame(root)
login_frame.pack(pady=20)

tk.Label(login_frame, text="Username").grid(row=0, column=0, padx=10, pady=10)
username_entry = tk.Entry(login_frame)
username_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(login_frame, text="Password").grid(row=1, column=0, padx=10, pady=10)
password_entry = tk.Entry(login_frame, show="*")
password_entry.grid(row=1, column=1, padx=10, pady=10)

login_button = tk.Button(login_frame, text="Login", command=validate_login)
login_button.grid(row=2, columnspan=2, pady=10)

# Main Frame for sentiment analysis
main_frame = tk.Frame(root)

tk.Label(main_frame, text="Enter the tweet or text:").pack(pady=10)
tweet_entry = tk.Entry(main_frame, width=50)
tweet_entry.pack(pady=10)

analyze_button = tk.Button(main_frame, text="Analyze Sentiment", command=perform_analysis)
analyze_button.pack(pady=10)

result_label = tk.Label(main_frame, text="")
result_label.pack(pady=10)

# Start the main loop
root.mainloop()