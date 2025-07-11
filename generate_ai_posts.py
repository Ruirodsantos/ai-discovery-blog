import os
import requests
from datetime import datetime

# === CONFIGURATION ===
NUM_POSTS = 10
POSTS_DIR = "_posts"
NEWS_API_URL = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "YOUR_NEWS_API_KEY"  # Replace with your actual NewsAPI key

PARAMS = {
    "q": "artificial intelligence",
    "language": "en",
    "sortBy": "publishedAt",
    "pageSize": NUM_POSTS,
    "apiKey": NEWS_API_KEY,
}

# === FETCH NEWS ===
response = requests.get(NEWS_API_URL, params=PARAMS)
articles = response.json().get("articles", [])

if not os.path.exists(POSTS_DIR):
    os.makedirs(POSTS_DIR)

# === CREATE POSTS ===
for article in articles:
    date = datetime.strptime(article["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
    filename = f"{date.strftime('%Y-%m-%d')}-{article['title'][:50].replace(' ', '-').replace('/', '').replace(':', '').lower()}.md"
    filepath = os.path.join(POSTS_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write(f"layout: post\n")
        f.write(f"title: \"{article['title']}\"\n")
        f.write(f"date: {date.strftime('%Y-%m-%d')}\n")
        f.write("---\n\n")
        f.write(f"{article['description'] or 'No description available.'}\n\n")
        f.write(f"Read more at: [{article['source']['name']}]({article['url']})\n")

print(f"✅ {len(articles)} posts created in '{POSTS_DIR}' folder.")
