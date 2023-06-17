import telebot
import requests
import config

WEATHER_API_TOKEN = "f5f5940d1f7998969493426b9fa05d86"
WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"

bot = telebot.TeleBot("6112407952:AAFS2xltekG6j4necBgeRn0nYVXYdDnZVnw")

def get_weather(city, API_KEY):
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
    URL = BASE_URL + "q=" + city + "&appid=" + API_KEY
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        temperature = int(data['main']['temp'] - 273.15)
        weather_desc = data['weather'][0]['description']
        wind_speed = data['wind']['speed']
        precipitation = data.get('rain', {}).get('1h', 0) + data.get('snow', {}).get('1h', 0)
        return temperature, weather_desc, wind_speed, precipitation
    else:
        print("Error in HTTP request")


@bot.message_handler(commands=['start'])
def start_message(message):
    msg = bot.reply_to(message, "Привіт! Я - бот, який показує поточну погоду \U0001F31E в місті.")
    bot.send_message(message.chat.id, "Введіть назву міста, щоб продовжити")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    city = message.text
    temperature, weather_desc, wind_speed, precipitation = get_weather(city, WEATHER_API_TOKEN)
    if temperature is not None:
        reply = f"Поточна погода в місті {city}:\n" \
                f"Температура: {temperature}°C\n" \
                f"Опис погоди: {weather_desc}\n" \
                f"Швидкість вітру: {wind_speed} м/с\n"
    else:
        reply = "Не вдалося отримати дані про погоду. Будь ласка, спробуйте ще раз."
    bot.reply_to(message, reply)
   bot.send_message(message.chat.id, "Введіть назву міста, щоб продовжити")
    bot.register_next_step_handler(msg, print_weather)

bot.polling()
