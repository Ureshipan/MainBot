import logging
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.input_file import InputFile
import random
from bd_funcs import *

API_TOKEN = '6159808536:AAHsRPkSlKgsbPmLsTluqxX-hLHICo9p_dA'  # тестить здесь http://t.me/ColorStudyBot
BASE_PATH = "/home/ureshipan/Yandex.Disk/Color_Study"

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

users_data = {"id": {"ignore": "Composition", "position": 0, "pic_id": 0, "social_rate": 0}}  # Пример оформления

# with open('users_data.json') as json_file: #Загрузка из сейва
#   users_data = json.load(json_file)
#   json_file.close()


questions = {
    "Композиция": {"quest": "На данной картине композиция открытая или закрытая?", "buttons": ["Открытая", "Закрытая"]},
    "Динамика": {"quest": "На данной картине композиция динамическая или статическая?",
                 "buttons": ["Динамическая", "Статическая"]},
    "Метафора": {"quest": "На данной картине геометрические фигуры являются метафорой или сеткой?",
                 "buttons": ["Метафора", "Сетка"]},
    "Фотомонтаж": {"quest": "На данной картине присутствует фотомонтаж?", "buttons": ["Есть", "Отсутствует"]},
    "Симметрия": {"quest": "На данной картине присутствует симметрия?","buttons": ["Есть","Отсутствует"]},
    "Контраст Направлений": {"quest": "На данной картине присутствует контраст направлений?","buttons": ["Есть","Отсутствует"]},
    "Контраст Цветов": {"quest": "На данной картине присутствует контраст цветов?","buttons": ["Есть","Отсутствует"]},
    "Контраст Форм": {"quest": "На данной картине присутствует контраст форм?","buttons": ["Есть","Отсутствует"]},
    "Контраст Размеров": {"quest": "На данной картине присутствует контраст размеров?","buttons": ["Есть","Отсутствует"]},
    "Палитра": {"quest": "Какая палитра на данной картине?","buttons": ["Контрастная","Монохромная"]}}


# Пример функции, которая обрабатывает команды
#Это временные переменные, которые идут в БД
Dinam = ""
Metaf = ""
Photos = ""
Simm = ""
ContrastA = ""
ContrastB = ""
ContrastC = ""
ContrastD = ""
Poll = ""
Compos = "Закрытая"
#Дополнил тем, что в зависимости от шага, временные данные меняются
def save_ans(pic_id, param, mean):
    print(pic_id, param, mean)
    if(pic_id == 2):
        Dinam = mean
    elif(pic_id == 3):
        Metaf = mean
    elif(pic_id == 4):
        Photos = 0
    elif(pic_id == 5):
        Simm = 0
    elif(pic_id == 6):
        ContrastA = 0
    elif(pic_id == 7):
        ContrastB = 0
    elif (pic_id == 8):
        ContrastC = 0
    elif(pic_id == 9):
        ContrastD = 0
    elif (pic_id == 10):
        Poll = 0


def continu(pos, ignore):
    print(pos, end="->")
    pos += 1
    # print(list(questions.keys()), len(list(questions.keys())), pos)
    if pos == len(list(questions.keys())) + 1:
        pos = 0
        # print(pos)
    elif list(questions.keys())[pos - 1] == ignore:
        pos += 1
    print(pos)
    return pos


