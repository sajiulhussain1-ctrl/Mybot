import os
import telebot
import requests
from io import BytesIO
from flask import Flask
from threading import Thread
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is 24/7 Active & Alive!"

@app.route('/health')
def health():
    return "OK", 200

# Bot Credentials & Settings
BOT_TOKEN = "8838547784:AAGLp823nS_JpgVjbSHnOBmQUuFQ_mmMSKc"
ADMIN_ID = 8871839919
UPI_ID = "paytmqr5ijy2n@ptys"

START_PHOTOS = [
    "AgACAgUAAxkBAAM9arY0RSMLm_ceAhQLTtkl67RmHVQAAnYRaxvRprBVNfoyGs0zCpYBAAMCAAN4AAM9BA",
    "AgACAgUAAxkBAAM3arYzmwYknDv6zsIiT3c0KD5f844AAnQRaxvRprBVVpvbLoUMSWIBAAMCAAN4AAM9BA",
    "AgACAgUAAxkBAANBarY0T7yDAAGC_OrWBuG13FsfpC-FAAJ3EWsb0aawVSlICQq9dJuJAQADAgADeAADPQQ",
    "AgACAgUAAxkBAANDarY0VUamO1E7Z-fHtJG8mtLXsbcAAngRaxvRprBVrD-Ac9UBf1QBAAMCAAN4AAM9BA",
    "AgACAgUAAxkBAANFarY0V90s50KM8xU4IE8v2efwS1QAAnkRaxvRprBV1HYT58Mm_mABAAMCAAN4AAM9BA"
]

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start_cmd(message):
    user = message.from_user
    username = f"@{user.username}" if user.username else "No Username"
    
    admin_alert = (
        f"👤 <b>New User Visit!</b>\n\n"
        f"• <b>Name:</b> {user.first_name}\n"
        f"• <b>Username:</b> {username}\n"
        f"• <b>User ID:</b> <code>{user.id}</code>"
    )
    try:
        bot.send_message(ADMIN_ID, admin_alert, parse_mode="HTML")
    except Exception as e:
        print("Admin alert error:", e)

    try:
        media_group = [InputMediaPhoto(photo_id) for photo_id in START_PHOTOS]
        bot.send_media_group(message.chat.id, media_group)
    except Exception as e:
        print("Media group send error:", e)

    pricing_text = (
        "<b>✨ Welcome to Taniya Exclusive Service ✨</b>\n\n"
        "🔥 <b>Available Rates & Packages:</b>\n\n"
        "📹 <b>2 Min Open Video:</b> ₹150\n"
        "📹 <b>5 Min Open Video:</b> ₹300\n"
        "👩‍🦰 <b>10 Min Video (With Face):</b> ₹500\n"
        "📞 <b>WhatsApp Video Call (VC):</b> ₹700\n\n"
        "👇 <b>Payment karne ke liye niche 'Pay Now / Scan QR' button par click karein!</b>"
    )
    
    markup = InlineKeyboardMarkup()
    btn_pay = InlineKeyboardButton("💳 Pay Now / Scan QR", callback_data="pay_qr")
    markup.add(btn_pay)
    
    bot.send_message(message.chat.id, pricing_text, parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "pay_qr")
def send_qr_code(call):
    try:
        bot.answer_callback_query(call.id, text="Generating QR Code...")
        user_id = call.from_user.id
        
        # Image bytes fetch using requests
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=upi://pay?pa={UPI_ID}%26pn=Taniya%20Service"
        res = requests.get(qr_url)
        
        payment_info = (
            "📌 <b>Payment Details & QR Code:</b>\n\n"
            f"👉 <b>UPI ID:</b> <code>{UPI_ID}</code>\n\n"
            "1️⃣ Upar dikh rahe QR Code ko Kisi bhi App (PhonePe, Paytm, GooglePay) se scan karein.\n"
            "2️⃣ Ya direct UPI ID copy karke pay karein.\n"
            "3️⃣ Payment complete hone ke baad screenshot yahan bhejein! ✅"
        )
        
        if res.status_code == 200:
            qr_file = BytesIO(res.content)
            qr_file.name = 'qr.png'
            bot.send_photo(user_id, photo=qr_file, caption=payment_info, parse_mode="HTML")
        else:
            bot.send_message(user_id, payment_info, parse_mode="HTML")

    except Exception as e:
        print("Error sending QR:", e)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    user = message.from_user
    username = f"@{user.username}" if user.username else "No Username"
    photo_file_id = message.photo[-1].file_id

    caption = (
        f"🚨 <b>NEW PAYMENT SCREENSHOT RECEIVED!</b> 🚨\n\n"
        f"• <b>From User:</b> {user.first_name}\n"
        f"• <b>Username:</b> {username}\n"
        f"• <b>User ID:</b> <code>{user.id}</code>"
    )
    
    try:
        bot.send_photo(ADMIN_ID, photo=photo_file_id, caption=caption, parse_mode="HTML")
    except Exception as e:
        print("Failed to send screenshot to admin:", e)

    bot.reply_to(message, "✅ <b>Payment Screenshot Received!</b>\nHum aapka payment verify kar rahe hain. Aapki service instant receive ho jayegi.", parse_mode="HTML")

def run_flask():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    Thread(target=run_flask, daemon=True).start()
    bot.infinity_polling(timeout=20, long_polling_timeout=10)
