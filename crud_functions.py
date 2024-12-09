'''Задача "Продуктовая база":
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

Пример результата выполнения программы:
Добавленные записи в таблицу Product и их отображение в Telegram-bot:



Примечания:
Название продуктов и картинок к ним можете выбрать самостоятельно. (Минимум 4)
Файлы module_14_4.py, crud_functions.py, а также файл с базой данных и таблицей Products загрузите на ваш GitHub репозиторий. В решении пришлите ссылку на него.
Успехов!'''
import sqlite3


def initiate_db():
    connection = sqlite3.connect('Products.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL,
    img_name TEXT
    )    
    ''')
    connection.commit()
    connection.close()


def set_product(title,description,price,img_name):
    connection = sqlite3.connect('Products.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Users (title,description,price, img_name) VALUES (?,?,?,?)",
                   (f'{title}', f'{description}', f'{price}',f'{img_name}'))
    connection.commit()
    connection.close()




def get_all_products():
    connection = sqlite3.connect('Products.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Users")
    total = cursor.fetchall()
    connection.close()
    return total


#initiate_db()
#set_product("Product_A",'Самый лучший комплекс_A',100, "A.jpg")
#set_product("Product_B",'Самый лучший комплекс_B',200, "B.jpg")
#set_product("Product_C",'Самый лучший комплекс_C',300, "C.jpg")
#set_product("Product_D",'Самый лучший комплекс_D',400, "D.jpg")

