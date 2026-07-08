from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# إعدادات التليجرام
TOKEN = '8593713585:AAE3x1wyxnuGV1I_BLwdKj16ZJlegqpvO-4'
CHAT_ID = 'ضع_رقم_الـ_ID_الخاص_بك_هنا' # لا تنسَ وضع الـ ID الخاص بك هنا

# رقم الواتساب المحدث
MY_PHONE = '201140395791'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
    name = request.form['name']
    phone = request.form['phone']
    
    # 1. إرسال الطلب للبوت على تليجرام
    message_tg = f"طلب جديد من موقع شركة أبو قلص:%0Aالاسم: {name}%0Aالهاتف: {phone}"
    url_tg = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message_tg}"
    try:
        import requests
        requests.get(url_tg)
    except:
        pass # إذا حدث خطأ في البوت، استمر ولن يتوقف الموقع
    
    # 2. تجهيز رابط الواتساب وتوجيه العميل
    message_wa = f"أهلاً، أرغب في طلب خدمة من موقع شركة أبو قلص:%0Aالاسم: {name}%0Aالهاتف: {phone}"
    whatsapp_url = f"https://wa.me/{MY_PHONE}?text={message_wa}"
    
    return redirect(whatsapp_url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

