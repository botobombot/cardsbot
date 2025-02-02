from database import Character

def calculate_damage(attacker, defender):
    damage = max(attacker.attack - defender.defense, 0)
    defender.take_damage(damage)
    return damage

def fight(character1, character2):
    turn = 0
    while character1.is_alive() and character2.is_alive():
        if turn % 2 == 0:
            damage = calculate_damage(character1, character2)
            print(f"{character1.name} атакует {character2.name} и наносит {damage} урона. Осталось здоровья: {character2.health}")
        else:
            damage = calculate_damage(character2, character1)
            print(f"{character2.name} атакует {character1.name} и наносит {damage} урона. Осталось здоровья: {character1.health}")
        turn += 1

    if character1.is_alive():
        return f"{character1.name} победил!"
    else:
        return f"{character2.name} победил!"
    