from scraper import scrape_comments  # Updated import statement
from sentiment import analyze_sentiment
import pandas as pd
import streamlit as st

# Streamlit app title
st.title("Instagram Comment Sentiment Analysis")

# Input for Instagram post URL
url = st.text_input("Enter Instagram Post URL:")

if url:
    # Scrape comments
    st.write("Scraping comments...")
    csv_path = scrape_comments(url)  # Updated function name

    # Perform sentiment analysis
    st.write("Analyzing sentiment...")
    df = analyze_sentiment(csv_path)

    # Display results
    st.write("### Sentiment Analysis Results")
    st.dataframe(df)

    # Download results as CSV
    st.write("### Download Results")
    st.download_button(
        label="Download CSV",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name=f"instagram_comments_sentiment.csv",
        mime="text/csv",
    )