@dp.message_handler()
async def send_welcome(message: types.Message):
    global users_data
    skip = True
    boolans = 0
    startkeyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)  # Объявляем варианты ответов для кнопок
    buttons = ['Начать опрос', 'О проекте']
    startkeyboard.add(*buttons)  # Заполняем варианты ответов, распаковывая массив с названиями кнопок
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    if message.text == "/start":
        if get_user(message.from_user.id) == "No":
            users_data[message.from_user.id] = {"ignore": "Отвечу на всё", "qualification": "1-2 курс", "position": -2,
                                                "pic_id": -1, "social_rate": 0, "answers": {"Композиция": 2,
                                                                                            "Динамика": 2,
                                                                                            "Метафора": 2,
                                                                                            "Фотомонтаж": 2,
                                                                                            "Симметрия": 2,
                                                                                            "Контраст Направлений": 2,
                                                                                            "Контраст Цветов": 2,
                                                                                            "Контраст Форм": 2,
                                                                                            "Контраст Размеров": 2,
                                                                                            "Палитра": 2}
                                                }
            new_user(message.from_user.id, 1, "Отвечу на всё")
        else:
            data = get_user(message.from_user.id)
            users_data[message.from_user.id] = {"ignore": data[2],
                                                "qualification": data[1],
                                                "position": data[3],
                                                "pic_id": -1,
                                                "social_rate": data[4],
                                                "answers": {}}
        await message.answer("Привет! Это бот Color Study для сбора информации")

        await message.answer('Что бы вы хотели сделать?', reply_markup=startkeyboard)
    elif users_data[message.from_user.id]["position"] == -2 and message.text != 'О проекте':
        picker = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # buttons = list(questions.keys()) + ["Отвечу на всё"]
        buttons = ["1-2 курс", "3-4 курс", "Искуствовед"]
        picker.add(*buttons)
        if message.text in buttons:
            users_data[message.from_user.id]["qualification"] = message.text
            users_data[message.from_user.id]["position"] = continu(-2, users_data[message.from_user.id]["ignore"])
        else:
            await message.answer('Кем вы являетесь на данный момент? (это нужно только для правильной статистики, '
                                 'полагаемся на вашу честность)', reply_markup=picker)

    if users_data[message.from_user.id]["position"] == -1 and message.text != 'О проекте':
        picker = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = list(questions.keys()) + ["Отвечу на всё"]
        picker.add(*buttons)
        if message.text in buttons:
            users_data[message.from_user.id]["ignore"] = message.text
            users_data[message.from_user.id]["position"] = continu(-1, users_data[message.from_user.id]["ignore"])
        else:
            await message.answer('На вопросы по какой теме вы бы не хотели отвечать? '
                                 '(в чём не уверены, что можете дать правильный ответ)', reply_markup=picker)
        # return message.text
    elif message.text == 'О проекте':
        await message.answer('*Что-то о Color Study*', reply_markup=startkeyboard)

    # Отправка изображения и первый вопрос юзеру. В обработчике следующего вопроса нужно сделать проверку
    # корректности ответа на первый, если первый вопрос вообще задаётся и собственно задать следующий вопрос.
    # contin делать только если ответ на предыдущий вопрос корректен
    if users_data[message.from_user.id]["position"] == 0 and message.text != "Нет":
        pic = InputFile(
            'test_images/' + random.choice([x for x in os.scandir("test_images/") if os.path.isfile(x)]).name)
        # contin = True
        users_data[message.from_user.id]["position"] = continu(0, users_data[message.from_user.id]["ignore"])
        pic = get_next_pic(message.from_user.id)
        users_data[message.from_user.id]["pic_id"] = pic[0]
        await message.answer_photo(photo=pic[-1], caption=pic[1]+" \""+pic[2]+"\" "+str(pic[3]))

        # await message.reply(random.choice([x for x in os.scandir("test_images/")if os.path.isfile(x)]).name)

    if users_data[message.from_user.id]["position"] == 1:
        if message.text in questions["Композиция"]["buttons"]:
            # contin = True
            if message.text == "Открытая":
                boolans = 1
            else:
                boolans = 0
            users_data[message.from_user.id]["answers"]["Композиция"] = boolans
            users_data[message.from_user.id]["position"] = continu(users_data[message.from_user.id]["position"],
                                                                   users_data[message.from_user.id]["ignore"])
        elif message.text == "Пропустить" and skip:
            skip = False
            users_data[message.from_user.id]["position"] = continu(users_data[message.from_user.id]["position"],
                                                                   users_data[message.from_user.id]["ignore"])
        else:
            skip = True
            await message.answer(questions["Композиция"]["quest"],
                                 reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(
                                     *questions["Композиция"]["buttons"] + ["Пропустить"]))

    if users_data[message.from_user.id]["position"] == 2:
        if message.text in questions["Динамика"]["buttons"]:
            if message.text == "Динамическая":
                boolans = 1
            else:
                boolans = 0
            users_data[message.from_user.id]["answers"]["Динамика"] = boolans
            users_data[message.from_user.id]["position"] = continu(users_data[message.from_user.id]["position"],
                                                                   users_data[message.from_user.id]["ignore"])
        elif message.text == "Пропустить" and skip:
            skip = False
            users_data[message.from_user.id]["position"] = continu(users_data[message.from_user.id]["position"],
                                                                   users_data[message.from_user.id]["ignore"])
        else:
            skip = True
            await message.answer(questions["Динамика"]["quest"],
                                 reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(
                                     *questions["Динамика"]["buttons"] + ["Пропустить"]))

    if users_data[message.from_user.id]["position"] == 3:
        if message.text in questions["Метафора"]["buttons"]:
            if message.text == "Метафора":
                boolans = 1
            else:
                boolans = 0
            users_data[message.from_user.id]["answers"]["Метафора"] = boolans
            users_data[message.from_user.id]["position"] = continu(users_data[message.from_user.id]["position"],
                                                                   users_data[message.from_user.id]["ignore"])
        elif message.text == "Пропустить" and skip:
            skip = False
            users_data[message.from_user.id]["position"] = continu(users_data[message.from_user.id]["position"],
                                                                   users_data[message.from_user.id]["ignore"])
        else:
            skip = True
            await message.answer(questions["Метафора"]["quest"],
                                 reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(
                                     *questions["Метафора"]["buttons"] + ["Пропустить"]))

    if users_data[message.from_user.id]["position"] == 4:
        if message.text in questions["Фотомонтаж"]["buttons"]:
            if message.text == "Есть":
                boolans = 1
            else:
                boolans = 0
            users_data[message.from_user.id]["answers"]["Фотомонтаж"] = boolans
            users_data[message.from_user.id]["position"] = continu(users_data[message.from_user.id]["position"],
                                                                   users_data[message.from_user.id]["ignore"])
            # Рестарт опроса ******************* Необходимо переносить в последний из существующих обработчиков вопросов
            # ****************************************************
        elif message.text == "Пропустить" and skip:
            skip = False
            users_data[message.from_user.id]["position"] = continu(users_data[message.from_user.id]["position"],
                                                                   users_data[message.from_user.id]["ignore"])
        else:
            skip = True
            await message.answer(questions["Фотомонтаж"]["quest"],
                                 reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(
                                     *questions["Фотомонтаж"]["buttons"] + ["Пропустить"]))

    if users_data[message.from_user.id]["position"] == 5:
        if message.text in questions["Симметрия"]["buttons"]:
            if message.text == "Есть":
                boolans = 1
            else:
                boolans = 0
            users_data[message.from_user.id]["answers"]["Симметрия"] = boolans
            users_data[message.from_user.id]["position"] = continu(users_data[message.from_user.id]["position"],
                                                                   users_data[message.from_user.id]["ignore"])
            # Рестарт опроса ******************* Необходимо переносить в последний из существующих обработчиков вопросов

            # ****************************************************
        elif message.text == "Пропустить" and skip:
            skip = False
            users_data[message.from_user.id]["position"] = continu(users_data[message.from_user.id]["position"],
                                                                   users_data[message.from_user.id]["ignore"])
        else:
            skip = True
            await message.answer(questions["Симметрия"]["quest"],
                                 reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(
                                     *questions["Симметрия"]["buttons"] + ["Пропустить"]))
    if users_data[message.from_user.id]["position"] == 6:
        if message.text in questions["Контраст Направлений"]["buttons"]:
            if message.text == "Есть":
                boolans = 1
            else:
                boolans = 0
            users_data[message.from_user.id]["answers"]["Контраст Направлений"] = boolans
            users_data[message.from_user.id]["position"] = continu(users_data[message.from_user.id]["position"],
                                                                   users_data[message.from_user.id]["ignore"])
            # Рестарт опроса ******************* Необходимо переносить в последний из существующих обработчиков вопросов
            # ****************************************************
        elif message.text == "Пропустить" and skip:
            skip = False
            users_data[message.from_user.id]["position"] = continu(users_data[message.from_user.id]["position"],
                                                                   users_data[message.from_user.id]["ignore"])
        else:
            skip = True
            await message.answer(questions["Контраст Направлений"]["quest"],
                                 reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(
                                     *questions["Контраст Направлений"]["buttons"] + ["Пропустить"]))
    if users_data[message.from_user.id]["position"] == 7:
        if message.text in questions["Контраст Форм"]["buttons"]:
            if message.text == "Есть":
                boolans = 1
            else:
                boolans = 0
            users_data[message.from_user.id]["answers"]["Контраст Форм"] = boolans
            users_data[message.from_user.id]["position"] = continu(users_data[message.from_user.id]["position"],
                                                                   users_data[message.from_user.id]["ignore"])
            # Рестарт опроса ******************* Необходимо переносить в последний из существующих обработчиков вопросов
            # ****************************************************
        elif message.text == "Пропустить" and skip:
            skip = False
            users_data[message.from_user.id]["position"] = continu(users_data[message.from_user.id]["position"],
                                                                   users_data[message.from_user.id]["ignore"])
        else:
            skip = True
            await message.answer(questions["Контраст Форм"]["quest"],
                                 reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(
                                     *questions["Контраст Форм"]["buttons"] + ["Пропустить"]))
    if users_data[message.from_user.id]["position"] == 8:
        if message.text in questions["Контраст Цветов"]["buttons"]:
            if message.text == "Есть":
                boolans = 1
            else:
                boolans = 0
            users_data[message.from_user.id]["answers"]["Контраст Цветов"] = boolans
            users_data[message.from_user.id]["position"] = continu(users_data[message.from_user.id]["position"],
                                                                   users_data[message.from_user.id]["ignore"])
            # Рестарт опроса ******************* Необходимо переносить в последний из существующих обработчиков вопросов
            # ****************************************************
        elif message.text == "Пропустить" and skip:
            skip = False
            users_data[message.from_user.id]["position"] = continu(users_data[message.from_user.id]["position"],
                                                                   users_data[message.from_user.id]["ignore"])
        else:
            skip = True
            await message.answer(questions["Контраст Цветов"]["quest"],
                                 reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(
                                     *questions["Контраст Цветов"]["buttons"] + ["Пропустить"]))
    if users_data[message.from_user.id]["position"] == 9:
        if message.text in questions["Контраст Размеров"]["buttons"]:
            if message.text == "Есть":
                boolans = 1
            else:
                boolans = 0
            users_data[message.from_user.id]["answers"]["Контраст Размеров"] = boolans
            users_data[message.from_user.id]["position"] = continu(users_data[message.from_user.id]["position"],
                                                                   users_data[message.from_user.id]["ignore"])
            # Рестарт опроса ******************* Необходимо переносить в последний из существующих обработчиков вопросов
            # ****************************************************
        elif message.text == "Пропустить" and skip:
            skip = False
            users_data[message.from_user.id]["position"] = continu(users_data[message.from_user.id]["position"],
                                                                   users_data[message.from_user.id]["ignore"])
        else:
            skip = True
            await message.answer(questions["Контраст Размеров"]["quest"],
                                 reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(
                                     *questions["Контраст Размеров"]["buttons"] + ["Пропустить"]))
    if users_data[message.from_user.id]["position"] == 10:
        if message.text in questions["Палитра"]["buttons"]:
            if message.text == "Контрастная":
                boolans = 1
            else:
                boolans = 0
            users_data[message.from_user.id]["answers"]["Палитра"] = boolans
            users_data[message.from_user.id]["position"] = continu(users_data[message.from_user.id]["position"],
                                                                   users_data[message.from_user.id]["ignore"])
            # Рестарт опроса ******************* Необходимо переносить в последний из существующих обработчиков вопросов
            picker = types.ReplyKeyboardMarkup(resize_keyboard=True)
            buttons = ["Да", "Нет"]
            picker.add(*buttons)
            # skip = True
            await message.answer('Спасибо, ваши ответы записаны. Хотите продолжить?', reply_markup=picker)
            ResultUserOpros(message.from_user.id, users_data[message.from_user.id]["pic_id"], users_data[message.from_user.id]["answers"]) #Функция, которая записывает наши ответы
            # ****************************************************

        elif message.text == "Пропустить" and skip:
            picker = types.ReplyKeyboardMarkup(resize_keyboard=True)
            buttons = ["Да", "Нет"]
            picker.add(*buttons)
            # skip = True
            await message.answer('Спасибо, ваши ответы записаны. Хотите продолжить?', reply_markup=picker)
            users_data[message.from_user.id]["position"] = continu(users_data[message.from_user.id]["position"],
                                                                   users_data[message.from_user.id]["ignore"])
        else:
            skip = True
            await message.answer(questions["Палитра"]["quest"],
                                 reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(
                                     *questions["Палитра"]["buttons"] + ["Пропустить"]))


def control():
    while True:
        command = input()
        if command == "Save":
            print("saving...")
            for user_id in users_data.keys():
                update_pos(user_id, users_data[user_id]["position"])
            print("done!")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
