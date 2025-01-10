from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests

OWM_API_KEY = "38ca48c0966459cb26384fd8e3b549c4"
TELEGRAM_TOKEN = "8110024487:AAFVbx6oqPfF4NELDU4vWHnp9K7Nb24-WEQ"

def get_weather(city: str):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=uk&appid={OWM_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        city_name = data["name"]
        temp = data["main"]["temp"]
        weather_desc = data["weather"][0]["description"]
        return f"Погода в {city_name}: {temp}°C, {weather_desc.capitalize()}"
    else:
        return "Не вдалося знайти інформацію про погоду. Перевірте назву міста."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("Передати геопозицію", request_location=True)],
        [KeyboardButton("Ввести місто вручну")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Привіт! Виберіть опцію:", reply_markup=reply_markup)

async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location = update.message.location
    lat = location.latitude
    lon = location.longitude
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&lang=uk&appid={OWM_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        city_name = data["name"]
        temp = data["main"]["temp"]
        weather_desc = data["weather"][0]["description"]
        await update.message.reply_text(f"Погода в {city_name}: {temp}°C, {weather_desc.capitalize()}")
    else:
        await update.message.reply_text("Не вдалося отримати погоду за вашою геопозицією.")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = update.message.text
    weather = get_weather(city)
    await update.message.reply_text(weather)

def main():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.LOCATION, handle_location))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    application.run_polling()

if __name__ == "__main__":
    main()
