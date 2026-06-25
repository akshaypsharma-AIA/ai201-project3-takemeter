import requests
import csv
import time

def scrape_nba(limit=500):
    headers = {"User-Agent": "Mozilla/5.0"}
    posts = []
    
    # Scrape hot posts
    url = "https://www.reddit.com/r/nba/hot.json?limit=100"
    response = requests.get(url, headers=headers)
    print(response.status_code)
    print(response.text[:500])
    data = response.json()
    print(data.keys())
    
    for post in data["data"]["children"]:
        text = post["data"]["title"]
        if len(text) > 20:  # skip very short titles
            posts.append({"text": text, "label": ""})
    
    time.sleep(2)  # be polite to Reddit
    
    # Scrape comments from top posts
    for post in data["data"]["children"][:10]:
        post_id = post["data"]["id"]
        comment_url = f"https://www.reddit.com/r/nba/comments/{post_id}.json?limit=20"
        r = requests.get(comment_url, headers=headers)
        comments = r.json()
        
        try:
            for comment in comments[1]["data"]["children"]:
                text = comment["data"].get("body", "")
                if len(text) > 30 and len(text) < 500:
                    posts.append({"text": text, "label": ""})
        except:
            pass
        
        time.sleep(1)
    
    # Save to CSV
    with open("nba_posts.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["text", "label"])
        writer.writeheader()
        writer.writerows(posts)
    
    print(f"Saved {len(posts)} posts to nba_posts.csv")

scrape_nba()