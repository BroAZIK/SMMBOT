from telegram import InlineKeyboardButton
from settings import *

# start_but = [
#     ["Hamyon ochish 💳", "Natijalar🔝"],
#     ["Pul ishlash 💰"],
#     ["Malumot ℹ️", "Statistika 📊"]
# ]

start_but = [
    [InlineKeyboardButton("Malumot ℹ️", callback_data="info"), InlineKeyboardButton("Statistika 📊", callback_data="stats")]
]

non_sub_but = [
    [InlineKeyboardButton("Obuna bo'lish➕",url=f'https://t.me/{CHANNEL_ID2}')],
    [InlineKeyboardButton("Tekshirish✅", callback_data="check" )]
]

admin_start_but = [
    ["Item qo'shish➕", "Olib tashlash🗑"],
    ["Statistika📊"]
]

back_but = [
    ["Ortga⬅️"]
]