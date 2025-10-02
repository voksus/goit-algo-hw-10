import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import quad

# Очистка екрану
print('\033c')

# --- 1. Налаштування та функція "Торнадо" ---

def f(x):
    """Функція "Торнадо" для інтегрування."""
    return  np.sin(x**2) / x**2 + 1.5

a = -5.0  #  Ліва межа
b =  5.0  # Права межа

# Налаштування методу Монте-Карло
N_POINTS   = 500_000      # Кількість випадкових точок
POINT_SIZE = .2           # Розмір точок на графіку

# Максимальне значення f(x) на [-5, 5] ~ 2.5 (при x=0). 
Y_MAX = 3.0 
Y_MIN = 0.0 

# Генеруємо випадкові точки у прямокутнику [a, b] x [Y_MIN, Y_MAX]
x_random = np.random.uniform(a, b, N_POINTS)
y_random = np.random.uniform(Y_MIN, Y_MAX, N_POINTS)

# Рахуємо, скільки точок потрапило ПІД криву
points_under_curve = y_random < f(x_random)
N_HIT = np.sum(points_under_curve)

# Площа прямокутника
RECT_AREA = (b - a) * (Y_MAX - Y_MIN)

# Оцінка інтеграла Монте-Карло
integral_monte_carlo = RECT_AREA * (N_HIT / N_POINTS)


# --- 3. Точна математична перевірка ---

# Функція quad для обчислення інтеграла з високою точністю (реальне значення)
def f_scalar(x):
    if x == 0:
        return 2.5
    return np.sin(x**2) / x**2 + 1.5

integral_exact_result = quad(f_scalar, a, b)
integral_exact = integral_exact_result[0]
scipy_error = integral_exact_result[1] # Похибка, яку гарантує SciPy

# --- 4. Оцінка похибки Монте-Карло ---

# Абсолютна похибка: різниця між оцінкою та "точним" значенням
absolute_error = abs(integral_monte_carlo - integral_exact)

# Відносна похибка: абсолютна похибка, поділена на "точне" значення
relative_error = absolute_error / abs(integral_exact)


# --- 5. Візуалізація результату ---

x_plot = np.linspace(a - 0.5, b + 0.5, 400)
y_plot = f(x_plot) # Використовуємо векторизовану функцію

fig, ax = plt.subplots(figsize=(10, 6))

# 5.1. Малювання випадкових точок (Монте-Карло)
ax.scatter(x_random[~points_under_curve], y_random[~points_under_curve], 
           color='red', s=POINT_SIZE, alpha=0.1, label=f'Точки над кривою (Miss={N_POINTS - N_HIT:,})'.replace(',', '\''))
ax.scatter(x_random[points_under_curve], y_random[points_under_curve], 
           color='green', s=POINT_SIZE, alpha=0.3, label=f'Точки під кривою (Hit={N_HIT:,})'.replace(',', '\''))

# 5.2. Малювання самої функції
ax.plot(x_plot, y_plot, 'b', linewidth=2, label=R'$f(x) = \frac{\sin(x^2)}{x^2} + 1.5$')

# 5.3. Налаштування графіка та вивід результатів
ax.set_xlim([x_plot[0], x_plot[-1]])
ax.set_ylim([Y_MIN, Y_MAX])
ax.set_xlabel('x')
ax.set_ylabel('f(x)')

ax.axvline(x=a, color='gray', linestyle='--')
ax.axvline(x=b, color='gray', linestyle='--')
ax.set_title(f'Метод Монте-Карло для оцінки інтеграла (N = {N_POINTS:,})'.replace(',', '\''))

# Вивід результатів у вигляді тексту на графіку
ax.text(0.5, 0.95, 
        f'Оцінка Монте-Карло: {integral_monte_carlo:.4f}\n'
        f'Точне значення (SciPy): {integral_exact:.4f}\n'
        f'Абсолютна похибка: {absolute_error:.4e}\n'
        f'Відносна похибка: {relative_error:.2%}',
        transform=ax.transAxes, fontsize=12,
        verticalalignment='top',
        bbox=dict(boxstyle="round", facecolor='yellow', alpha=0.5))

plt.legend(loc='lower left')
plt.grid(True)
plt.show()