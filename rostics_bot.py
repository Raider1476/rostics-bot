from flask import Flask
from threading import Thread
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import logging
import os

# Логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Получаем токен из Secrets
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("Токен бота не найден в Secrets!")
else:
    logger.info("Токен успешно загружен из Secrets.")

# Создаем Flask приложение
app = Flask(__name__)

# Маршрут для главной страницы
@app.route('/')
def home():
    return "Бот активен!"

# Функция для запуска Flask сервера
def run_flask():
    logger.info("Flask сервер запускается...")
    port = int(os.environ.get("PORT", 5000))  # Используем порт из переменной окружения
    app.run(host='0.0.0.0', port=port)  # Привязываем к 0.0.0.0

# Запуск Flask сервера в отдельном потоке
def keep_alive():
    t = Thread(target=run_flask)
    t.start()

# Приветственное сообщение
async def start(update: Update, context: CallbackContext):
    logger.info("Пользователь запустил бота")
    welcome_message = "Привет, я бот по стандартам Rostics! 🍟\nВыбери свою станцию и подраздел:"
    buttons = [["1. Касса", "2. Сервис"], ["3. Кухня", "4. Мойка"], ["5. Мытье рук и химия"]]
    reply_markup = ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

# Обработка выбора станции и подраздела
async def handle_message(update: Update, context: CallbackContext):
    logger.info(f"Получено сообщение: {update.message.text}")
    text = update.message.text
    if text in ["1. Касса", "2. Сервис", "3. Кухня", "4. Мойка", "5. Мытье рук и химия"]:
        if text == "1. Касса":
            buttons = [
                ["1. Сроки годности", "2. Сервировка и сборка"],
                ["3. Напитки и десерты", "4. Остальное"],
                ["Назад"]
            ]
            reply_markup = ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True)
            await update.message.reply_text("Выбери подраздел Кассы:", reply_markup=reply_markup)
        elif text == "2. Сервис":
            buttons = [
                ["1. Сроки годности и пополнение", "2. Составы"],
                ["3. Фритюр"],
                ["Назад"]
            ]
            reply_markup = ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True)
            await update.message.reply_text("Выбери подраздел Сервиса:", reply_markup=reply_markup)
        elif text == "3. Кухня":
            buttons = [
                ["1. Шортенинг (жир)", "2. Дефростация"],
                ["3. Сроки хранения", "4. Панирование"],
                ["5. Жарим"],
                ["Назад"]
            ]
            reply_markup = ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True)
            await update.message.reply_text("Выбери подраздел Кухни:", reply_markup=reply_markup)
        elif text == "4. Мойка":
            await send_washing_info(update)
        elif text == "5. Мытье рук и химия":
            await send_washing_info(update)
    elif text == "Назад":
        await start(update, context)
    elif text == "2. Дефростация":
        await send_defrost_info(update)
    elif text == "1. Шортенинг (жир)":
        await send_shortening_info(update)
    elif text == "5. Жарим":
        await send_frying_info(update)
    elif text == "4. Панирование":
        await send_paniruem_info(update)
    elif text == "3. Сроки хранения":
        await send_srok_hraneniya_info(update)
    elif text == "2. Сервировка и сборка":
        await send_servirovka_info(update)
    elif text == "3. Напитки и десерты":
        await send_drinks_info(update)
    elif text == "4. Остальное":
        await send_other_info(update)
    elif text == "1. Сроки годности и пополнение":
        await send_srok_godnosti_info(update)
    elif text == "2. Составы":
        await send_sostav_info(update)
    elif text == "3. Фритюр":
        await send_fryer_info(update)
    elif text == "1. Сроки годности":
        await send_sroki_godnosti_kassa_info(update)
    elif text == "Приготовление замеса":
        await send_zames_info(update)
    elif text == "В главное меню":
        await start(update, context)
    else:
        await update.message.reply_text("Пожалуйста, выбери подраздел из списка.")

# Функция для отправки информации о сроках годности в разделе Кассы
async def send_sroki_godnosti_kassa_info(update: Update):
    try:
        await update.message.reply_photo(photo="https://i.ibb.co/nBNzkRh/sroki.jpg")
    except Exception as e:
        logger.error(f"Ошибка в send_sroki_godnosti_kassa_info: {e}")
    await show_main_menu(update)

