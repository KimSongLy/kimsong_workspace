import requests
import csv
from datetime import datetime

def fetch_all_reviews(appid, params=None):
    if params is None:
        params = {
            'json': 1,
            'filter': 'recent',
            'language': 'all',
            'day_range': '10',
            'cursor': '*',
            'review_type': 'all',
            'purchase_type': 'all',
            'num_per_page': '100',
            #'filter_offtopic_activity': 1
        }
    
    all_reviews = []
    
    #time_interval = timedelta(hours=24)                 
    #the timestamp in the return result are unix timestamp (GMT+0)
    #start time is January 1, 2024 and end time is December 31, 2024
    start_time = datetime(2024, 1, 1, 0, 0, 0)
    end_time = datetime(2024, 12, 31, 23, 59, 59)
    
    passed_start_time = False
    passed_end_time = False
    
    #runs until both passed_start_time and passed_end_time are set to True
    while not passed_start_time or not passed_end_time:  
        url = f'https://store.steampowered.com/appreviews/{appid}'
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            reviews_data = response.json()
            
            if reviews_data['success'] != 1 or not reviews_data.get('reviews'):
                break
            
            valid_reviews = []
            for review in reviews_data['reviews']:
                timestamp_created = review['timestamp_created']

                #skip comments beyond end_time
                if not passed_end_time:
                    if timestamp_created > end_time.timestamp():
                        continue
                    else:
                        passed_end_time = True
                
                if not passed_start_time:
                    if timestamp_created < start_time.timestamp():
                        passed_start_time = True
                        break

                if review['review']:
                    review['review'] = review['review']
                else:
                    review['review'] = "No review text"

                valid_reviews.append(review)
                
            
            all_reviews.extend(valid_reviews)

            print(f"Fetched {len(reviews_data['reviews'])} reviews, moving to next page...")

            # 커서 값 출력
            params['cursor'] = reviews_data.get('cursor', None)
            print(f"Current cursor: {params['cursor']}")

            if params['cursor'] is None:
                print("No more pages to fetch. Exiting loop.")
                break
        else:
            print(f"Error: {response.status_code}")
            break
    
    return all_reviews

def save_reviews_to_csv(reviews, output_file):
    fieldnames = ['recommendationid', 'author.steamid', 'author.num_games_owned', 
                  'author.num_reviews', 'author.playtime_forever', 
                  'author.playtime_last_two_weeks', 'author.playtime_at_review', 
                  'author.last_played', 'language', 'review', 
                  'timestamp_created', 'voted_up', 'votes_up', 
                  'comment_count', 'steam_purchase', 'received_for_free']

    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for review in reviews:
            flat_review = {
                'recommendationid': review['recommendationid'],
                'author.steamid': review['author']['steamid'],
                'author.num_games_owned': review['author']['num_games_owned'],
                'author.num_reviews': review['author']['num_reviews'],
                'author.playtime_forever': review['author']['playtime_forever'],
                'author.playtime_last_two_weeks': review['author']['playtime_last_two_weeks'],
                'author.playtime_at_review': review['author']['playtime_at_review'],
                'author.last_played': review['author']['last_played'],
                'language': review['language'],
                'review': review['review'],
                'timestamp_created': datetime.fromtimestamp(review['timestamp_created']).isoformat(),
                'voted_up': review['voted_up'],
                'votes_up': review['votes_up'],
                'comment_count': review['comment_count'],
                'steam_purchase': review['steam_purchase'],
                'received_for_free': review['received_for_free']
            }
            writer.writerow(flat_review)

if __name__ == "__main__":
    appid = input("Enter the Steam App ID: ").strip()
    output_file = input("Enter the output CSV file name (e.g., reviews.csv): ").strip()

    reviews = fetch_all_reviews(appid)
    save_reviews_to_csv(reviews, output_file)
    print(f"All reviews saved to {output_file}")
