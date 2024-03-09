# Import necessary libraries
from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Set up Flask
app = Flask(__name__)

# Set of stopwords
stop_words = set(stopwords.words('english'))

# Function to clean and preprocess text
def clean_text(text):
    text = text.lower()  # Convert text to lowercase
    words = word_tokenize(text)  # Tokenize the text into words
    cleaned_words = [word for word in words if word.isalpha() and word not in stop_words]  # Remove stopwords and non-alphabetic words
    cleaned_text = " ".join(cleaned_words)  # Join words back into a string
    return cleaned_text

# Function to analyze sentiment and categorize
def analyze_sentiment(text):
    cleaned_text = clean_text(text)
    blob = TextBlob(cleaned_text)

    # Define thresholds for categorization
    neutral_threshold = 0.1
    positive_threshold = 0.2

    positive_keywords = ['strong', 'positive' ,'premium', 'soars', 'profit', 'bullish' ,'growth', 'high', 'upside', 'rally', 'rise', 'raises', 'buy', 'zooms', 'uptrend','highest','jump','up']
    negative_keywords = ['negative', 'weak', 'decline' , 'loss', 'bearish', 'sell-of', 'slump', 'underperform', 'downgrade', 'plunge', 'turmoil', 'panic', 'correction', 'volatility', 'downtrend','lowest','fall','down']

    # Check if any positive keyword is in the cleaned text
    if any(word in text for word in positive_keywords):
        sentiment = "Positive"
    elif any(word in text for word in negative_keywords):
        sentiment = "Negative"
    elif blob.sentiment.polarity > positive_threshold:
        sentiment = "Positive"
    elif blob.sentiment.polarity < -positive_threshold:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return sentiment

# Function to fetch news articles from Moneycontrol
def fetch_news():
    url = 'https://www.moneycontrol.com/news/business/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = []
    for article in soup.find_all('li', {'class': 'clearfix'}):
        title = article.find('h2').text.strip()
        summary = article.find('p').text.strip()
        link = article.find('a')['href']
        img = article.find('img')['data-src']
        img = img.replace("width=135", "width=770")  # Change width to 200
        img = img.replace("height=80", "height=443")
        # Fetch the date of the news article
        date = article.find('span').text.strip()
        articles.append({
            'title': title,
            'summary': summary,
            'link': link,
            'image': img,
            'date': date  # Add date to the dictionary
        })

    return articles

# Route for home page
@app.route('/')
def home():
    # Fetch news articles
    articles = fetch_news()

    # Initialize counts for sentiments
    positive_count = 0
    negative_count = 0
    neutral_count = 0

    # Analyze sentiment for each article
    for article in articles:
        title = article['title']
        summary = article['summary']
        image = article['image']

        # Combine title and summary for analysis
        text = title + ". " + summary

        # Analyze sentiment
        sentiment = analyze_sentiment(text)
        article['sentiment'] = sentiment

        # Count the sentiments
        if sentiment == 'Positive':
            positive_count += 1
        elif sentiment == 'Negative':
            negative_count += 1
        else:
            neutral_count += 1

    # Calculate percentages
    total_count = len(articles)
    positive_percent = (positive_count / total_count) * 100 if total_count > 0 else 0
    negative_percent = (negative_count / total_count) * 100 if total_count > 0 else 0
    neutral_percent = (neutral_count / total_count) * 100 if total_count > 0 else 0

    return render_template('index.html', articles=articles, positive_count=positive_count, negative_count=negative_count, neutral_count=neutral_count, positive_percent=positive_percent, negative_percent=negative_percent, neutral_percent=neutral_percent)

if __name__ == '__main__':
    app.run(debug=True)
