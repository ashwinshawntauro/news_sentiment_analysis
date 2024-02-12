# Import libraries
from textblob import TextBlob

# Function to clean text (replace with your specific steps)
def clean_text(text):
  text = text.lower() # lowercase
  text = text.replace("[^a-zA-Z ]", "") # remove non-alphanumeric characters
  text = " ".join(text.split()) # remove duplicate spaces
  return text

# Function to analyze sentiment and categorize
def analyze_sentiment(text):
  cleaned_text = clean_text(text)
  blob = TextBlob(cleaned_text)

  # Define thresholds for categorization
  neutral_threshold = 0.2
  positive_threshold = 0.5

  if blob.polarity > positive_threshold:
    sentiment = "good"
  elif blob.polarity < -positive_threshold:
    sentiment = "bad"
  else:
    sentiment = "neutral"

  return sentiment

# Sample usage
news_text = "No noise"
sentiment = analyze_sentiment(news_text)

print(f"Text: {news_text}")
print(f"Sentiment: {sentiment}")

# Adapt and expand for your specific use case:
# 1. Integrate web scraping libraries for data.
# 2. Loop through news articles, analyze sentiment, store results.
# 3. Count and visualize sentiment distribution by category.
# 4. Fine-tune thresholds and consider subjectivity for nuance.

