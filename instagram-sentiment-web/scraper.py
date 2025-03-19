import pandas as pd
from instaloader import Instaloader, Post, ConnectionException
from glob import glob
from os.path import expanduser
from sqlite3 import connect
import time

# Step 1: Authenticate using Firefox cookies
def authenticate_instagram():
    # Path to your Firefox cookies file
    path_to_firefox_cookies = "C:/Users/svish/AppData/Roaming/Mozilla/Firefox/Profiles/vbpglpvj.default-release/cookies.sqlite"
    FIREFOXCOOKIEFILE = glob(expanduser(path_to_firefox_cookies))[0]

    # Initialize Instaloader
    instaloader = Instaloader(max_connection_attempts=1)

    # Load cookies from Firefox
    conn = connect(FIREFOXCOOKIEFILE)
    cursor = conn.cursor()
    cursor.execute("SELECT name, value FROM moz_cookies WHERE host='.instagram.com'")
    cookies = {name: value for name, value in cursor.fetchall()}
    instaloader.context._session.cookies.update(cookies)

    # Test the connection
    try:
        username = instaloader.test_login()
        if not username:
            raise ConnectionException("Failed to log in.")
    except ConnectionException as e:
        raise SystemExit(f"Cookie import failed: {e}. Are you logged in successfully in Firefox?")

    instaloader.context.username = username

    # Save session for future use
    instaloader.save_session_to_file()
    return instaloader

# Step 2: Scrape comments from a post
def scrape_comments(url):
    # Authenticate
    instaloader = authenticate_instagram()

    # Extract shortcode from URL
    shortcode = url.split("/")[-2]

    # Initialize Instaloader
    instagram = Instaloader()

    # Load session
    instagram.load_session_from_file('divya_lakshmi_1029')  # Replace with your Instagram username

    # Get post using shortcode
    post = Post.from_shortcode(instagram.context, shortcode)

    # Scrape comments
    comments_data = []
    for comment in post.get_comments():
        comments_data.append({
            "post_shortcode": post.shortcode,
            "commenter_username": comment.owner.username,
            "comment_text": comment.text,
            "comment_likes": comment.likes_count
        })
        time.sleep(2)  # Add delay to avoid rate limiting

    # Convert to DataFrame
    df = pd.DataFrame(comments_data)
    return df

# Step 3: Save results to CSV
def save_to_csv(df, shortcode):
    output_file = f"instagram_comments_{shortcode}.csv"
    df.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")

# Main function
def main():
    # Input Instagram post URL
    url = input("Enter the Instagram post URL: ")
    shortcode = url.split("/")[-2]  # Extract shortcode from URL

    # Scrape comments
    print("Scraping comments...")
    df = scrape_comments(url)

    # Save results to CSV
    save_to_csv(df, shortcode)

# Run the script
if __name__ == "__main__":
    main()