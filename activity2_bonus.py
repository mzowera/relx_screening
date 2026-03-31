import schedule
import time
from datetime import datetime

from scraper.quotes import get_quotes
from utils.s3 import upload_to_s3

def job():
    print(f"[{datetime.now()}] Running scraper...")
    
    quotes = get_quotes() 
    upload_to_s3(quotes)
    
    print(f"Scraped {len(quotes)} quotes")


def run_scheduler():
    # Run every day at 2 AM
    schedule.every().day.at("02:00").do(job)

    print("Scheduler started...")

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    run_scheduler()