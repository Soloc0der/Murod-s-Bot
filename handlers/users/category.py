from aiogram import types
from states.main import ShopState
from loader import dp, db
from aiogram.dispatcher.storage import FSMContext
from keyboards.default.menu import make_products_markup


@dp.message_handler(state=ShopState.category)
async def get_products_by_category(message: types.Message, state: FSMContext):
    category_name = message.text
    cat_id = db.get_category(name=category_name)[0]
    markup = make_products_markup(cat_id)
    await state.update_data({
        "cat_id": cat_id
    })
    await message.answer(f"{category_name} kategoriyasidagi mahsulotlar", reply_markup=markup)
    await ShopState.next()

