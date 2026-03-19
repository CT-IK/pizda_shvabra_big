import asyncio
import os
import random
import csv
import json 
from datetime import datetime, timedelta 

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

import db

ALLOWED_UPDATES = ['message']

TIMER_FILE = 'files/timer.json'
if not os.path.exists('files'):
    os.makedirs('files')
if not os.path.exists(TIMER_FILE):
    with open(TIMER_FILE, 'w') as f:
        json.dump([], f)

bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()

ACTIONS = {
    "обнять": [
        "🤗 @{from_user} обнял @{to_user}",
        "🫂 @{from_user} крепко обнял @{to_user}"
    ],
    "пожать_руку": [
        "🤝 @{from_user} пожал руку @{to_user}",
        "🤝 @{from_user} с уважением пожал руку @{to_user}"
    ],
    "погладить": [
        "😊 @{from_user} погладил @{to_user}",
        "😌 @{from_user} нежно погладил @{to_user}"
    ],
    "похвалить": [
        "🌟 @{from_user} похвалил @{to_user}: ты красавчик!",
        "👏 @{from_user} сказал, что @{to_user} отлично справился",
        "🔥 @{from_user} считает, что @{to_user} реально крут",
        "💎 @{from_user} отметил, что @{to_user} — топ",
        "🏆 @{from_user} похвалил @{to_user} за отличную работу"
    ],
    "поддержать": [
        "❤️ @{from_user} поддержал @{to_user}: всё получится",
        "🤝 @{from_user} рядом с @{to_user} в трудную минуту",
        "🫶 @{from_user} сказал @{to_user}, что он не один"
    ],
    "поблагодарить": [
        "🙏 @{from_user} поблагодарил @{to_user}",
        "💐 @{from_user} сказал спасибо @{to_user}",
        "🙌 @{from_user} выразил благодарность @{to_user}"
    ],
    "поздравить": [
        "🎉 @{from_user} поздравил @{to_user}",
        "🥳 @{from_user} от всей души поздравляет @{to_user}",
        "🎂 @{from_user} пожелал всего лучшего @{to_user}"
    ],

    "тыкнуть": [
        "👉 @{from_user} тыкнул в @{to_user}",
        "😐 @{from_user} зачем-то тыкнул @{to_user}"
    ],
    "посмотреть": [
        "👀 @{from_user} внимательно посмотрел на @{to_user}",
        "🧐 @{from_user} изучающе посмотрел на @{to_user}"
    ],
    "позавидовать": [
        "😒 @{from_user} завидует @{to_user}",
        "👀 @{from_user} с завистью посмотрел на @{to_user}"
    ],

    "ударить": [
        "👊 @{from_user} ударил @{to_user}",
        "💥 @{from_user} отвесил леща @{to_user}"
    ],
    "уебать": [
        "💢 @{from_user} уебал @{to_user}",
        "🔥 @{from_user} жёстко уебал @{to_user}"
    ],
    "оскорбить": [
        "😈 @{from_user} оскорбил @{to_user}",
        "💀 @{from_user} словесно уничтожил @{to_user}"
    ],
    "уважать": [
        "🫡 @{from_user} выразил уважение @{to_user}",
        "💪 @{from_user} уважает @{to_user}"
    ],
    "осуждать": [
        "☝️ @{from_user} осуждает @{to_user}",
        "🤨 @{from_user} неодобрительно посмотрел на @{to_user}"
    ],
    "аплодировать": [
        "👏 @{from_user} аплодирует @{to_user}",
        "👏👏 @{from_user} громко похлопал @{to_user}"
    ]
}


def now_msk():
    return datetime.utcnow() + timedelta(hours=3)

Users = {}
complements = []
with open('комплименты.csv', 'r', encoding='UTF-8') as comp:
    for i in csv.reader(comp):
        complements.append(''.join(i))

orgcom = ['@diaa_le', '@aamdenisov', '@DmitriyIkhsanov', '@DmitriyIkhsanov', '@nikiforovau', '@Polyakovaaa', '@ulbnv']

