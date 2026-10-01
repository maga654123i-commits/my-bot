import logging
import asyncio
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# === ВСТАВЬ СЮДА СВОЙ ТОКЕН ОТ BOTFATHER ===
TOKEN = "8640095721:AAEI7EoHTa4T1RpulhZAu_VeggBPB0FdCU4"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Заглушка для Render, чтобы он видел открытый порт
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    server.serve_forever()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("а) А", callback_data="a"), InlineKeyboardButton("б) М", callback_data="m")],
        [InlineKeyboardButton("в) Ф", callback_data="q1_f"), InlineKeyboardButton("г) Ж", callback_data="j")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = (
        "Привет, солнышко! ❤️\n\n"
        "Я знаю, что 11 класс и ЕНТ — это жесткий стресс, но ты умница и со всем справишься!\n"
        "Давай немного отвлечемся. **Вопрос №1**:\n\n"
        "✨ **Кого любит Мага? На какую букву начинается имя его любимой девочки-маги?** ✨"
    )
    
    if update.message:
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")
    elif update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def show_question_2(query, hint_prefix=""):
    keyboard = [
        [InlineKeyboardButton("а) 16 👶", callback_data="q2_16"), InlineKeyboardButton("б) 20 😎", callback_data="q2_20")],
        [InlineKeyboardButton("в) 25 👴", callback_data="q2_25"), InlineKeyboardButton("г) 18 🔞", callback_data="q2_18")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = f"{hint_prefix}Первый вопрос позади! 🎉\n\n**Вопрос №2**:\n✨ **А сколько лет твоему Маге?** ✨"
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def show_question_3(query, hint_prefix=""):
    keyboard = [
        [InlineKeyboardButton("а) Профессиональный балет 🩰", callback_data="q3_ballet")],
        [InlineKeyboardButton("б) Создание приложений, игр и сайтов 💻", callback_data="q3_dev")],
        [InlineKeyboardButton("в) Сборка кубика Рубика 🧩", callback_data="q3_rubik")],
        [InlineKeyboardButton("г) Вышивание крестиком 🪡", callback_data="q3_stitch")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = f"{hint_prefix}Красота! Двигаемся дальше! 🚀\n\n**Вопрос №3**:\n✨ **Чем увлекается Мага больше всего?** ✨"
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def show_question_4(query, hint_prefix=""):
    keyboard = [
        [InlineKeyboardButton("а) Турецкие сериалы 🌹", callback_data="q4_turkish"), InlineKeyboardButton("б) Вести недели 📺", callback_data="q4_news")],
        [InlineKeyboardButton("в) Аниме ⛩️", callback_data="q4_anime"), InlineKeyboardButton("г) Кулинарные шоу 👨‍🍳", callback_data="q4_cooking")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = f"{hint_prefix}Уже близко к финалу! 🎯\n\n**Вопрос №4**:\n✨ **Что Мага обожает смотреть в свободное время?** ✨"
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def show_question_5(query, hint_prefix=""):
    keyboard = [
        [InlineKeyboardButton("а) Winston 🚬", callback_data="q5_winston"), InlineKeyboardButton("б) L&M 🚬", callback_data="q5_lm")],
        [InlineKeyboardButton("в) LD 🚬", callback_data="q5_ld"), InlineKeyboardButton("г) Chapman 🍫", callback_data="q5_chapman")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = f"{hint_prefix}И финальный вопрос викторины! 🏆\n\n**Вопрос №5**:\n✨ **Какие сигареты курит Мага?** ✨"
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    choice = query.data
    
    if choice == "q1_f":
        await show_question_2(query, hint_prefix="Угадала! Конечно же на 'Ф', ведь его любимой девушкой являешься ты! ❤️\n\n")
    elif choice in ["a", "m", "j"]:
        hints_q1 = {
            "a": "Мимо! 'А' — это 'Ангельская', но Мага любит кое-кого на другую букву! Подумай еще 😜",
            "m": "Хмм... 'М' — это сам Мага, а мы ищем его любимую девочку! Попробуй еще 😉",
            "j": "Не-а! 'Ж' — это 'Желанная', но первая буква имени другая! Давай еще попытку 💖"
        }
        retry_keyboard = [
            [InlineKeyboardButton("а) А", callback_data="a"), InlineKeyboardButton("б) М", callback_data="m")],
            [InlineKeyboardButton("в) Ф", callback_data="q1_f"), InlineKeyboardButton("г) Ж", callback_data="j")]
        ]
        await query.edit_message_text(
            text=f"{hints_q1.get(choice)}\n\n✨ **С какой буквы начинается имя любимой девочки Маги?** ✨",
            reply_markup=InlineKeyboardMarkup(retry_keyboard)
        )

    elif choice == "q2_18":
        await show_question_3(query, hint_prefix="Красава! В точку — 18 лет! 😎\n\n")
    elif choice in ["q2_20", "q2_16", "q2_25"]:
        hints_q2 = {
            "q2_20": "Ого, прибавила мне пару лет! Я ещё не настолько взрослый 😉 Попробуй еще!",
            "q2_16": "Эй, я же уже старше! Не уменьшай мой возраст 😜 Подумай еще!",
            "q2_25": "Ну ты чего, я ещё не дед! 😂 Давай другую цифру!"
        }
        retry_keyboard = [
            [InlineKeyboardButton("а) 16 👶", callback_data="q2_16"), InlineKeyboardButton("б) 20 😎", callback_data="q2_20")],
            [InlineKeyboardButton("в) 25 👴", callback_data="q2_25"), InlineKeyboardButton("г) 18 🔞", callback_data="q2_18")]
        ]
        await query.edit_message_text(
            text=f"{hints_q2.get(choice)}\n\n✨ **А сколько лет твоему Маге?** ✨",
            reply_markup=InlineKeyboardMarkup(retry_keyboard)
        )

    elif choice == "q3_dev":
        await show_question_4(query, hint_prefix="Естественно! Кодинг и IT — ванлав! 💻\n\n")
    elif choice in ["q3_ballet", "q3_rubik", "q3_stitch"]:
        hints_q3 = {
            "q3_ballet": "В пачке и на пуантах? 😂 Ну нет, балет оставлю профессионалам! Попробуй еще 😉",
            "q3_rubik": "Интересный вариант, но я больше по цифровым штукам! Подумай еще 😜",
            "q3_stitch": "Вышивание — это мило, но мои пальцы обычно стучат по клавиатуре! 😂 Давай еще попытку!"
        }
        retry_keyboard = [
            [InlineKeyboardButton("а) Профессиональный балет 🩰", callback_data="q3_ballet")],
            [InlineKeyboardButton("б) Создание приложений, игр и сайтов 💻", callback_data="q3_dev")],
            [InlineKeyboardButton("в) Сборка кубика Рубика 🧩", callback_data="q3_rubik")],
            [InlineKeyboardButton("г) Вышивание крестиком 🪡", callback_data="q3_stitch")]
        ]
        await query.edit_message_text(
            text=f"{hints_q3.get(choice)}\n\n✨ **Чем увлекается Мага больше всего?** ✨",
            reply_markup=InlineKeyboardMarkup(retry_keyboard)
        )

    elif choice == "q4_anime":
        await show_question_5(query, hint_prefix="Точно, Аниме! ⛩ Наш человек!\n\n")
    elif choice in ["q4_turkish", "q4_cooking", "q4_news"]:
        hints_q4 = {
            "q4_turkish": "100 серий страданий? 😅 Не-е-ет, это слишком даже для меня! Попробуй еще 😉",
            "q4_cooking": "Готовить люблю, но смотреть про это часами... Не, ищи другой вариант! 😜",
            "q4_news": "Серьезно? Новости? 😂 Я ещё не настолько дедушка! Подумай еще!"
        }
        retry_keyboard = [
            [InlineKeyboardButton("а) Турецкие сериалы 🌹", callback_data="q4_turkish"), InlineKeyboardButton("б) Вести недели 📺", callback_data="q4_news")],
            [InlineKeyboardButton("в) Аниме ⛩️", callback_data="q4_anime"), InlineKeyboardButton("г) Кулинарные шоу 👨‍🍳", callback_data="q4_cooking")]
        ]
        await query.edit_message_text(
            text=f"{hints_q4.get(choice)}\n\n✨ **Что Мага обожает смотреть в свободное время?** ✨",
            reply_markup=InlineKeyboardMarkup(retry_keyboard)
        )

    elif choice == "q5_lm":
        win_keyboard = [[InlineKeyboardButton("сыграть еще раз 🔄", callback_data="restart")]]
        await query.edit_message_text(
            text=(
                "🎉 **БИНГО! ТЫ ПРОШЛА ВСЕ 5 ВОПРОСОВ!** 🎉\n\n"
                "Да, L&M — классика! 🚬✨\n"
                "Ты знаешь Магу на все 100%! Кстати, этого бота он сам написал специально для тебя, ведь его любимой девушкой являешься ты. ❤️\n\n"
                "Помни: никакие ЕНТ, тесты, уроки и суета не заставят меня сомневаться в тебе. "
                "Ты самая крутая, сильная и любимая!\n\n"
                "Отдыхай больше, не бери всё близко к сердцу, а твоя поддержка всегда рядом! 🤍"
            ),
            reply_markup=InlineKeyboardMarkup(win_keyboard),
            parse_mode="Markdown"
        )
    elif choice in ["q5_winston", "q5_ld", "q5_chapman"]:
        hints_q5 = {
            "q5_winston": "Винстон? Не-а, хороший вариант, но выбор не тот! Попробуй еще 😉",
            "q5_ld": "LD? Мимо! Давай еще попытку 😜",
            "q5_chapman": "Чапман с вишней или шоколадом — стильно, конечно, но не они! Подумай еще! 😂"
        }
        retry_keyboard = [
            [InlineKeyboardButton("а) Winston 🚬", callback_data="q5_winston"), InlineKeyboardButton("б) L&M 🚬", callback_data="q5_lm")],
            [InlineKeyboardButton("в) LD 🚬", callback_data="q5_ld"), InlineKeyboardButton("г) Chapman 🍫", callback_data="q5_chapman")]
        ]
        await query.edit_message_text(
            text=f"{hints_q5.get(choice)}\n\n✨ **Какие сигареты курит Мага?** ✨",
            reply_markup=InlineKeyboardMarkup(retry_keyboard)
        )

def main():
    # Запускаем фоновый HTTP-сервер для Render
    threading.Thread(target=run_dummy_server, daemon=True).start()
    
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(start, pattern="^restart$"))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
