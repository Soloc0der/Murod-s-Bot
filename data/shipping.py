from aiogram import types
from aiogram.types import LabeledPrice






REGULAR_SHIPPING = types.ShippingOption(
    id='post_reg',
    title="Emu (3 kun)",
    prices=[
        LabeledPrice(
            'Maxsus quti', 500000),
        LabeledPrice(
            '3 ish kunida yetkazish', 1500000),
    ]
)

FAST_SHIPPING = types.ShippingOption(
    id='post_fast',
    title='Express pochta (1 kun)',
    prices=[
        LabeledPrice(
            '1 kunda yetkazish', 3000000),
    ]
)

PICKUP_SHIPPING = types.ShippingOption(id='pickup',
                                       title="Do'kondan olib ketish",
                                       prices=[
                                           LabeledPrice("Yetkazib berishsiz", -2000000)
                                       ])