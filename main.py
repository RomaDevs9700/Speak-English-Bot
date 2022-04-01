import logging
from aiogram import Bot, Dispatcher, executor, types
from oxfordLookup import getDefinitions
from googletrans import Translator
translator = Translator()

API_TOKEN = ''
ADMINS = []  # your telegram id

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_start_welcome(message: types.Message):
    await message.answer(f"Salom 👋, {message.from_user.full_name}\n"
                         "🗣 Speak English Botiga Xush kelibsiz!"
                         "Bot foydalanish uchun so'z yoki matn yuboring")
    if message.from_user.username:
        user_n = message.from_user.username
    else:
        user_n = "username yo'q"
    msg = f"{message.from_user.full_name} va @{user_n} foydalanuvchi Speak English botdan foydalandi"
    await bot.send_message(chat_id=ADMINS[0], text=msg)


@dp.message_handler(commands=['help'])
async def send_help_welcome(message: types.Message):
    await message.answer("""
1) Bitta so'zning inglizcha ma'nosi va audiosini olishni istasangiz, bitta so'z yuboring!
2) Bittadan ko'p so'z, matn yuborsangiz uni ingliz tiliga tarjima qilib yuboramiz, ingliz tilida yuborsangiz o'zbekchaga! 
🇺🇿Uzbek - English🇬🇧
🇬🇧English - Uzbek🇺🇿 
🏁Other Language - English🇬🇧""")


@dp.message_handler()
async def tarjimon(message: types.Message):
    lang = translator.detect(message.text).lang
    if len(message.text.split()) > 2:
        dest = 'uz' if lang == 'en' else 'en'
        await message.answer(translator.translate(message.text, dest).text)
    else:
        if lang == 'en':
            word_id = message.text
        else:
            word_id = translator.translate(message.text, dest='en').text

        lookup = getDefinitions(word_id)
        if lookup:
            await message.reply(f"Word: {word_id} \nDefinitions:\n{lookup['definitions']}")
            if lookup.get('audio'):
                await message.reply_voice(lookup['audio'])
        else:
            await message.reply("Bunday so'z topilmadi")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)