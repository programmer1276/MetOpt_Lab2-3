import math


def f(x):
    """
    Исходная функция f(x) = x^2 - 2x + e^(-x).
    """
    return x ** 2 - 2 * x + math.e ** (-x)


def quadratic_approximation_method(x1=1.0, dx=0.25, eps1=0.01, eps2=0.01, max_iter=50):
    """
    Поиск минимума функции f(x)=x^2 - 2x + e^(-x) методом квадратичной аппроксимации,
    с выводом информации о каждом шаге.

    Параметры:
      x1         : float
          Начальная точка (x_1).
      dx         : float
          Шаг Delta_x.
      eps1, eps2 : float
          Критерии точности:
              - eps1 для относительной разницы значений функции,
              - eps2 для относительной разницы аргументов.
      max_iter   : int
          Максимальное число итераций.

    Возвращает:
      (x_star, f_star) : (float, float)
          x_star - найденное приближение минимума,
          f_star - значение функции f(x_star).
    """
    # 1) Начальная точка x1, строим x2 = x1 + dx
    x2 = x1 + dx

    # Значения функции в x1, x2
    f1 = f(x1)
    f2 = f(x2)

    iteration = 0

    print(f"Инициализация:\n  x1={x1:.6f}, f(x1)={f1:.6f},  x2={x2:.6f}, f(x2)={f2:.6f}")

    while iteration < max_iter:
        iteration += 1

        # 2) Определяем x3:
        if f1 > f2:
            # Если f(x1) > f(x2), x3 = x1 + 2*dx
            x3 = x1 + 2 * dx
        else:
            # Иначе x3 = x1 - dx
            x3 = x1 - dx

        f3 = f(x3)

        # Определяем F_min и x_min
        F_min = min(f1, f2, f3)
        if F_min == f1:
            x_min = x1
        elif F_min == f2:
            x_min = x2
        else:
            x_min = x3

        # 3) Формула вершины квадратичной аппроксимации
        x1_sq = x1 * x1
        x2_sq = x2 * x2
        x3_sq = x3 * x3

        numerator = ((x2_sq - x3_sq) * f1 +
                     (x3_sq - x1_sq) * f2 +
                     (x1_sq - x2_sq) * f3)

        denominator = 2.0 * (
                (x2 - x3) * f1
                + (x3 - x1) * f2
                + (x1 - x2) * f3
        )

        # Чтобы избежать деления на ноль
        if abs(denominator) < 1e-14:
            print(f"\nИтерация {iteration}: denominator почти 0 => выход из метода.")
            # Возвращаем лучшую из x1,x2,x3
            best_point, best_val = (x1, f1)
            if f2 < best_val:
                best_point, best_val = (x2, f2)
            if f3 < best_val:
                best_point, best_val = (x3, f3)
            return best_point, best_val

        bar_x = numerator / denominator
        f_bar = f(bar_x)

        # Вывод текущей итерации
        print(f"\nИтерация {iteration}:")
        print(f"  x1={x1:.6f}, f1={f1:.6f};  x2={x2:.6f}, f2={f2:.6f};  x3={x3:.6f}, f3={f3:.6f}")
        print(f"  bar_x={bar_x:.6f}, f(bar_x)={f_bar:.6f}")

        # 4) Критерии остановки
        #    |F_min - f(bar_x)| / |f(bar_x)| < eps1
        #    |x_min - bar_x|   / |bar_x|    < eps2

        # Защита от деления на 0
        if abs(f_bar) < 1e-14:
            crit_value = 0
        else:
            crit_value = abs(F_min - f_bar) / abs(f_bar)

        if abs(bar_x) < 1e-14:
            crit_point = 0
        else:
            crit_point = abs(x_min - bar_x) / abs(bar_x)

        print(f"  Относительная разница значений = {crit_value:.6f}")
        print(f"  Относительная разница аргументов = {crit_point:.6f}")

        if crit_value < eps1 and crit_point < eps2:
            print("  Достигнуты критерии останова.")
            return bar_x, f_bar

        # 5) Если нет, переформируем тройку (x1, x2, x3),
        #    где центр - та точка, у которой значение f меньше.

        # Текущее f(x_min):
        current_fmin = f(x_min)
        if f_bar < current_fmin:
            # bar_x даёт меньшее значение => bar_x - "центральная"
            # Упрощённая стратегия (не самая изощрённая):

            # Случай: x_min < bar_x
            if x_min < bar_x:
                # (x1, x2, x3) = (x_min, bar_x, ...)
                # Выберем третью точку среди {x2, x3, x1} которая > bar_x
                # Но у нас x2 или x3 менялись.
                # Чтобы не усложнять сильно, просто берём x1, x2, x3 как
                # (x_min, bar_x, x2) если x2 > bar_x иначе (x_min, bar_x, x3).
                # Сохраним "под рукой" f2, f3

                if x2 > bar_x:
                    x1, x2, x3 = x_min, bar_x, x2
                    f1, f2, f3 = f(x1), f(bar_x), f(x2)
                else:
                    x1, x2, x3 = x_min, bar_x, x3
                    f1, f2, f3 = f(x1), f(bar_x), f(x3)
            else:
                # bar_x < x_min
                if x3 < bar_x:
                    x1, x2, x3 = x3, bar_x, x_min
                    f1, f2, f3 = f(x1), f(bar_x), f(x_min)
                else:
                    x1, x2, x3 = bar_x, x_min, x2
                    f1, f2, f3 = f(bar_x), f(x_min), f(x2)
        else:
            # x_min даёт меньшее значение => x_min - "центральная"
            if bar_x < x_min:
                x1, x2, x3 = bar_x, x_min, x2
                f1, f2, f3 = f(bar_x), f(x_min), f(x2)
            else:
                x1, x2, x3 = x_min, bar_x, x2
                f1, f2, f3 = f(x_min), f(bar_x), f(x2)

        # Перед следующей итерацией можно пересчитать dx,
        # но зачастую это не делают (зависит от варианта метода).

    # Если за max_iter не вышли по критериям — вернём лучшую точку
    print("\nДостигнуто max_iter без выполнения критериев остановки.")
    all_points = [(x1, f1), (x2, f2), (x3, f3)]
    best = min(all_points, key=lambda p: p[1])
    return best[0], best[1]


# =================================================
# Пример использования
if __name__ == "__main__":
    x_star, f_star = quadratic_approximation_method(
        x1=1.0,  # Начальное x1
        dx=0.25,  # Шаг
        eps1=0.0001,  # Критерий по f
        eps2=0.0001,  # Критерий по x
        max_iter=20  # Ограничение итераций
    )

    print("\n--- Результат ---")
    print(f"Найденная точка: x* = {x_star:.6f}")
    print(f"Значение функции: f(x*) = {f_star:.6f}")

    # Проверка значений на концах [1,1.5]
    print(f"f(1.0) = {f(1.0):.6f}")
    print(f"f(1.5) = {f(1.5):.6f}")
