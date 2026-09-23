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
        
        # إضافة الـ Headers المطلوبة للمصادقة مع Bybit
        headers = {
            "X-BAPI-API-KEY": BYBIT_API_KEY if BYBIT_API_KEY else "",
            "Content-Type": "application/json"
        }
        
        # يمكنك تعديل الروابط حسب الحاجة
        response = requests.get("https://api.bybit.com/v5/market/time", headers=headers, timeout=10)
        
        if response.status_code == 200:
            log("API request successful.")
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
