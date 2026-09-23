import os
import requests
import sys

# جلب المفاتيح من Environment Variables
BYBIT_API_KEY = os.getenv("BYBIT_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def log(message):
    print(message, flush=True)

def main():
    log("Starting bot.py script...")

    # مثال على طلب API مع تفعيل الـ timeout لتفادي التبلوكاج
    try:
        log("Fetching data from API...")
        # استبدل الرابط برابط الـ API الحقيقي لي كتخدم بيه
        response = requests.get("https://api.bybit.com/v5/market/time", timeout=10)
        
        if response.status_code == 200:
            log("API request successful.")
            data = response.json()
            log(f"Response data: {data}")
        else:
            log(f"API request failed with status code: {response.status_code}")
            
    except requests.exceptions.Timeout:
        log("Error: The API request timed out!")
    except Exception as e:
        log(f"An error occurred: {e}")

    log("Bot script finished execution successfully.")

if __name__ == "__main__":
    main()
