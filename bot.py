import os
import json
import time
import requests

BYBIT_API_KEY = os.getenv("BYBIT_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def get_bybit_price():
    try:
        url = "https://api.bybit.com/v5/market/tickers?category=linear&symbol=BTCUSDT"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        data = response.json()
        if data.get("retCode") == 0 and len(data['result']['list']) > 0:
            price = data['result']['list'][0]['lastPrice']
            return float(price)
        return None
    except Exception as e:
        return None

def get_ai_analysis(price):
    try:
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "deepseek/deepseek-chat",
            "messages": [
                {"role": "user", "content": f"The current Bitcoin price on Bybit is {price}. Give a very short professional trading analysis and recommendation (Buy/Sell/Hold) in English."}
            ]
        }
        response = requests.post(url, headers=headers, json=payload)
        res_data = response.json()
        return res_data['choices'][0]['message']['content']
    except Exception as e:
        return "Error in AI analysis"

if __name__ == "__main__":
    print("بدء تشغيل حلقة المراقبة لمدة مستمرة...")
    
    # حساب مدة 6 ساعات بالثواني (6 * 3600 = 21600 ثانية)
    end_time = time.time() + 6 * 3600
    
    while time.time() < end_time:
        print("جاري جلب السعر من Bybit...")
        btc_price = get_bybit_price()
        
        if btc_price:
            print(f"السعر الحالي: {btc_price}")
            analysis = get_ai_analysis(btc_price)
            
            status_data = {
                "price": btc_price,
                "analysis": analysis,
                "status": "Running Continuously"
            }
            
            with open("status.json", "w", encoding="utf-8") as f:
                json.dump(status_data, f, ensure_ascii=False, indent=4)
            print("تم تحديث status.json بنجاح!")
        else:
            print("فشل في جلب السعر، إعادة المحاولة...")

        # الانتظار لمدة 5 دقائق (300 ثانية) قبل المراقبة الموالية
        time.sleep(300)
