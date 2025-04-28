import os
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode


TOKEN = '7774939080:AAH4BB8qhexRBNK7h5aRRyVNn08YeWiSYO0'
WEATHER_API_KEY = 'd13df17617fb572a9b47fa839e1ae33a'

bot = Bot(TOKEN)
dp = Dispatcher()


async def get_weather(city: str) -> str:
    try:
        api_key = WEATHER_API_KEY
        if not api_key:
            return "Ошибка: API-ключ не найден."

        city_encoded = city.strip().replace(" ", "%20")
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_encoded}&appid={api_key}&units=metric&lang=ru"

        response = requests.get(url)
        data = response.json()

        print("Ответ API:", data)  # Для отладки (удалите в продакшене)

        if "cod" in data and data["cod"] == 200:
            weather = (
                f"🌤 Погода в {data['name']}:\n"
                f"➡ {data['weather'][0]['description'].capitalize()}\n"
                f"🌡 {data['main']['temp']}°C (ощущается как {data['main']['feels_like']}°C)\n"
                f"💧 Влажность: {data['main']['humidity']}%\n"
                f"🌬 Ветер: {data['wind']['speed']} м/с"
            )
            return weather
        else:
            error_msg = data.get("message", "Неизвестная ошибка API")
            return f"Ошибка: {error_msg}. Пример запроса: 'Москва' или 'New York'"

    except Exception as e:
        print("Ошибка в get_weather:", e)
        return "Сервис погоды временно недоступен."


@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer(
        "Привет! Я бот, который показывает погоду.\n"
        "Просто отправь мне название города, и я пришлю текущий прогноз погоды."
    )


@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "Как пользоваться ботом:\n"
        "1. Просто отправьте название города (например, Москва)\n"
        "2. Бот вернет текущую погоду в этом городе\n\n"
        "Команды:\n"
        "/start - начать работу с ботом\n"
        "/help - получить справку"
    )


@dp.message()
async def get_city_weather(message: Message):
    city = message.text
    weather = await get_weather(city)
    await message.answer(weather, parse_mode=ParseMode.MARKDOWN)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())