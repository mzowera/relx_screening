from scraper.quotes import get_quotes
from utils.s3 import upload_to_s3

def main():
    quotes = get_quotes()
    upload_to_s3(quotes)

if __name__ == '__main__':
    main()
