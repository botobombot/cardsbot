import sqlite3

class Character:
    def __init__(self, name, attack, defense, health):
        self.name = name
        self.attack = attack
        self.defense = defense
        self.health = health

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def is_alive(self):
        return self.health > 0

class User:
    def __init__(self, user_id, own, clan, bio):
        self.user_id = user_id
        self.own = own
        self.clan = clan
        self.bio = bio

def create_database():
    conn = sqlite3.connect('characters.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS characters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            attack INTEGER NOT NULL,
            defense INTEGER NOT NULL,
            health INTEGER NOT NULL
        )
    ''')
 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            own INTEGER NOT NULL,
            clan TEXT NOT NULL,
            bio TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

def add_user(user_id):
    conn = sqlite3.connect('characters.db')
    cursor = conn.cursor()

    cursor.execute('INSERT OR IGNORE INTO users (user_id, own, clan, bio) VALUES (?, 0, "None", "None")', (user_id,))

    conn.commit()
    conn.close()

def get_user(user_id):
    conn = sqlite3.connect('characters.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    conn.close()

    if user:
        return User(user[0], user[1], user[2], user[3])
    else:
        return None


def add_bio(user_id, bio): #ПРОТЕСТИРОВАТЬ НАДО
    conn = sqlite3.connect('characters.db')
    cursor = conn.cursor()

    cursor.execute('INSERT OR IGNORE INTO users (bio) VALUES (, , , ?) WHERE user_id = ?', (bio, user_id,))

    conn.commit()
    conn.close()

def get_all_users():
    conn = sqlite3.connect('characters.db')
    cursor = conn.cursor()

    cursor.execute('SELECT user_id FROM users')
    users = cursor.fetchall()

    conn.close()

    return [user[0] for user in users]

def add_character(name, attack, defense, health):
    conn = sqlite3.connect('characters.db')
    cursor = conn.cursor()

    info = cursor.execute('SELECT name FROM characters WHERE name=?', (name, )).fetchone()
    #Если запрос вернул 0 строк, то...
    if info is None: 
        cursor.execute('''
            INSERT INTO characters (name, attack, defense, health)
            VALUES (?, ?, ?, ?)
            ''', (name, attack, defense, health))
    else:
            return True

    conn.commit()
    conn.close()

def get_characters_with_ids():
    conn = sqlite3.connect('characters.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id, name FROM characters')
    characters = cursor.fetchall()

    conn.close()

    return characters


def get_character(character_id):
    conn = sqlite3.connect('characters.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM characters WHERE id = ?', (character_id,))
    character = cursor.fetchone()

    conn.close()

    if character:
        return Character(character[1], character[2], character[3], character[4])
    else:
        return None

def get_all_characters():
    conn = sqlite3.connect('characters.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM characters')
    characters = cursor.fetchall()

    conn.close()

    return characters

# Создаем базу данных и добавляем несколько персонажей для примера
create_database()
add_character("Джотаро (JJBA)", 10, 7, 150)
add_character("Дазай (BSD)", 5, 1, 40)
add_character("Артурия (Fate Series)", 999, 999, 999)
add_character("Демифинд (SMT)", 1, 1, 1)
add_character("Наруто (Naruto)", 15, 5, 150)
add_character("Фрауден (Реал Лайф)", 1, 0, 1)

