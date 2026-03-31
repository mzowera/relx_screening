from datetime import datetime

from utils.s3 import upload_to_s3

def generate_data():
    # Replace this with your scraper later
    return {
        "message": "Hello from EC2",
        "timestamp": str(datetime.now())
    }

if __name__ == "__main__":
    data = generate_data()
    upload_to_s3(data)