def read_timer():
    with open(TIMER_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_timer(data):
    with open(TIMER_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def find_user(message: types.Message):
    args = message.text.split()
    if len(args) >= 2 and args[1].startswith('@'):
        return args[1][1:]
    return None

async def check_alarms():
    while True:
        now = now_msk()
        alarms = read_timer()
        if alarms:
            new_alarms = []
            for alarm in alarms:
                alarm_time = datetime.strptime(f"{alarm['date']} {alarm['time']}", "%d.%m.%Y %H:%M")
                if now >= alarm_time:
                    try:
                        await bot.send_message(alarm['chat_id'], f"🔔 @{alarm['user']}, ПОДЪЕМ!")
                    except:
                        pass
                else:
                    new_alarms.append(alarm)
            write_timer(new_alarms)
        await asyncio.sleep(30)

@dp.message(Command("помощь", prefix="!"))
async def help_cmd(message: types.Message):
    await message.answer(
    "📖 Доступные команды:\n"
    "\n"
    "Полезные:\n"
    "!помощь — Список команд\n"
    "!инфа [@username] — Информация о пользователе\n"
    #"/номер — Номер телефона пользователя\n"
    "!мут [секунды] — Мутит пользователя (ответом на сообщение)\n"
    "!анмут — Размут пользоватея. Используйте ответом на сообщение\n"
    "\n"
    "Приколюха:\n"
    "!вероятность — Рассчитывает вероятность события\n"
    "!цитата — Сохраняет цитату (ответом на сообщение)\n"
    "!мысль — Выводит рандомную цитату\n"
    "!мысль [@username] — Цитата конкретного пользователя\n"
    "!кто — Узнать, кто больше всего соответствует запросу\n"
    "!совместимость — Показывает совместимость чего-либо\n"
    "!комплимент — Сделать комплимент пользователю\n"
    "!рулетка — Испытай удачу\n"
    "\n"
    "Будильник:\n"
    "!разбудить [сегодня/завтра/ДД:ММ] [ЧЧ:ММ] [@username] - без него разбудит тебя\n"
    "!не будить — убрать меня из списка\n"
    "!разбудяшки — список будильников\n"
    "\n"
    "Интерактивные команды:\n"
    "!обнять [@username]\n"
    "!пожать_руку [@username]\n"
    "!погладить [@username]\n"
    "!похвалить [@username]\n"
    "!поддержать [@username]\n"
    "!поблагодарить [@username]\n"
    "!поздравить [@username]\n"
    "!тыкнуть [@username]\n"
    "!посмотреть [@username]\n"
    "!позавидовать [@username]\n"
    "!ударить [@username]\n"
    "!уебать [@username]\n"
    "!оскорбить [@username]\n"
    "!уважать [@username]\n"
    "!осуждать [@username]\n"
    "!аплодировать [@username]"
)

@dp.message(F.text.startswith("!разбудить"))
async def set_alarm_cmd(message: types.Message):
    args = message.text.split()
    if len(args) < 3:
        return await message.reply("Используй: !разбудить [сегодня/завтра/ДД.ММ] [ЧЧ:ММ] [@username]")

    date_arg, time_arg = args[1].lower(), args[2]
    target = args[3][1:] if len(args) > 3 and args[3].startswith('@') else message.from_user.username

    dt_now = now_msk()

    # Формируем дату будильника
    if date_arg == "сегодня":
        date_val = dt_now.strftime("%d.%m.%Y")
    elif date_arg == "завтра":
        date_val = (dt_now + timedelta(days=1)).strftime("%d.%m.%Y")
    else:
        try:
            date_val = datetime.strptime(date_arg, "%d.%m").replace(year=dt_now.year).strftime("%d.%m.%Y")
        except:
            return await message.reply("Ошибка даты (ДД.ММ)")

    # Проверка корректности времени
    try:
        datetime.strptime(f"{date_val} {time_arg}", "%d.%m.%Y %H:%M")
    except:
        return await message.reply("Ошибка времени (ЧЧ:ММ)")

    # Сохраняем будильник
    alarms = read_timer()
    alarms.append({"date": date_val, "time": time_arg, "user": target, "chat_id": message.chat.id})
    write_timer(alarms)
    await message.reply(f"Ок, разбужу @{target} {date_val} в {time_arg}")


@dp.message(F.text == "!не будить")
async def unwake_cmd(message: types.Message):
    alarms = read_timer()
    new_alarms = [a for a in alarms if a['user'] != message.from_user.username]
    if len(alarms) == len(new_alarms):
        await message.answer("Хорошо...\nХотя тебя и не было в списке разбудяшек...")
    else:
        write_timer(new_alarms)
        await message.answer("Хорошо, я не буду тебя будить!")

@dp.message(F.text == "!разбудяшки")
async def awakers_cmd(message: types.Message):
    alarms = read_timer()
    if not alarms: return await message.answer("Список пуст")
    res = "Вот список разбудяшек:"
    for a in alarms:
        try:
            u = db.userdata("@" + a['user'])[0]
            name = f"{u[0]}" if u else a['user']
        except: name = a['user']
        res += f"\n{name} {a['date']} в {a['time']}"
    await message.answer(res)

@dp.message(Command('вероятность', prefix="!"))
async def chance_cmd(message: types.Message):
    event = message.text.replace('!вероятность', '', 1).strip()
    chance = random.randint(0, 100)
    if not event:
        await message.reply('Напишите событие')
    else:
        await message.reply(f'Вероятность {event} - {chance}%')

@dp.message(Command('тест', prefix="!"))
async def test_cmd(message: types.Message):
    await message.answer(message.text)

@dp.message(Command('инфа', prefix="!"))
async def info_cmd(message: types.Message):
    args = message.text.split()
    if len(args) > 1 and args[1].startswith('@'):
        username = args[1]
    else:
        await message.reply(
            "❗ Используй:\n"
            "/инфа @username"
        )
        return
    
    userdata = db.userdata(username)[0]
    if userdata == None:
        text = 'Пользователь не найден'
    else:
        if db.userdata(username)[1] == 'Coach':
            text = (
        f"<b>👤 ИНФОРМАЦИЯ ПОЛЬЗОВАТЕЛЯ</b>\n\n"
        f"<b>ФИО:</b> {userdata[0]}\n"
        f"<b>Роль:</b> {userdata[5]}\n"
        f"<b>Курс:</b> {userdata[1]}\n"
        f"<b>Telegram:</b> {username}\n"
        f"<b>Номер телефона:</b> {userdata[4]}\n"
    )
        else:
            text = (
        f"<b>👤 ИНФОРМАЦИЯ ПОЛЬЗОВАТЕЛЯ</b>\n\n"
        f"<b>ФИО:</b> {userdata[0]}\n"
        f"<b>Роль:</b> {userdata[10]}\n"
        f"<b>Факультет:</b> {userdata[2]} {userdata[1]} курс\n"
        f"<b>ВК:</b> <a href='{userdata[4]}'>Кликабельно</a>\n"
        f"<b>Telegram:</b> {username}\n"
        f"<b>Номер телефона:</b> {userdata[7]}\n"
    )

    await message.reply(text, parse_mode="HTML")

'''@dp.message(Command('номер', prefix="!"))
async def number_cmd(message: types.Message):
    user = None
    if message.reply_to_message:
        user = message.reply_to_message.from_user.username
    else:
        args = message.text.split()
        if len(args) > 1 and args[1].startswith('@'):
            user = args[1][1:]
    if not user:
        await message.reply(
            "❗ Используй:\n"
            "/инфа ответом на сообщение\n"
            "/инфа @username"
        )
        return
    for i in DATA:
        if ('@' + user) in i:
            userinfo = i
    if userinfo == None:
        await message.reply("❌ Пользователь не найден")
    user_number = userinfo[7]
    await message.reply(user_number)'''

@dp.message(Command('мысль', prefix="!"))
async def thought_cmd(message: types.Message):
    thoughts = []
    with open('цитаты.csv', 'r', encoding='UTF-8') as file:
        reader = csv.reader(file)
        for row in reader:
            thoughts.append(row)
    args = message.text.split()
    if len(args) > 2:
        await message.reply('Вы неправильно использовали команду\nПопробуйте снова')
    else:
        if len(args) == 1:
            random_thought = random.choice(thoughts)
            thought, author = random_thought
            await message.reply(
                f'«{thought}»\n\n'
                f'Автор: @{author}'
            )
        elif len(args) == 2 and args[1].startswith('@'):
            user = args[1][1:]
            if ('@' + user) in (message.text.split()):
                userquotes = [x for x in thoughts if user in x]
                random_thought = random.choice(userquotes)
                thought, author = random_thought
                await message.reply(
                    f'«{thought}»\n\n'
                    f'Автор: @{author}'
                )
            else:
                await message.reply('❌ Пользователь не найден')
        else:
            await message.reply('Вы неправильно использовали команду\nПопробуйте снова')



@dp.message(Command('цитата', prefix="!"))
async def quote_cmd(message: types.Message):
    quote = message.reply_to_message.text
    user = message.reply_to_message.from_user.username
    if quote == None:
        await message.reply('Используйте ответом на сообщение')
    else:
        with open('цитаты.csv', 'a', encoding='UTF-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([quote, user])
        await message.reply(
            f'💾 Цитата сохранена!\n\n'
            f"«{quote}»\n"
            f"— @{user}"
        )

@dp.message(Command('кто', prefix="!"))
async def who_cmd(message: types.Message):
    question = message.text.split()
    who = random.choice(db.usernames())[0]
    if len(question) < 2:
        await message.reply('Вы неправильно использовали команду\nПопробуйте снова')
    else:
        question.remove('!кто')
        a = ' '.join(question)
        await message.reply(
            f'{who} {a}'
        )

@dp.message(Command('комплимент', prefix="!"))
async def complement_cmd(message: types.Message):
    user = None
    if message.reply_to_message:
        user = message.reply_to_message.from_user.username
    else:
        args = message.text.split()
        if len(args) > 1 and args[1].startswith('@'):
            user = args[1][1:]
    if not user:
        await message.reply(
            "❗ Используй:\n"
            "/комплимент ответом на сообщение\n"
            "/комплимент @username"
        )
    else:
        complement = random.choice(complements)
        await message.reply(f'@{user} {complement}')    

@dp.message(Command('совместимость', prefix="!"))
async def compatibility_cmd(message: types.Message):
    event = message.text.replace('/совместимость', '', 1).strip()
    compatibility = random.randint(0, 100)
    if not event:
        await message.reply('Напишите событие')
    else:
        await message.reply(f'Совместимость {event} - {compatibility}%')

@dp.message(Command('рулетка', prefix="!"))
async def roulette_cmd(message: types.Message):
    a = message.from_user
    Users[a.id] = a.username
    chance = random.randint(1, 6)
    if chance == 1:
        until_date = message.date + timedelta(minutes=5)
        await bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=message.from_user.id,
            permissions=types.ChatPermissions(can_send_messages=False),
            until_date=until_date
        )
        await message.reply('Тебе сегодня явно не везет\nТы поймал мут на 5 минут')
    else:
        await message.reply('Везунчик, живешь без мута\nПопробуй еще раз')

@dp.message(Command('мут', prefix="!"))
async def mute_cmd(message: types.Message):
    args = message.text.split()
    member = await bot.get_chat_member(
        chat_id=message.chat.id,
        user_id=message.from_user.id
    )
    if member.status in ('administrator', 'creator'):
        if len(args) == 2:
            seconds = int(args[1])
            a = message.reply_to_message.from_user
            user = message.reply_to_message.from_user.username
            user_id = message.reply_to_message.from_user.id
            until_date = message.date + timedelta(seconds=seconds)
            Users[a.id] = a.username
            await bot.restrict_chat_member(
                chat_id=message.chat.id,
                user_id=user_id,
                permissions=types.ChatPermissions(can_send_messages=False),
                until_date=until_date
            )
            await message.reply(
                'Готово!\n'
                f'Пользователь @{user} замучен на {seconds} секунд'
            )
        else:
            await message.reply('Введите в формате\n/мут [секунды]\nи используйте ответом на сообщение пользователя')   
    else:
        await message.reply('Нельзя тебе мутить\nМаленький еще!')
@dp.message(Command('анмут', prefix="!"))
async def unmute_cmd(message: types.Message):
    if message.reply_to_message:
        await bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=message.reply_to_message.from_user.id,
            permissions=types.ChatPermissions(can_send_messages=True)
        )
        await message.reply('Сделал')
    else:
        for user_id in Users.keys():
            await bot.restrict_chat_member(
                chat_id=message.chat.id,
                user_id=user_id,
                permissions=types.ChatPermissions(can_send_messages=True)
            )
        await message.reply('Все пользователи размучены')

'''@dp.message(Command('девиз', prefix="!"))
async def devis_cmd(message: types.Message):
    args = message.text.split()
    if len(args) == 2 and args[1].startswith('@'):
        user = find_user(message)
        for i in DATA:
            if ('@' + user) in i:
                a = i
        await message.reply(
            f'{a[9]}\n\n'
            f'Автор: {a[5]}'
        )
    else:    
        a = random.choice(DATA)
        await message.reply(
            f'{a[9]}\n\n'
            f'Автор: {a[5]}'
        )'''

#интерактивные команды
@dp.message()
async def action_cmd(message: types.Message):
    if not message.text or not message.text.startswith('!'):
        return
    command = message.text.split()
    command = command[0][1:]
    if command not in ACTIONS:
        return
    to_user = find_user(message)
    from_user = message.from_user.username
    if to_user == None:
        await message.reply('Введите в формате\n/[действие] @username')
    else:
        text = random.choice(ACTIONS[command]).format(from_user=from_user, to_user=to_user)
        await message.reply(text)

@dp.message()
async def save_users(message: types.Message):
    user = message.from_user
    Users[user.id] = user.username

async def main():
    print('Бот работает')
    await bot.delete_webhook(drop_pending_updates=True)
    asyncio.create_task(check_alarms()) # Запуск фоновой проверки будильников
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)

if __name__ == "__main__":
    asyncio.run(main())