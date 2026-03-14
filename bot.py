import asyncio
import os
import random
import csv

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from dotenv import load_dotenv, find_dotenv
from datetime import timedelta

load_dotenv(find_dotenv())

import db

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



Users = {}
complements = []
with open('комплименты.csv', 'r', encoding='UTF-8') as comp:
    for i in csv.reader(comp):
        complements.append(''.join(i))

orgcom = ['@diaa_le', '@aamdenisov', '@DmitriyIkhsanov', '@DmitriyIkhsanov', '@nikiforovau', '@Polyakovaaa', '@ulbnv']

def find_user(message: types.Message):
    args = message.text.split()
    if len(args) == 2 and args[1].startswith('@'):
        return args[1][1:]
    return None

@dp.message(Command("help"))
async def help_cmd(message: types.Message):
    await message.answer(
    "📖 Доступные команды:\n"
    "\n"
    "Полезные:\n"
    "/help — Список команд\n"
    "/инфа [@username] — Информация о пользователе\n"
    #"/номер — Номер телефона пользователя\n"
    "/мут [секунды] — Мутит пользователя (ответом на сообщение)\n"
    "/анмут — Размут пользоватея. Используйте ответом на сообщение\n"
    "\n"
    "Приколюха:\n"
    "/вероятность — Рассчитывает вероятность события\n"
    "/цитата — Сохраняет цитату (ответом на сообщение)\n"
    "/мысль — Выводит рандомную цитату\n"
    "/мысль [@username] — Цитата конкретного пользователя\n"
    "/кто — Узнать, кто больше всего соответствует запросу\n"
    "/совместимость — Показывает совместимость чего-либо\n"
    "/комплимент — Сделать комплимент пользователю\n"
    "/рулетка — Испытай удачу\n"
    "\n"
    "Интерактивные команды:\n"
    "/обнять [@username]\n"
    "/пожать_руку [@username]\n"
    "/погладить [@username]\n"
    "/похвалить [@username]\n"
    "/поддержать [@username]\n"
    "/поблагодарить [@username]\n"
    "/поздравить [@username]\n"
    "/тыкнуть [@username]\n"
    "/посмотреть [@username]\n"
    "/позавидовать [@username]\n"
    "/ударить [@username]\n"
    "/уебать [@username]\n"
    "/оскорбить [@username]\n"
    "/уважать [@username]\n"
    "/осуждать [@username]\n"
    "/аплодировать [@username]"
)



@dp.message(Command('вероятность'))
async def chance_cmd(message: types.Message):
    event = message.text.replace('/вероятность', '', 1).strip()
    chance = random.randint(0, 100)
    if not event:
        await message.reply('Напишите событие')
    else:
        await message.reply(f'Вероятность того, что {event} - {chance}%')

@dp.message(Command('тест'))
async def test_cmd(message: types.Message):
    await message.answer(message.text)

@dp.message(Command('инфа'))
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

'''@dp.message(Command('номер'))
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

@dp.message(Command('мысль'))
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



@dp.message(Command('цитата'))
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

@dp.message(Command('кто'))
async def who_cmd(message: types.Message):
    question = message.text.split()
    who = random.choice(db.usernames())[0]
    if len(question) < 2:
        await message.reply('Вы неправильно использовали команду\nПопробуйте снова')
    else:
        question.remove('/кто')
        a = ' '.join(question)
        await message.reply(
            f'{who} {a}'
        )

@dp.message(Command('комплимент'))
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

@dp.message(Command('совместимость'))
async def compatibility_cmd(message: types.Message):
    event = message.text.replace('/совместимость', '', 1).strip()
    compatibility = random.randint(0, 100)
    if not event:
        await message.reply('Напишите событие')
    else:
        await message.reply(f'Совместимость {event} - {compatibility}%')

@dp.message(Command('рулетка'))
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

@dp.message(Command('мут'))
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
@dp.message(Command('анмут'))
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

'''@dp.message(Command('девиз'))
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
    if not message.text.startswith('/'):
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
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
