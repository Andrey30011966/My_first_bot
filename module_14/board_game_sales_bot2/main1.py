import sqlite3

def add_products():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    # Добавляем несколько продуктов
    products = [
        ("Продукт 1", "Описание 1", 100),
        ("Продукт 2", "Описание 2", 200),
        ("Продукт 3", "Описание 3", 300),
        ("Продукт 4", "Описание 4", 400),
    ]

    cursor.executemany('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)', products)

    conn.commit()
    conn.close()

add_products()