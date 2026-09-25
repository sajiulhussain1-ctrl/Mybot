import os
import telebot
from flask import Flask
from threading import Thread
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

Thread(target=run, daemon=True).start()

BOT_TOKEN = "8838547784:AAFYDcGPKNTaxkNdWWZ-lV-K0NhbbNGz56Q"

# Temporary links
QR_CODE_URL = "https://i.ibb.co/C0315k2/qr.png"
START_PHOTOS = [
    "https://i.ibb.co/LBWL674/image.jpg",
    "https://i.ibb.co/V0ht4ST/image.jpg",
    "https://i.ibb.co/HfH47ZT/image.jpg",
    "https://i.ibb.co/7dspqTH/image.jpg",
    "https://i.ibb.co/hxkBBHW/image.jpg"
]

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start_cmd(message):
    try:
        media_group = [InputMediaPhoto(url) for url in START_PHOTOS]
        bot.send_media_group(message.chat.id, media_group)
    except Exception as e:
        print("Media group error:", e)

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
    caption_text = (
        "📌 <b>Payment Details & Instructions:</b>\n\n"
        "1️⃣ <b>Option 1:</b> Upar diye gaye QR Code ko scan karke payment karein.\n"
        "2️⃣ <b>Option 2:</b> Direct UPI ID par pay karein:\n"
        "   • <b>UPI ID:</b> <code>mitali55@ptaxis</code>\n\n"
        "3️⃣ Payment complete hone ke baad screenshot is chat me bhejein.\n"
        "4️⃣ Screenshot milne ke baad aapki service instantly start kar di jayegi! ✅"
    )
    
    try:
        bot.send_photo(call.message.chat.id, photo=QR_CODE_URL, caption=caption_text, parse_mode="HTML")
    except Exception as e:
        fallback_text = (
            "📌 <b>Payment Details & Instructions:</b>\n\n"
            "👉 <b>UPI ID:</b> <code>mitali55@ptaxis</code>\n\n"
            "1️⃣ Upar di gayi UPI ID par payment karein.\n"
            "2️⃣ Payment complete hone ke baad screenshot is chat me bhejein.\n"
            "3️⃣ Screenshot milne ke baad aapki service instantly start kar di jayegi! ✅"
        )
        bot.send_message(call.message.chat.id, fallback_text, parse_mode="HTML")
        
    bot.answer_callback_query(call.id)

# HD Photo File ID Reply Handler
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_id = message.photo[-1].file_id
    bot.reply_to(message, f"<b>HD Photo ID:</b>\n<code>{file_id}</code>", parse_mode="HTML")

bot.infinity_polling(timeout=10, long_polling_timeout=5)
