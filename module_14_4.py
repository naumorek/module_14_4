'''ЗЦель: написать простейшие CRUD функции для взаимодействия с базой данных.

Задача "Продуктовая база":
Подготовка:
Для решения этой задачи вам понадобится код из предыдущей задачи. Дополните его, следуя пунктам задачи ниже.

Дополните ранее написанный код для Telegram-бота:
Создайте файл crud_functions.py и напишите там следующие функции:
initiate_db, которая создаёт таблицу Products, если она ещё не создана при помощи SQL запроса. Эта таблица должна содержать следующие поля:
id - целое число, первичный ключ
title(название продукта) - текст (не пустой)
description(описание) - текст
price(цена) - целое число (не пустой)
get_all_products, которая возвращает все записи из таблицы Products, полученные при помощи SQL запроса.

Изменения в Telegram-бот:
В самом начале запускайте ранее написанную функцию get_all_products.
Измените функцию get_buying_list в модуле с Telegram-ботом, используя вместо обычной нумерации продуктов функцию get_all_products. Полученные записи используйте в выводимой надписи: "Название: <title> | Описание: <description> | Цена: <price>"
Перед запуском бота пополните вашу таблицу Products 4 или более записями для последующего вывода в чате Telegram-бота.
.'''



from aiogram import Bot,Dispatcher,executor,types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton
import asyncio
import crud_functions
from module14.crud_functions import get_all_products


api="7706788533:"
bot=Bot(token=api)
dp=Dispatcher(bot,storage=MemoryStorage())
kb_menu=ReplyKeyboardMarkup(              #главное меню
    keyboard=[
        [
            KeyboardButton(text="Расчитать"),
            KeyboardButton(text="info"),
            KeyboardButton(text="Купить")
        ]
    ], resize_keyboard=True
)

kb2=InlineKeyboardMarkup(   #выбор расчет калорий или вывод формулы
    inline_keyboard=[
        [InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')],
        [InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')]
    ]
)

kb_product=InlineKeyboardMarkup(   #выбор расчет калорий или вывод формулы
    inline_keyboard=[
        [InlineKeyboardButton(text='Product_A', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product_B', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product_C', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product_D', callback_data='product_buying')]
    ]
)







class UserState(StatesGroup):
    growth=State()
    weight=State()
    age=State()
@dp.message_handler(commands= ["start"])
async def main_start(message):
    await message.answer('Привет! \nВыберите опцию:', reply_markup=kb_menu)

@dp.message_handler(text="Расчитать")
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb2)

@dp.message_handler(text= "info")
async def get_info(message):
    await message.answer('Этот бот считает каллории для мужчин, со средней физической активностью')

@dp.message_handler(text="Купить")
async def get_buying_list(message):
    await message.answer('У вас есть возможность приобрести следующие товары:')
    all_product = get_all_products()
    for i in range(len(all_product)):    #Вынимаем из BD характеристики товаров, и соответствующие "фото"
        with open(f'{all_product[i][4]}', "rb") as img:
            await message.answer_photo(img, f'Название: {all_product[i][1]} | Описание: {all_product[i][2]} | Цена:{all_product[i][3]}')

    await message.answer('Для покупки товара нажмите на соответствующую кнопку',reply_markup=kb_product)



@dp.callback_query_handler(text= "calories")
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await call.answer()
    await UserState.age.set()     #ждем передачи сообщения от пользователя -> Состояние age


@dp.message_handler(state=UserState.age) #как только прило сообщение, происходит событие  UserState.age
async def set_growth(message,state):

        try:
            a=float(message.text)
            await state.update_data(age=message.text)   #записываем в дата с ключом age значение age

            await message.answer('Введите свой рост:')
            await UserState.growth.set()
        except Exception:
            await message.answer('неверный формат возраста')
            await message.answer('Введите свой возраст еще раз:')
            await UserState.age.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message,state):
    try:
        a = float(message.text)
        await state.update_data(growth=message.text)
        await message.answer('Введите свой вес')
        await UserState.weight.set()
    except Exception:
        await message.answer('неверный формат роста')
        await message.answer('Введите свой рост еще раз:')
        await UserState.growth.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    try:
        a = float(message.text)
        await state.update_data(weight=message.text)
        data = await state.get_data()   # получаем dat'у из записанных значений
        k_call=(10*float(data['weight'])+6.25*float(data['growth'])-5*float(data['age'])+5)*1.55
        await message.answer(f'Ваша норма каллорий: {k_call}')
        await state.finish()  #завершаем состояние
    except Exception:
        await message.answer('неверный формат веса')
        await message.answer('Введите свой вес еще раз:')
        await UserState.weight.set()
@dp.callback_query_handler(text= 'product_buying')
async def send_confirm_message(call):
    await call.message.answer('Продукт заказан')
    await call.answer()


@dp.callback_query_handler(text= 'formulas')
async def get_formulas(call):
    await call.message.answer('call=10*weight(kg)+6.25*growth(cm)-5*age(y)+5)*1.55')
    await call.answer()




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
