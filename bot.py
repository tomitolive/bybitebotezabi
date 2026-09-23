import os
import requests

BYBIT_API_KEY = os.getenv("BYBIT_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def log(message):
    print(message, flush=True)

def main():
    log("Starting bot.py script...")

    try:
        log("Fetching data from Bybit API...")
        
        # Headers متكاملة تحاكي متصفح حقيقي لتجاوز حظر CloudFront WAF
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://www.bybit.com/",
            "X-BAPI-API-KEY": BYBIT_API_KEY if BYBIT_API_KEY else "",
            "Content-Type": "application/json"
        }
        
        # طلب البيانات مع الـ Headers والـ Timeout
        response = requests.get("https://api.bybit.com/v5/market/time", headers=headers, timeout=10)
        
        if response.status_code == 200:
            log("API request successful!")
            data = response.json()
            log(f"Response data: {data}")
        else:
            log(f"API request failed with status code: {response.status_code}")
            log(f"Response text: {response.text}")
            
    except requests.exceptions.Timeout:
        log("Error: The API request timed out!")
    except Exception as e:
        log(f"An error occurred: {e}")

    log("Bot script finished execution successfully.")

if __name__ == "__main__":
    main()
