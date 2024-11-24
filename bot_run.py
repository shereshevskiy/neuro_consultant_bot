"""telegram bot."""


import json
import os
from pathlib import Path

import aiohttp
import openai
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# подгружаем переменные окружения
load_dotenv()

ROOT_DIR_LESSON14 = Path(os.path.dirname(os.path.abspath(__file__)))

# передаем секретные данные в переменные
TOKEN = os.environ.get("TG_TOKEN")
GPT_SECRET_KEY = os.environ.get("GPT_SECRET_KEY")

# передаем секретный токен chatgpt
openai.api_key = GPT_SECRET_KEY


# функция для синхронного общения с chatgpt
async def get_answer(text):
    payload = {"text":text}
    response = requests.post("http://127.0.0.1:5000/api/get_answer", json=payload)
    return response.json()


# функция для асинхронного общения с сhatgpt
async def get_answer_async(text):
    payload = {"text":text}
    async with aiohttp.ClientSession() as session:
        async with session.post('http://127.0.0.1:5000/api/get_answer_async', json=payload) as resp:
            return await resp.json()


# функция-обработчик команды /start 
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # при первом запуске бота добавляем этого пользователя в словарь
    if update.message.from_user.id not in context.bot_data.keys():
        context.bot_data[update.message.from_user.id] = {}
        context.bot_data[update.message.from_user.id]["requests"] = 3  # добавляем число запросов
        context.bot_data[update.message.from_user.id]["story"] = []  # добавляем хранилище для истории запросов
    
    # возвращаем текстовое сообщение пользователю
    await update.message.reply_text('Задайте любой вопрос ChatGPT')


# функция-обработчик команды /data 
async def data(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # создаем json и сохраняем в него словарь context.bot_data
    with open(ROOT_DIR_LESSON14/'data.json', 'w') as fp:
        json.dump(context.bot_data, fp)
    
    # возвращаем текстовое сообщение пользователю
    await update.message.reply_text('Данные сгружены')


# функция-обработчик текстовых сообщений
async def text(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # проверка доступных запросов пользователя
    if context.bot_data[update.message.from_user.id]["requests"] > 0:

        # формируе текст запроса из текущего запроса и истории запросов
        ask = update.message.text
        if context.bot_data[update.message.from_user.id]["story"]:
            ask = f"Текущий вопрос - {ask}. История предыдущих запросов, начиная с более раннего запроса - {'; '.join(context.bot_data[update.message.from_user.id]['story'])}"
        # print(ask)
        
        # выполнение запроса в chatgpt
        first_message = await update.message.reply_text('Ваш запрос обрабатывается, пожалуйста подождите...')
        # res = await get_answer(ask)  # запуск в синхронном режиме
        res = await get_answer_async(ask)  # запуск в асинхронном режиме
        await context.bot.edit_message_text(text=res['message'], chat_id=update.message.chat_id, message_id=first_message.message_id)

        # уменьшаем количество доступных запросов на 1
        context.bot_data[update.message.from_user.id]["requests"] -= 1
        await update.message.reply_text(f'Осталось запросов: {context.bot_data[update.message.from_user.id]["requests"]}')
        
        # сохраняем запрос в историю и оставляем 5 последних
        ask_and_answer = f"вопрос: {update.message.text}, ответ: {res['message']}"
        context.bot_data[update.message.from_user.id]["story"].append(ask_and_answer)
        context.bot_data[update.message.from_user.id]["story"] = context.bot_data[update.message.from_user.id]["story"][-5:]
    
    else:

        # сообщение если запросы исчерпаны
        await update.message.reply_text('Ваши запросы на сегодня исчерпаны')


# функция, которая будет запускаться раз в сутки для обновления доступных запросов
async def callback_daily(context: ContextTypes.DEFAULT_TYPE):

    # проверка базы пользователей
    if context.bot_data != {}:

        # проходим по всем пользователям в базе и обновляем их доступные запросы
        for key in context.bot_data:
            context.bot_data[key]["requests"] = 5
        print('Запросы пользователей обновлены')
    else:
        print('Не найдено ни одного пользователя')


def main():

    # создаем приложение и передаем в него токен бота
    application = Application.builder().token(TOKEN).build()
    print('Бот запущен...')

    # создаем job_queue 
    job_queue = application.job_queue
    job_queue.run_repeating(callback_daily, # функция обновления базы запросов пользователей
                            interval=60,    # интервал запуска функции (в секундах)
                            first=60)       # первый запуск функции (через сколько секунд)

    # добавление обработчиков
    application.add_handler(CommandHandler("start", start, block=False))
    application.add_handler(CommandHandler("data", data, block=False))
    application.add_handler(MessageHandler(filters.TEXT, text, block=False))

    # запуск бота (нажать Ctrl+C для остановки)
    application.run_polling()
    print('Бот остановлен')


if __name__ == "__main__":
    main()
