from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
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
        return "Не вдалося визначити погоду міста, перевірте назву міста"
    

def start(update: Update, context: CallbackContext):
    keyboard = [
        [KeyboardButton("Передати геопозицію", request_location=True)],
        [KeyboardButton("Ввести місто вручну")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text("Привіт! Виберіть опцію:", reply_markup=reply_markup)

def handle_location(update: Update, context: CallbackContext):
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
        update.message.reply_text(f"Погода в {city_name}: {temp}°C, {weather_desc.capitalize()}")
    else:
        update.message.reply_text("Не вдалося отримати погоду за вашою геопозицією.")