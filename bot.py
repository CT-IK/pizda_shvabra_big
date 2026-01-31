import asyncio
import os
import random
import csv

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from dotenv import load_dotenv, find_dotenv
from datetime import timedelta

load_dotenv(find_dotenv())

bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()

Users = {}
complements = []
with open('комплименты.csv', 'r', encoding='UTF-8') as comp:
    for i in csv.reader(comp):
        complements.append(''.join(i))

DATA = []
with open('DATA.csv', 'r', encoding='UTF-8') as file:
    for i in csv.reader(file):
        if i[5].startswith('@'):
            DATA.append(i)
usernames = [y for x in DATA for y in x if y.startswith('@')]

@dp.message(Command("help"))
async def help_cmd(message: types.Message):
    await message.answer(
        "📖 Доступные команды:\n"
        "\n"
        "Полезные:\n"
        "/help — Список команд\n"
        "/инфа - Информация о пользователе. Используйте с ответом на сообщение или укажите @username\n"
        "/номер - Номер телефона пользователя\n"
        "/мут [секунды] - Мутит пользователя. Используйте с ответом на сообщение\n"
        "/анмут - Размут всех пользователей\n"
        "\n"
        "Приколюха:\n"
        "/вероятность - расчитывает вероятность события\n"
        "/цитата - Сохраняет цитату. Используйте с ответом на сообщение\n"
        "/цитата - Выводит рандомную цитату\n"
        "/цитата @username - Выводит рандомную цитату пользователя\n"
        "/кто - Узнать, кто больше всего соответствует запросу\n"
        "/совместимость – Показывает совместимость чего-либо.\n"
        "/комплимент - Делает комплемент пользователю. Используйте с ответом на сообщение или @username\n"
        "/рулетка - Испытай удачу\n"
        "/девиз - Выдает рандомный девиз с анкет с подписью автора"
    )


@dp.message(Command('вероятность'))
async def chance_cmd(message: types.Message):
    event = message.text.replace('/вероятность', '', 1).strip()
    chance = random.randint(0, 100)
    if not event:
        await message.reply('Напишите событие')
    else:
        await message.reply(f'Вероятность того, что {event} - {chance}%')


@dp.message(Command('инфа'))
async def info_cmd(message: types.Message):
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
    user_name = userinfo[0]
    user_course = userinfo[1]
    user_faculty = userinfo[2]
    user_VK = userinfo[4]
    user_number = userinfo[7]
    user_devis = userinfo[9]
    user_role = userinfo[10]
    if user_role == '':
        user_role = 'Саппорт'
    
    
    text = (
        f"<b>👤 ИНФОРМАЦИЯ ПОЛЬЗОВАТЕЛЯ</b>\n\n"
        f"<b>ФИО:</b> {user_name}\n"
        f"<b>Роль:</b> {user_role}\n"
        f"<b>Факультет:</b> {user_faculty} {user_course} курс\n"
        f"<b>ВК:</b> <a href='{user_VK}'>Кликабельно</a>\n"
        f"<b>Telegram:</b> @{user}"
    )

    await message.reply(text, parse_mode="HTML")

@dp.message(Command('номер'))
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
    await message.reply(user_number)

@dp.message(Command('цитата'))
async def quote_cmd(message: types.Message):
    if message.reply_to_message:
        quote = message.reply_to_message.text
        user = message.reply_to_message.from_user.username
        with open('цитаты.csv', 'a', encoding='UTF-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([quote, user])
        await message.reply(
            f'💾 Цитата сохранена!\n\n'
            f"«{quote}»\n"
            f"— @{user}"
        )
    else:
        args = message.text.split()
        if len(args) > 1 and args[1].startswith('@'):
            user = args[1][1:]
        quotes = []
        with open('цитаты.csv', 'r', encoding='UTF-8') as file:
            reader = csv.reader(file)
            for row in reader:
                quotes.append(row)
        if len(message.text.split()) == 1:
            random_quotes = random.choice(quotes)
            quote, author = random_quotes
            await message.reply(
                f'«{quote}»\n\n'
                f'Автор: @{author}'
            )
        
        else:
            if ('@' + user) in (message.text.split()):
                userquotes = [x for x in quotes if user in x]
                random_quotes = random.choice(userquotes)
                quote, author = random_quotes
                await message.reply(
                    f'«{quote}»\n\n'
                    f'Автор: @{author}'
                )

            else:
                await message.reply('Вы неправильно использовали команду\nПопробуйте снова')

@dp.message(Command('кто'))
async def who_cmd(message: types.Message):
    question = message.text.split()
    who = random.choice(usernames)
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
        await message.reply('БАМ! Тебе сегодня явно не везет\nТы поймал мут на 5 минут')
    else:
        await message.reply('Везунчик, живешь без мута\nПопробуй еще раз)')

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
            await message.reply('Введите в формате\n/мут [секунды]\n И используйте ответом на сообщение пользователя')   
    else:
        await message.reply('Нельзя тебе мутить\nМаленький еще!')
@dp.message(Command('анмут'))
async def unmute_cmd(message: types.Message):
    for user_id in Users.keys():
        await bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=user_id,
            permissions=types.ChatPermissions(can_send_messages=True)
        )
    await message.reply('Все пользователи размучены')

@dp.message(Command('девиз'))
async def devis_cmd(message: types.Message):
    a = random.choice(DATA)
    await message.reply(
        f'{a[9]}\n\n'
        f'Автор: {a[5]}'
    )

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