# Функция для отправки информации о дефростации
async def send_defrost_info(update: Update):
    try:
        messages = [
            "Мясо размораживается сутки, хранится после этого двое. Экстренная разморозка мяса производится в воде, в средней раковине, при температуре не более 21, срок годности включая время разморозки (1,5 ч) - 12 часов.",
            "Экстренная разморозка производится в средней раковине, в мармиде, стоявшем выше уровня мойки, решётки отделяют пакеты друг от друга, вода непрерывно циркулирует."
        ]
        for message in messages:
            await update.message.reply_text(message)
        await update.message.reply_photo(photo="https://i.ibb.co/JzHvHWg/defrost.jpg")
    except Exception as e:
        logger.error(f"Ошибка в send_defrost_info: {e}")
    await show_main_menu(update)

# Функция для отправки информации о шортенинге (жире)
async def send_shortening_info(update: Update):
    try:
        messages = [
            "Враги жира: химия, металл, соль, вода, тепло, воздух, частицы пищи.",
            "Признаки испорченного жира: цвет, запах, вкус, задымление, пенообразование.",
            "Фильтрация - надеваем СИЗ, выключаем машинку, включаем напор и слив жира. Чистим кочергой, поднимаем жир.",
            "Открытый фритюр фильтруется не более 5 минут, закрытый не более 7. Магнезолятся машинки 15 минут. Магнезол делают два раза в день: утром до первой партии мяса и после часа-пика.",
            "38 градусов температура перелива жира."
        ]
        for message in messages:
            await update.message.reply_text(message)
    except Exception as e:
        logger.error(f"Ошибка в send_shortening_info: {e}")
    await show_main_menu(update)

# Функция для отправки информации о жарке
async def send_frying_info(update: Update):
    try:
        messages = [
            "Крыло жарится 10 минут, байтсы 3:05, стрипсы 4:30, зингер 7 минут. Температура 171.",
            "Ориг стрипсы 1 пакет - 178 градусов, 2 - 182. Ноги пакет 154, два пакета - 168, 3 пакета 174, 4 пакета 182. Филе ор - 182.",
            "Для дезинфекции поверхностей используем микрокват. Вытереть тряпкой с микрокватом муку с ручек, смочить тряпку водой, вытереть повторно, помыть руки."
        ]
        for message in messages:
            await update.message.reply_text(message)
    except Exception as e:
        logger.error(f"Ошибка в send_frying_info: {e}")
    await show_main_menu(update)

# Функция для отправки информации о панировании
async def send_paniruem_info(update: Update):
    try:
        messages = [
            "Перед панированием нужно провести инспекцию продукта на синяки, кровоподтёки, перья, кристаллики льда, переломы костей.",
            "Также запанированное мясо не хранится (надо сразу во фритюр отправлять).",
            "Перед началом панирования машинку переводим в режим drop (на нагрев).",
            "Мука просеивается каждые два цикла, как и меняется вода. Муку надо засыпать по отметку в ванне.",
            "Вода для панирования набирается на краю нижней ванны, в этот момент мыть руки нельзя, дабы избежать перекрёстного загрязнения.",
            "Принципы панирования: Крылья, байтсы, стрипсы, филе - 7-10-7-7. То есть: 7 раз собрать-поднять собрать-накрыть, 10 раз потрясти от влаги, 7 раз собрать-поднять собрать-накрыть, 7 раз придавить. Ноги - 7-7-7. То есть: 7 раз собрать-поднять, 7 раз собрать-поднять, 7 раз придавить."
        ]
        for message in messages:
            await update.message.reply_text(message)
        await update.message.reply_photo(photo="https://i.ibb.co/ym9Jd6w/paniruem.jpg")
        await update.message.reply_photo(photo="https://i.ibb.co/cvx3ryy/paniruem1.jpg")
        await update.message.reply_photo(photo="https://i.ibb.co/dgpJy6y/paniruem2.jpg")
        await update.message.reply_photo(photo="https://i.ibb.co/K9ydS0w/paniruem3.jpg")
        await update.message.reply_photo(photo="https://i.ibb.co/b5214qS/paniruem4.jpg")
        await update.message.reply_photo(photo="https://i.ibb.co/ggJWFQ0/paniruem5.jpg")
    except Exception as e:
        logger.error(f"Ошибка в send_paniruem_info: {e}")
    await show_main_menu(update)

