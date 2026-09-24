import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "8986124658:AAEHNiey_GDxU-Z3CQKg6_rP0vVZdZZhuQY"
QR_CODE_URL = "https://i.ibb.co/68032549/image.jpg"

if not os.path.exists('screenshots'):
    os.makedirs('screenshots')

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start_cmd(message):
    pricing_text = (
        "👋 **Welcome! Hamare Services & Rates:**\n\n"
        "🎥 **2 Min Video** — ₹150\n"
        "🎥 **5 Min Video** — ₹300\n"
        "🎥 **10 Min Video** — ₹500\n"
        "📞 **WhatsApp Number with VC** — ₹700\n\n"
        "⚡ *Pay and send screenshot to receive service instantly!*\n\n"
        "👇 Service lene ke liye niche button par click karein:"
    )
    
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("🎬 2 Min Video (₹150)", callback_data="buy_150")
    btn2 = InlineKeyboardButton("🎬 5 Min Video (₹300)", callback_data="buy_300")
    btn3 = InlineKeyboardButton("🎬 10 Min Video (₹500)", callback_data="buy_500")
    btn4 = InlineKeyboardButton("📞 WhatsApp VC (₹700)", callback_data="buy_700")
    
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    markup.add(btn4)
    
    bot.send_message(message.chat.id, pricing_text, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def send_paytm_qr(call):
    item_map = {
        "buy_150": ("2 Min Video", "₹150"),
        "buy_300": ("5 Min Video", "₹300"),
        "buy_500": ("10 Min Video", "₹500"),
        "buy_700": ("WhatsApp Number with VC", "₹700")
    }
    
    item_name, item_price = item_map.get(call.data, ("Service", "Amount"))
    
    caption = (
        f"📌 **Selected Service:** {item_name}\n"
        f"💰 **Price:** {item_price}\n\n"
        "1️⃣ Niche diye gaye Paytm QR Code ko scan karke payment karein.\n"
        "2️⃣ Payment hone ke baad **Payment Ka Screenshot** is chat me bhej dein."
    )
    
    bot.send_photo(call.message.chat.id, photo=QR_CODE_URL, caption=caption, parse_mode="Markdown")

@bot.message_handler(content_types=['photo'])
def handle_screenshot(message):
    user_id = message.chat.id
    username = message.from_user.username or message.from_user.first_name
    
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    file_name = f"screenshots/{user_id}_{username}.jpg"
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)
    
    bot.send_message(
        user_id, 
        "✅ **Payment Screenshot Receive Ho Gaya Hai!**\n\nAdmin jald hi verify karke aapko aapki service/content bhej denge. Dhanyawad!"
    )

bot.infinity_polling()
