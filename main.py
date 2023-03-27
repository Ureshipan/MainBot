import logging
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.input_file import InputFile
import random

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
    "Метафоры": {"quest": "На данной картине геометрические фигуры являются метафорой или сеткой?",
                 "buttons": ["Метафора", "Сетка"]},
    "Фотомонтаж": {"quest": "На данной картине присутствует фотонмонтаж?", "buttons": ["Есть", "Отсутствует"]},
    "Симметрия": {"quest": "На данной картине присутствует симметрия?","buttons": ["Есть","Отсутствует"]},
    "Контраст_Направлений": {"quest": "На данной картине присутствует контраст направлений?","buttons": ["Есть","Отсутствует"]},
    "Контраст_Цветов": {"quest": "На данной картине присутствует контраст цветов?","buttons": ["Есть","Отсутствует"]},
    "Контраст_Форм": {"quest": "На данной картине присутствует контраст форм?","buttons": ["Есть","Отсутствует"]},
    "Контраст_Размеров": {"quest": "На данной картине присутствует контраст размеров?","buttons": ["Есть","Отсутствует"]},
    "Палитра": {"quest": "Какая палитра на данной картине?","buttons": ["Красочная","Монохромная"]},}


# Пример функции, которая обрабатывает команды


def save_ans(pic_id, param, mean):
    print(pic_id, param, mean)


def continu(pos, ignore):
    pos += 1
    # print(list(questions.keys()), len(list(questions.keys())), pos)
    if pos == len(list(questions.keys())) + 1:
        pos = 0
        # print(pos)
    elif list(questions.keys())[pos - 1] == ignore:
        pos += 1
    # print(pos)
    return pos


@dp.message_handler()
async def send_welcome(message: types.Message):
    global users_data
    startkeyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)  # Объявляем варианты ответов для кнопок
    buttons = ['/start_opros', '/about']
    startkeyboard.add(*buttons)  # Заполняем варианты ответов, распаковывая массив с названиями кнопок
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    if message.text == "/start":
        if message.from_user.id not in users_data.keys():
            users_data[message.from_user.id] = {"ignore": "Отвечу на всё", "position": -1, "pic_id": -1,
                                                "social_rate": 0}
            # with open('users_data.json') as json_file:
            # #Добавление юзера в локальный словарь если его нет и перезапись сейва
            #    json.dump(users_data, json_file)
            #    json_file.close()
        await message.answer("Привет! Это бот Color Study для сбора информации")

        await message.answer('Что бы вы хотели сделать?', reply_markup=startkeyboard)
    elif users_data[message.from_user.id]["position"] == -1 and message.text != '/about':
        picker = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ['Симметрия', 'Динамика', 'Колористика', 'Отвечу на все']
        picker.add(*buttons)
        if message.text in buttons:
            users_data[message.from_user.id]["ignore"] = message.text
            users_data[message.from_user.id]["position"] = continu(-1, users_data[message.from_user.id]["ignore"])
        else:
            await message.answer('Что бы вы не хотели оценивать?', reply_markup=picker)
        # return message.text
    elif message.text == '/about':
        await message.answer('*Что-то о Color Study*', reply_markup=startkeyboard)

    # Отправка изображения и первый вопрос юзеру. В обработчике следующего вопроса нужно сделать проверку
    # корректности ответа на первый, если первый вопрос вообще задаётся и собственно задать следующий вопрос.
    # contin делать только если ответ на предыдущий вопрос корректен
    if users_data[message.from_user.id]["position"] == 0 and message.text != "Нет":
        pic = InputFile(
            'test_images/' + random.choice([x for x in os.scandir("test_images/") if os.path.isfile(x)]).name)
        # contin = True
        users_data[message.from_user.id]["position"] = continu(0, users_data[message.from_user.id]["ignore"])
        await message.answer_photo(photo=pic, caption="Автор, название, год")

        # await message.reply(random.choice([x for x in os.scandir("test_images/")if os.path.isfile(x)]).name)

    if users_data[message.from_user.id]["position"] == 1:
        if message.text in questions["Композиция"]["buttons"]:
            save_ans(users_data[message.from_user.id]["pic_id"], "Композиция", message.text)
            # contin = True
            users_data[message.from_user.id]["position"] = continu(1, users_data[message.from_user.id]["ignore"])
        else:
            await message.answer(questions["Композиция"]["quest"],
                                 reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(
                                     *questions["Композиция"]["buttons"]))

    if users_data[message.from_user.id]["position"] == 2:
        if message.text in questions["Динамика"]["buttons"]:
            save_ans(users_data[message.from_user.id]["pic_id"], "Динамика", message.text)
            users_data[message.from_user.id]["position"] = continu(2, users_data[message.from_user.id]["ignore"])
        else:
            await message.answer(questions["Динамика"]["quest"],
                                 reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(
                                     *questions["Динамика"]["buttons"]))

    if users_data[message.from_user.id]["position"] == 3:
        if message.text in questions["Метафора"]["buttons"]:
            save_ans(users_data[message.from_user.id]["pic_id"], "Метафора", message.text)
            users_data[message.from_user.id]["position"] = continu(3, users_data[message.from_user.id]["ignore"])
            """# Рестарт опроса **************** Необходимо переносить в последний из существующих обработчиков вопросов
            picker = types.ReplyKeyboardMarkup(resize_keyboard=True)
            buttons = ["Да", "Нет"]
            picker.add(*buttons)
            await message.answer('Спасибо, ваши ответы записаны. Хотите продолжить?', reply_markup=picker)"""
            # ****************************************************
        else:
            await message.answer(questions["Метафора"]["quest"],
                                 reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(
                                     *questions["Метафора"]["buttons"]))

    if users_data[message.from_user.id]["position"] == 4:
        if message.text in questions["Фотомонтаж"]["buttons"]:
            save_ans(users_data[message.from_user.id]["pic_id"], "Фотомонтаж", message.text)
            users_data[message.from_user.id]["position"] = continu(4, users_data[message.from_user.id]["ignore"])
            # Рестарт опроса ******************* Необходимо переносить в последний из существующих обработчиков вопросов
            picker = types.ReplyKeyboardMarkup(resize_keyboard=True)
            buttons = ["Да", "Нет"]
            picker.add(*buttons)
            await message.answer('Спасибо, ваши ответы записаны. Хотите продолжить?', reply_markup=picker)
            # ****************************************************
        else:
            await message.answer(questions["Фотомонтаж"]["quest"],
                                 reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add(
                                     *questions["Фотомонтаж"]["buttons"]))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