# Функция для отправки информации о мойке
async def send_washing_info(update: Update):
    try:
        messages = [
            "Мойка посуды:",
            "Левая ванна Дезинфекция Micro Quat❕Средняя ванна Ополаскивание❕ Правая ванна мойка « Lemon »❕",
            "1) Наливаем раствор в правую ванну « Lemon » 1 нажатие на 36 литров (t' 43-50) До границы синей линии.",
            "2) Наливаем Micro Quat в левую ванную дезинфекция, концентрация 450ppm (0,05%). (t' 18-22). Для 40 литров раствора необходимо 5 литров раствора Micro Quat 4% и 35 литров холодной воды (t' 18-22). Для 64 литров 8 литров раствора Micro Quat 4% и 56 л холодной воды (t' 18-22).",
            "3) Очищаем посуду и замачиваем на 5-10 минут в правой ванне.",
            "4) Ополаскиваем в средней ванне теплой водой. Если есть необходимость, воспользуйтесь щеткой для мытья посуды или падом.",
            "5) Замачиваем в Micro Quat на 15 мин. (t' 18-22).",
            "6) После споласкиваем в средней ванне 65 t'.",
            "7) Ставим сушиться на стелаж мойки в перевернутом виде."
        ]
        for message in messages:
            await update.message.reply_text(message)
        await update.message.reply_photo(photo="https://i.ibb.co/gM9Dg44/washing2.jpg")
        await update.message.reply_photo(photo="https://i.ibb.co/GdJ455r/washing1.jpg")
        await update.message.reply_photo(photo="https://i.ibb.co/ccYYkPN/washing.jpg")
    except Exception as e:
        logger.error(f"Ошибка в send_washing_info: {e}")
    await show_main_menu(update)

# Функция для отправки информации о сроках хранения в разделе Кухни
async def send_srok_hraneniya_info(update: Update):
    try:
        await update.message.reply_photo(photo="https://i.ibb.co/dQ7r6Q8/srokp.jpg")
    except Exception as e:
        logger.error(f"Ошибка в send_srok_hraneniya_info: {e}")
    await show_main_menu(update)

# Функция для отправки информации о сервировке и сборке
async def send_servirovka_info(update: Update):
    try:
        await update.message.reply_photo(photo="https://i.ibb.co/QDbbfHd/servirovka.jpg")
        await update.message.reply_photo(photo="https://i.ibb.co/hKgz235/servirovka1.jpg")
        await update.message.reply_photo(photo="https://i.ibb.co/gjhYCb7/servirovka3.jpg")
        await update.message.reply_photo(photo="https://i.ibb.co/s95gGCb/servirovka4.jpg")
        await update.message.reply_photo(photo="https://i.ibb.co/kSPTF0p/servirovka5.jpg")
        await update.message.reply_photo(photo="https://i.ibb.co/Nn0WjSH/servirovka6.jpg")
        await update.message.reply_photo(photo="https://i.ibb.co/XJkJrjb/servirovka7.jpg")
        await update.message.reply_photo(photo="https://i.ibb.co/Jj9HZQH/servirovka8.jpg")
        await update.message.reply_photo(photo="https://i.ibb.co/L1kT4LV/servorovla2.jpg")
    except Exception as e:
        logger.error(f"Ошибка в send_servirovka_info: {e}")
    await show_main_menu(update)

# Функция для отправки информации о напитках и десертах
async def send_drinks_info(update: Update):
    try:
        await update.message.reply_photo(photo="https://i.ibb.co/t3KrLM8/drink.jpg")
        await update.message.reply_photo(photo="https://i.ibb.co/jg0PQ3j/drink1.jpg")
        await update.message.reply_photo(photo="https://i.ibb.co/xLVqBpy/drink2.jpg")
    except Exception as e:
        logger.error(f"Ошибка в send_drinks_info: {e}")
    await show_main_menu(update)

