import logging
import subprocess #Чтобы взаимодействовать с bash консолью линукса
from aiogram import Bot, Dispatcher, executor, types
import random, os

API_TOKEN = '6070379081:AAGrYcJlgTrVuoVAeRJjvHZjPwbxqSjfvJI' #тестить здесь @PrjctServerControllerBot

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

BASE_PATH = "/home/ureshipan/Yandex.Disk/Color_Study"

#backupnumber =
# Пример функции, которая обрабатывает команды
@dp.message_handler()
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Привет! Это бот Color Study для сбора информации")
    startkeyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)#Объявляем варианты ответов для кнопок
    buttons = ['/start','/about']
    startkeyboard.add(*buttons)  # Заполняем варианты ответов, распаковывая массив с названиями кнопок
    await message.answer('Что бы вы хотели сделать?', reply_markup=startkeyboard)
    questionNumber = 0
    if message.text == '/start':
        picker = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ['Симметрия','Динамика','Колористика','Отвечу на все']
        picker.add(*buttons)
        await message.answer('Что бы вы не хотели оценивать?', reply_markup=picker)
        return message.text,questionNumber
    elif message.text == '/about':
        await message.answer('*Что-то о Color Study*', reply_markup=startkeyboard)



@dp.message_handler()
async def PhotoSender(message: types.Message):
        photo = open(random.choice([x for x in os.listdir("*Сюда написать путь*")if os.path.isfile(x)]), 'rb')
        await bot.send_photo(chat_id = message.chat_id, photo=photo)



'''
@dp.message_handler(commands=['backup_cur'])
async def backup(message: types.Message):
    subprocess.call("rm -rf " + BASE_PATH + "/Backup/*", shell=True) #Чистим папку
    subprocess.call("cp -a " + BASE_PATH + "/Current_Run/* " + BASE_PATH + "/Backup/", shell=True) #Кидаем текущую версию в бек
    #Буквально пишем баш команды через интерфейс этой библы

@dp.message_handler(commands=['update'])
async def update(message: types.Message):
    subprocess.call("rm -rf " + BASE_PATH + "/Current_Run/*", shell=True) #Чистим папку
    subprocess.call("cp -a " + BASE_PATH + "/Newest/* " + BASE_PATH + "/Current_Run/", shell=True) #Обновляем текущую версию в Current run


# Пример функции, которая принимает любой текст и отправляет его же собеседнику
@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)
'''

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)