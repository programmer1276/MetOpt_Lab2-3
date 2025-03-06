import math


def f(x):
    """Функция f(x) = x^2 - 2x + e^{-x}."""
    return x ** 2 - 2 * x + math.e ** (-x)


def fprime(x):
    """Первая производная f'(x) = 2x - 2 - e^{-x}."""
    return 2 * x - 2 - math.e ** (-x)


def bisection_for_derivative(a, b, eps=0.05):
    """
    Метод половинного деления для уравнения f'(x)=0 на отрезке [a,b].
    eps — требуемая точность по x (длина отрезка).
    Предполагается, что f'(a) и f'(b) имеют разные знаки.

    Возвращает:
      (x_left, x_right) — итоговый отрезок, где лежит корень f'(x)=0,
      длина которого < eps.
    """
    fa = fprime(a)
    fb = fprime(b)

    # Убедимся, что на концах действительно разные знаки
    if fa * fb > 0:
        raise ValueError("На концах [a,b] знаки f'(x) совпадают; бисекция неприменима.")

    left, right = a, b

    while (right - left) >= eps:
        mid = 0.5 * (left + right)
        fmid = fprime(mid)

        # Определяем, с какой стороны корень
        if fa * fmid <= 0:
            # Корень лежит в [left, mid]
            right = mid
            fb = fmid
        else:
            # Корень в [mid, right]
            left = mid
            fa = fmid

    return (left, right)


# ==== Основная часть ====

a, b = 1.0, 1.5
eps = 0.0001

print("Ищем экстремум f(x) = x^2 - 2x + e^(-x) на [1, 1.5].")
print("Метод бисекции для решения f'(x)=0 с точностью по x =", eps)

# 1) Проверяем знаки производной на концах
fpa = fprime(a)
fpb = fprime(b)
print(f"f'(1)   = {fpa:.6f}")
print(f"f'(1.5) = {fpb:.6f}")

if fpa * fpb < 0:
    # 2) Запускаем метод половинного деления
    x_left, x_right = bisection_for_derivative(a, b, eps)
    # Берём середину финального отрезка как приближённый корень
    x_star = 0.5 * (x_left + x_right)

    print(f"\nНайден отрезок [{x_left:.6f}, {x_right:.6f}] длиной {x_right - x_left:.6f}.")
    print(f"Приближённая стационарная точка (корень f'(x)=0): x* ≈ {x_star:.6f}.\n")

    # 3) Проверяем тип экстремума (f''(x) = 2 + e^(-x) > 0 => минимум)
    print("Поскольку f''(x) = 2 + e^(-x) > 0 на любом x, это точка минимума.")

    # 4) Сравним f(x) на концах и в точке x_star
    fa_val = f(a)
    fb_val = f(b)
    fx_star = f(x_star)

    print(f"f(1)      = {fa_val:.6f}")
    print(f"f(1.5)    = {fb_val:.6f}")
    print(f"f(x_star) = {fx_star:.6f}")

    # Ищем минимум и максимум на отрезке [1, 1.5]
    points = [(a, fa_val), (x_star, fx_star), (b, fb_val)]
    points_sorted = sorted(points, key=lambda p: p[1])  # сортируем по значению f(x)

    x_min, f_min = points_sorted[0]
    x_max, f_max = points_sorted[-1]

    print(f"\nМинимум на отрезке: x={x_min:.6f}, f(x)={f_min:.6f}")
    print(f"Максимум на отрезке: x={x_max:.6f}, f(x)={f_max:.6f}")

else:
    print("f'(x) на концах [1, 1.5] имеет одинаковый знак: стационарной точки внутри нет.")
    # В таком случае минимум/максимум - только на концах.
    fa_val = f(a)
    fb_val = f(b)
    if fa_val < fb_val:
        print("Функция убывает или имеет минимум в x=1, максимум в x=1.5.")
    else:
        print("Функция возрастает или имеет минимум в x=1.5, максимум в x=1.")