# Функция для отправки информации о фритюре
async def send_fryer_info(update: Update):
    try:
        await update.message.reply_photo(photo="https://i.ibb.co/VHMr1TN/fryer.jpg")
        await update.message.reply_photo(photo="https://i.ibb.co/ccqmscC/fryer2.jpg")
    except Exception as e:
        logger.error(f"Ошибка в send_fryer_info: {e}")
    await show_main_menu(update)

# Функция для отправки информации о "Остальное"
async def send_other_info(update: Update):
    try:
        await update.message.reply_photo(photo="https://i.ibb.co/QNDth9B/other.jpg")
        await update.message.reply_photo(photo="https://i.ibb.co/F8y5HCK/other2.jpg")
        await update.message.reply_photo(photo="https://i.ibb.co/QK897J3/other3.jpg")
        await update.message.reply_photo(photo="https://i.ibb.co/PQBGR0m/other4.jpg")
        await update.message.reply_photo(photo="https://i.ibb.co/xJLJ9HK/other5.jpg")
        await update.message.reply_photo(photo="https://i.ibb.co/d6N9bwt/other6.jpg")
        await update.message.reply_photo(photo="https://i.ibb.co/YkMzB2G/other7.jpg")
        await update.message.reply_photo(photo="https://i.ibb.co/8KVFDgk/other8.jpg")
        await update.message.reply_photo(photo="https://i.ibb.co/DQgkJMm/other9.jpg")
    except Exception as e:
        logger.error(f"Ошибка в send_other_info: {e}")
    await show_main_menu(update)

# Функция для отправки информации о сроках годности и пополнении
async def send_srok_godnosti_info(update: Update):
    try:
        await update.message.reply_photo(photo="https://i.ibb.co/ykrNNPv/srok2.jpg")
        await update.message.reply_photo(photo="https://i.ibb.co/0Dtvw1C/srok3.jpg")
    except Exception as e:
        logger.error(f"Ошибка в send_srok_godnosti_info: {e}")
    await show_main_menu(update)

# Функция для отправки информации о составах
async def send_sostav_info(update: Update):
    try:
        await update.message.reply_photo(photo="https://i.ibb.co/wgDSCcb/sostav.jpg")
        await update.message.reply_photo(photo="https://i.ibb.co/Sf4CzZd/sostav.png")
        await update.message.reply_photo(photo="https://i.ibb.co/PNknk2J/sostav2.jpg")
        await update.message.reply_photo(photo="https://i.ibb.co/hsw5zgF/sostav2.png")
        await update.message.reply_photo(photo="https://i.ibb.co/BCNFH0R/sostav3.jpg")
        await update.message.reply_photo(photo="https://i.ibb.co/x22kBDk/Srok1.jpg")
    except Exception as e:
        logger.error(f"Ошибка в send_sostav_info: {e}")
    await show_main_menu(update)

# Функция для отправки информации о приготовлении замеса
async def send_zames_info(update: Update):
    try:
        messages = [
            "Состав замеса OR - мешок муки, молочно-яичная смесь пакет, пакет перца.",
            "Состав замеса HS - мешок муки, пакет остро-пряной панировки. Срок годности замеса - 7 суток."
        ]
        for message in messages:
            await update.message.reply_text(message)
    except Exception as e:
        logger.error(f"Ошибка в send_zames_info: {e}")
    await show_main_menu(update)

# Функция для отображения главного меню
async def show_main_menu(update: Update):
    buttons = [["В главное меню"]]
    reply_markup = ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Выбери дальнейшее действие:", reply_markup=reply_markup)

# Основная функция для запуска бота
def main():
    logger.info("Бот запускается...")
    # Запускаем Flask сервер
    keep_alive()

    # Создаем приложение для бота
    application = Application.builder().token(TOKEN).build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    logger.info("Обработчик команды /start зарегистрирован.")

    # Регистрируем обработчики сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("Обработчик текстовых сообщений зарегистрирован.")

    # Запускаем бота
    logger.info("Бот запущен и ожидает сообщений...")
    application.run_polling()

if __name__ == "__main__":
    main()
