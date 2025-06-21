from transformers import pipeline

# Load model once to avoid reloading it for each request
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
