import praw
import pandas as pd
import os
from datetime import datetime
import time

date = datetime.today().strftime('%Y-%m-%d')

# Add the path for the saved file
EXCEL_FILE_PATH = rf'[Path]\Reddit_Post_{date}.csv'

# 🔑 Add your credentials here
client_id = "enter_your_clientid"
client_secret = "enter_your_client_secret"
user_agent = "enter_your_user_agent"

# Initialize Reddit API client
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)

# Fetch multiple pages of posts
subreddit = reddit.subreddit("enter_your_subreddit")
posts = []

# Define the number of pages and posts per page
num_pages = 10  # Adjust the number of pages you want
posts_per_page = 100  # Max is 100 per request

# Pagination: Fetch multiple pages using `after`
last_post_id = None  # Keeps track of last post ID

for _ in range(num_pages):
    if last_post_id:
        new_posts = subreddit.new(limit=posts_per_page, params={"after": last_post_id})
    else:
        new_posts = subreddit.new(limit=posts_per_page)
    
    count = 0  # Track number of posts fetched
    for submission in new_posts:
        posts.append({
            "title": submission.title,
            "author": submission.author.name if submission.author else "[deleted]",
            "score": submission.score,
            "num_comments": submission.num_comments,
            "created_utc": datetime.utcfromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
            "post_url": submission.url,
            "id": submission.id
        })
        last_post_id = submission.fullname  # Correct way to paginate
        count += 1

    print(f"Fetched {count} posts in batch {_ + 1}")

    time.sleep(2)  # Add delay to avoid hitting rate limits

# Convert to DataFrame
df = pd.DataFrame(posts)

# Show results

# Extract file to CSV
def upload_to_folder(file_path):
    """Placeholder function for folder upload"""
    print(f"Uploading {file_path} to folder")
    
# Save to Excel
df.to_csv(EXCEL_FILE_PATH, index=False)
print(f"Data saving completed: {EXCEL_FILE_PATH}")

# Upload to folder (if implemented)
upload_to_folder(EXCEL_FILE_PATH)
