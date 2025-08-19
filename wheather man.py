import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# OpenWeatherMap API Key
API_KEY = "17466b816afd720d69d8ca7d93de3471"  # اینجا کلید واقعی OpenWeatherMap رو بذار
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
BOT_TOKEN = "7435287521:AAFVhd9Z3tBkM7S-uP1vCbphtBEITOmz5qs"  # توکن رباتت که از BotFather گرفتی

# تابع گرفتن اطلاعات آب‌وهوا
def get_weather(city_name):
    complete_url = f"{BASE_URL}appid={API_KEY}&q={city_name}&units=metric"
    response = requests.get(complete_url)

    if response.status_code == 200:
        data = response.json()
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        cloud_coverage = data["clouds"]["all"]

        weather_info = (f"🌡️ Temperature: {temperature}°C\n"
                        f"💧 Humidity: {humidity}%\n"
                        f"☁️ Cloud Coverage: {cloud_coverage}%")
        return weather_info
    else:
        return "City not found or API request failed!"

# تابع خوشامدگویی برای دستور /start
def start(update: Update, context: CallbackContext):
    keyboard = [["Send City Name"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text("Hi welcome to Weather Man! Please enter the city name.", reply_markup=reply_markup)

# تابع مدیریت پیام‌های کاربر
def handle_message(update: Update, context: CallbackContext):
    city_name = update.message.text.strip()
    if not city_name or city_name == "Send City Name":
        update.message.reply_text("Please enter a valid city name!")
        return

    weather_info = get_weather(city_name)
    update.message.reply_text(weather_info)

# تابع اصلی
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # اضافه کردن هندلرها
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # شروع ربات
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()