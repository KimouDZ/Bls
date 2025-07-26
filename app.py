import os
import requests
from bs4 import BeautifulSoup
import time

# استيراد token البوت و chat_id من متغيرات البيئة (ستحددها في railway)
TELEGRAM_BOT_TOKEN = os.getenv('8196868477:AAGPMnAc1fFqJvQcJGk8HsC5AYAnRkvu3cM')
TELEGRAM_CHAT_ID = os.getenv('1055739217')

# بيانات الدخول - استبدل هذه القيم بمتغيرات البيئة أيضاً في railway
BLS_USERNAME = os.getenv('akrambahnes@gmail.com')
BLS_PASSWORD = os.getenv('Kimoudz@27')

LOGIN_URL = "https://algeria.blsspainglobal.com/DZA/account/login"
APPOINTMENT_PAGE_URL = "https://algeria.blsspainglobal.com/DZA/appointment/scheduling/"

def send_telegram_message(text):
    api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    params = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text
    }
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")

def login_and_check_appointments():
    with requests.Session() as session:
        # خطوة تسجيل الدخول
        login_page = session.get(LOGIN_URL)
        soup = BeautifulSoup(login_page.text, "html.parser")

        # استخراج أي حقل hidden مطلوب (مثل __RequestVerificationToken)
        token_input = soup.find("input", {"name": "__RequestVerificationToken"})
        verification_token = token_input['value'] if token_input else ''

        login_payload = {
            "Login.Email": BLS_USERNAME,
            "Login.Password": BLS_PASSWORD,
            "__RequestVerificationToken": verification_token
        }

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        resp = session.post(LOGIN_URL, data=login_payload, headers=headers)
        if resp.url == LOGIN_URL:
            print("فشل تسجيل الدخول، تحقق من اسم المستخدم أو كلمة المرور")
            return

        # زيارة صفحة مواعيد الحجز بعد تسجيل الدخول
        appt_page = session.get(APPOINTMENT_PAGE_URL, headers=headers)
        appt_soup = BeautifulSoup(appt_page.text, "html.parser")

        # افحص هنا عن النص أو العنصر الذي يدل على توفر مواعيد
        # مثال: افترض أن وجود زر/نص "حجز موعد" يدل على توفر المواعيد
        if appt_soup.find(text=lambda t: "حجز موعد" in t):
            send_telegram_message("تنبيه: هناك مواعيد متاحة الآن في موقع حجز فيزا إسبانيا بنظام BLS الجزائر!")
            print("تم إرسال إشعار لحجز الموعد")
        else:
            print("لا توجد مواعيد متاحة حالياً")

if __name__ == "__main__":
    while True:
        try:
            login_and_check_appointments()
        except Exception as e:
            print(f"حدث خطأ: {e}")
        # انتظر 10 دقائق قبل الفحص التالي
        time.sleep(60)
      
