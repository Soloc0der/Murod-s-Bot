from aiogram import types
from states.main import ShopState
from loader import dp, db
from aiogram.dispatcher.storage import FSMContext
from keyboards.default.menu import numbers


@dp.message_handler(state=ShopState.product)
async def product_detail(message: types.Message, state: FSMContext):
    product_name = message.text
    data = db.get_product_data(name=product_name)
    msg = f"<b>{product_name} - {data[-2]} so'm</b>\n\n{data[2]}"
    await state.update_data({"product_name": product_name, "product_price": data[-2], "product_id": data[0]})
    await message.answer_photo(photo=data[-3], caption=msg, parse_mode="html", reply_markup=numbers)
    await ShopState.next()
