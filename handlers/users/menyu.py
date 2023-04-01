from aiogram import types
from states.main import ShopState
from loader import dp, db
from aiogram.dispatcher.storage import FSMContext
from keyboards.default.menu import cats_markup



@dp.message_handler(text="Menyu 🍲🍢", state="*")
async def bot_echo(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    cart_id = db.select_cart(user_id=user_id)[0]
    await state.update_data({"cart_id": cart_id})
    await message.answer("Xo'sh, buyurtmaga o'tamizmi, sizni issiq taomlarimiz kutmoqda 👨🏻‍🍳🔥\n\nTaomlarga o'tish uchun sahifani tanlang...", reply_markup=cats_markup)
    await ShopState.category.set()
