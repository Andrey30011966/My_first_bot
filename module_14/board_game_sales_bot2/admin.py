import sqlite3

con = sqlite3.connect('admin_db.db')
cursor = con.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Admins(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    first_name TEXT NOT NULL,
    block INTEGER NOT NULL
    )
    ''')

def add_user(user_id, username, first_name):
    check_user = cursor.execute('SELECT * FROM Admins WHERE id = ?', (user_id,))

    if check_user.fetchone() is None:
        cursor.execute('INSERT INTO Admins VALUES(?, ?, ?, ?)', (user_id, username, first_name, 0))
        con.commit()

def show_users():
    admins_list = cursor.execute('SELECT * FROM Admins')
    message = ''
    for admin in admins_list:
        message += f'{admin[0]} @{admin[1]} {admin[2]} \n'
    con.commit()
    return message

def show_stat():
    count_admin = cursor.execute('SELECT COUNT(*) FROM Admins').fetchone()
    con.commit()
    return count_admin[0]

def add_to_block(input_id):
    cursor.execute('UPDATE Admins SET block = ? WHERE id = ?', (1, input_id,))
    con.commit()

def remove_block(input_id):
    cursor.execute('UPDATE Admins SET block = ? WHERE id = ?', (0, input_id,))
    con.commit()

def check_to_block(input_id):
    admins = cursor.execute(f'SELECT block FROM Admins WHERE id = {input_id}').fetchone()
    con.commit()
    return admins[0]