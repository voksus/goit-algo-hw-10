# Очистка екрану
print('\033c')

# Головні налаштування
# Кольори
RESET  = '\033[0m'
BOLD   = '\033[1m'
DIM    = '\033[2m'
RED    = '\033[31m'
GREEN  = '\033[32m'
YELLOW = '\033[33m'
CYAN   = '\033[36m'
# Шаблони
CENT   = f'{DIM+YELLOW}₵{RESET}'
COIN_DECOR    = f'{BOLD+CYAN}{{val:2}}{RESET}{CENT}'
PAYMENT_DECOR = f'{BOLD+GREEN}{{payment:5}}{RESET}{CENT}'
# Монети для тесту алгоритмів
COINS_BASE = []

def p_decor(payment: int) -> str:
    return PAYMENT_DECOR.format(payment=payment)

def c_decor(val) -> str:
    return COIN_DECOR.format(val=val)

# 1 підзадача: жадібний алгоритм (швидке рішення)
def find_coins_greedy(amount: int) -> dict[int,int]:
    list.sort(COINS_BASE, reverse=True)
    result: dict[int,int] = {}
    for coin in COINS_BASE:
        count = amount // coin
        # Якщо монета не використана, то в словник її не додаємо
        if count > 0:
            result[coin] = count
            amount -= count * coin
    return result

# 2 підзадача: знаходження мінімальної кількоті монет
def find_min_coins(amount: int) -> list[dict[int, int]]:
    """
    Знаходить усі оптимальні (з найменшою кількістю монет) комбінації
    для видачі решти заданої суми, використовуючи динамічне програмування.
    """
    
    # min_coins_count[i] зберігає мінімальну кількість монет для суми i.
    # Значення 'amount + 1' дає більшим за будь-який можливий результат.
    # (імітуємо нескінченність для підстановки меньших кількостей монет)
    min_coins_count = [amount + 1] * (amount + 1)

    # combinations[i] зберігає список усіх оптимальних комбінацій для суми i.
    combinations: list[dict] = [[] for _ in range(amount + 1)]

    # Базовий випадок: 0 монет для суми 0
    min_coins_count[0] = 0
    combinations[0] = [{}]

    # Ітеративно розв'язуємо підзадачі від 1 до `amount`
    for i in range(1, amount + 1):
        for coin in COINS_BASE:
            if i >= coin:
                prev_amount = i - coin
                
                # Кількість монет, якщо ми використаємо поточну монету
                new_count = min_coins_count[prev_amount] + 1
                
                # 1. Знайдено кращий (менший) результат
                if new_count < min_coins_count[i]:
                    min_coins_count[i] = new_count
                    combinations[i] = [] # Очищуємо старі, гірші комбінації
                    
                    # Будуємо нові комбінації на основі оптимальних для `prev_amount`
                    for prev_comb in combinations[prev_amount]:
                        new_comb = prev_comb.copy()
                        new_comb[coin] = new_comb.get(coin, 0) + 1
                        combinations[i].append(new_comb)

                # 2. Знайдено альтернативний оптимальний результат
                elif new_count == min_coins_count[i]:
                    # Додаємо нові комбінації до існуючих
                    for prev_comb in combinations[prev_amount]:
                        new_comb = prev_comb.copy()
                        new_comb[coin] = new_comb.get(coin, 0) + 1
                        
                        # Уникаємо дублікатів, якщо вони можуть виникнути
                        if new_comb not in combinations[i]:
                             combinations[i].append(new_comb)

    # Повертаємо список оптимальних комбінацій для заданої суми
    return combinations[amount]


if __name__ == '__main__':
    # 1 підзадача з реалізацією жадібного алгоритму
    print('1. Функція жадібного алгоритму :')
    COINS_BASE = [1, 2, 5, 10, 25, 50]
    print(f'{DIM}Наявні монети: {",".join(f"{BOLD+RED}{c}{RESET+DIM}" for c in COINS_BASE)}{RESET}')
    payments = [93, 111, 113, 186, 256]
    for i, payment in enumerate(payments):
        coins_dict = find_coins_greedy(payment)
        # Трошки віддекоруємо вивід
        print(f'{i+1:4}){p_decor(payment)} = {', '.join(f"{c_decor(k)}: {v}" for k,v in coins_dict.items())}')
    
    # 2 підзадача зі знаходженням мінімальної кількості монет
    print(f'\n\n{""}2. Функція для знаходження мінімальної кількості монет :')
    COINS_BASE    = [1, 3, 4, 6, 10, 25]
    print(f'{DIM}Наявні монети: {",".join(f"{BOLD+RED}{c}{RESET+DIM}" for c in COINS_BASE)}{RESET}')
    payments = [7, 12, 32, 66, 82]
    for i, payment in enumerate(payments):
        min_coins_solutions = find_min_coins(payment)
        # Цей теж декоруємо
        solutions_str = f' {YELLOW}або{RESET} '.join([
            ', '.join(f'{c_decor(k)}: {v}' for k, v in sorted(solution.items()))
            for solution in min_coins_solutions
        ])
        print(f'{i+1:4}){p_decor(payment)} = {solutions_str}')