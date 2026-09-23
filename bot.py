import os
import json
import requests

# قراءة المفاتيح بأمان من GitHub Secrets
BYBIT_API_KEY = os.getenv("BYBIT_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def get_bybit_price():
    try:
        # جلب سعر البيتكوين مباشرة من Bybit API بدون الحاجة لـ ccxt لتجنب مشاكل التثبيت
        url = "https://api.bybit.com/v5/market/tickers?category=spot&symbol=BTCUSDT"
        response = requests.get(url)
        data = response.json()
        price = data['result']['list'][0]['lastPrice']
        return float(price)
    except Exception as e:
        return f"خطأ في جلب السعر: {str(e)}"

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
        return f"خطأ في التحليل الذكي: {str(e)}"

if __name__ == "__main__":
    print("جاري جلب البيانات من Bybit...")
    btc_price = get_bybit_price()
    print(f"السعر الحالي: {btc_price}")

    print("جاري إرسال البيانات إلى OpenRouter AI للتحليل...")
    analysis = get_ai_analysis(btc_price)
    print(f"التحليل: {analysis}")

    # حفظ النتائج في ملف status.json لكي تقرأه واجهة الموقع (Admin Panel)
    status_data = {
        "price": btc_price,
        "analysis": analysis,
        "status": "Running Successfully"
    }
    
    with open("status.json", "w", encoding="utf-8") as f:
        json.dump(status_data, f, ensure_ascii=False, indent=4)
    print("تم تحديث حالة البوت بنجاح!")
  
