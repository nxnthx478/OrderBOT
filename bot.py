from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

API_TOKEN = "7989455537:AAFhLGq4Ia2JHiduhZ312YUYB0aZ0Bspz9I"
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

CRYPTO_URL = "http://t.me/send?start=IVW2kI5dmez9"

# === Старт ===
@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    kb = InlineKeyboardMarkup().add(InlineKeyboardButton("Понятно", callback_data="main_menu"))
    text = (
        "Привет, ты попал в автоматизированный магазин Eweiq'a.\n"
        "Ты оплачиваешь заказ, в комментарий пишешь свой юзернейм,\n"
        "с тобой свяжутся. Надеюсь, всё ясно!"
    )
    await msg.answer(text, reply_markup=kb)

# === Главное меню ===
@dp.callback_query_handler(lambda c: c.data == "main_menu")
async def main_menu(callback: types.CallbackQuery):
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("О магазине", callback_data="about"),
        InlineKeyboardButton("Услуги", callback_data="services")
    )
    await callback.message.edit_text("Выбери раздел:", reply_markup=kb)

# === О магазине ===
@dp.callback_query_handler(lambda c: c.data == "about")
async def about(callback: types.CallbackQuery):
    text = (
        "О магазине!\n"
        "Этот бот предназначен для принятия заказов от тех, у кого другой часовой пояс или лень ждать ответа.\n"
        "После оплаты заказ АВТОМАТИЧЕСКИ передаётся Эвейку."
    )
    back = InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️ Назад", callback_data="main_menu"))
    await callback.message.edit_text(text, reply_markup=back)

# === Услуги ===
@dp.callback_query_handler(lambda c: c.data == "services")
async def services(callback: types.CallbackQuery):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("деф", callback_data="def"),
        InlineKeyboardButton("сват (4$)", callback_data="svat"),
        InlineKeyboardButton("донос (3$)", callback_data="donos"),
        InlineKeyboardButton("⬅️ Назад", callback_data="main_menu")
    )
    await callback.message.edit_text("Выбери услугу:", reply_markup=kb)

# === деф ===
@dp.callback_query_handler(lambda c: c.data == "def")
async def def_menu(callback: types.CallbackQuery):
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("3$ (1 месяц)", callback_data="pay_def_month"),
        InlineKeyboardButton("5$ (навсегда)", callback_data="pay_def_lifetime"),
        InlineKeyboardButton("⬅️ Назад", callback_data="services")
    )
    await callback.message.edit_text("Выбери вариант:", reply_markup=kb)

# === Оплата DEF ===
@dp.callback_query_handler(lambda c: c.data in ["pay_def_month", "pay_def_lifetime"])
async def pay_def(callback: types.CallbackQuery):
    kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton("💸 Оплатить", url=CRYPTO_URL),
        InlineKeyboardButton("✅ Я оплатил", callback_data="paid")
    )
    await callback.message.edit_text("После оплаты нажми кнопку 'Я оплатил'", reply_markup=kb)

# === Сват ===
@dp.callback_query_handler(lambda c: c.data == "svat")
async def svat(callback: types.CallbackQuery):
    kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton("💸 Оплатить", url=CRYPTO_URL),
        InlineKeyboardButton("✅ Я оплатил", callback_data="paid")
    )
    await callback.message.edit_text(
        "Обязательно прикрепить номер телефона, ФИО, город.\n\nПосле оплаты нажми 'Я оплатил'.",
        reply_markup=kb
    )

# === Донос ===
@dp.callback_query_handler(lambda c: c.data == "donos")
async def donos(callback: types.CallbackQuery):
    kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton("💸 Оплатить", url=CRYPTO_URL),
        InlineKeyboardButton("✅ Я оплатил", callback_data="paid")
    )
    await callback.message.edit_text(
        "Обязательно прикрепить ФИО, город, номер телефона.\n\nПосле оплаты нажми 'Я оплатил'.",
        reply_markup=kb
    )

# === Я оплатил ===
@dp.callback_query_handler(lambda c: c.data == "paid")
async def paid(callback: types.
               CallbackQuery):
    await callback.message.edit_text(
        "Напиши @eweiq и укажи, что ты оплатил, а также какую услугу выбрал.\n\n"
        "Только после этого заказ будет обработан."
    )

# === Запуск ===
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)