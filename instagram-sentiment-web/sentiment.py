import pandas as pd
from textblob import TextBlob

# Step 1: Load the CSV file
def load_data(csv_path):
    df = pd.read_csv(csv_path)
    return df

# Step 2: Perform sentiment analysis
def analyze_sentiment(df):
    def get_polarity(text):
        # Analyze sentiment using TextBlob
        return TextBlob(text).sentiment.polarity

    # Add polarity and sentiment columns
    df['text_polarity'] = df['comment_text'].apply(get_polarity)
    df['sentiment'] = pd.cut(df['text_polarity'], [-1, -0.00001, 0.00001, 1], labels=["Negative", "Neutral", "Positive"])
    return df

# Step 3: Save the results to a new CSV file
def save_results(df, output_path):
    df.to_csv(output_path, index=False)
    print(f"Results saved to {output_path}")

# Main function
def main():
    # Input CSV file path
    csv_path = input("Enter the path to the CSV file: ")

    # Load data
    print("Loading data...")
    df = load_data(csv_path)

    # Perform sentiment analysis
    print("Analyzing sentiment...")
    df = analyze_sentiment(df)

    # Save results
    output_path = "instagram_comments_DHLolwztvBW.csv"
    save_results(df, output_path)

# Run the script
if __name__ == "__main__":
    main()