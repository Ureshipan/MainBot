import logging
import os
import json
import subprocess #Чтобы взаимодействовать с bash консолью линукса
from aiogram import Bot, Dispatcher, executor, types
import random, os

API_TOKEN = '6070379081:AAGrYcJlgTrVuoVAeRJjvHZjPwbxqSjfvJI' #тестить здесь @PrjctServerControllerBot
BASE_PATH = "/home/ureshipan/Yandex.Disk/Color_Study"

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


# users_data = { "id" : {"ignore" : "Composition", "position" : 0, "pic_id" : 0, "social_rate" : 0}} #Пример оформления

with open('users_data.json') as json_file: #Загрузка из сейва
    users_data = json.load(json_file)
    json_file.close()


questions = { "Name" : "What on the picture?"}
# Пример функции, которая обрабатывает команды
@dp.message_handler()
async def send_welcome(message: types.Message):
    global users_data
    contin = False
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Привет! Это бот Color Study для сбора информации")
    startkeyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)#Объявляем варианты ответов для кнопок
    buttons = ['/start','/about']
    startkeyboard.add(*buttons)  # Заполняем варианты ответов, распаковывая массив с названиями кнопок
    await message.answer('Что бы вы хотели сделать?', reply_markup=startkeyboard)
    if message.text == '/start':

        if message.from_user.id not in users_data.keys():
            users_data[message.from_user.id] = {"ignore": "Отвечу на всё", "position": 0, "pic_id": -1, "social_rate": 0}
            with open('users_data.json') as json_file:     #Добавление юзера в локальный словарь если его нет и перезапись сейва
                json.dump(users_data, json_file)
                json_file.close()

        picker = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ['Симметрия', 'Динамика', 'Колористика', 'Отвечу на все']
        picker.add(*buttons)
        await message.answer('Что бы вы не хотели оценивать?', reply_markup=picker)
        return message.text
    elif message.text == '/about':
        await message.answer('*Что-то о Color Study*', reply_markup=startkeyboard)

    # Отправка изображения и первый вопрос юзеру. В обработчике следующего вопроса нужно сделать проверку
    # корректности ответа на первый, если первый вопрос вообще задаётся и собственно задать следующий вопрос.
    # contin делать только если ответ на предыдущий вопрос корректен
    elif users_data[message.from_user.id]["position"] == 0:
        await message.reply_photo(open(random.choice([x for x in os.listdir(BASE_PATH + "test_images/")if os.path.isfile(x)]), 'rb'), caption="Автор, название, год")
        if users_data[message.from_user.id]["ignore"] != "Открытая композиция":
            await message.reply(questions["Открытая композиция"])
        contin = True

    # Здесь обработчики всех остальных вопросов по образцу но ещё и с проверкой

    if contin: # Продвижение прогресса пользователя в прогрессе с учётом избегаемых тем
        users_data[message.from_user.id]["position"] += 1
        if users_data[message.from_user.id]["position"] == len(questions.keys()):
            users_data[message.from_user.id]["position"] = 0
        if questions.keys[users_data[message.from_user.id]["position"]] == users_data[message.from_user.id]["ignore"]:
            users_data[message.from_user.id]["position"] += 1






'''
@dp.message_handler()
async def PhotoSender(message: types.Message):
        photo = open(random.choice([x for x in os.listdir("*Сюда написать путь*")if os.path.isfile(x)]), 'rb')
        await bot.send_photo(chat_id = message.chat_id, photo=photo)

@dp.message_handler(commands=['backup_cur'])
async def backup(message: types.Message):
    subprocess.call("rm -rf " + BASE_PATH + "/Backup/*", shell=True) #Чистим папку
    subprocess.call("cp -a " + BASE_PATH + "/Current_Run/* " + BASE_PATH + "/Backup/", shell=True) #Кидаем текущую версию в бек
    #Буквально пишем баш команды через интерфейс этой библы

@dp.message_handler(commands=['update'])
async def update(message: types.Message):
    subprocess.call("rm -rf " + BASE_PATH + "/Current_Run/*", shell=True) #Чистим папку
    subprocess.call("cp -a " + BASE_PATH + "/Newest/* " + BASE_PATH + "/Current_Run/", shell=True) #Обновляем текущую версию в Current run


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)
'''


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)