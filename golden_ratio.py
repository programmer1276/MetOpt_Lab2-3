import math


def f(x):
    """
    Целевая функция f(x) = x^2 - 2x + e^(-x).
    """
    return x ** 2 - 2 * x + math.e ** (-x)


def golden_section_search(a, b, eps=0.05):
    """
    Поиск минимума функции f(x) на отрезке [a, b] методом золотого сечения,
    с печатью итераций.

    Параметры:
    -----------
      a, b : float
          Концы исходного отрезка, где ищем минимум.
      eps : float
          Допустимая погрешность (по длине отрезка).

    Возвращает:
    -----------
      (x_min, f_min) : кортеж
          x_min - координата точки, где достигается минимум (приближённо),
          f_min - значение функции f(x_min).
    """
    # Коэффициент пропорции золотого сечения
    phi = (math.sqrt(5) - 1) / 2  # ~ 0.61803

    # Начальные точки x1 и x2
    x1 = b - phi * (b - a)
    x2 = a + phi * (b - a)

    iteration = 1
    print("Начальный отрезок: [{:.6f}, {:.6f}]".format(a, b))
    while (b - a) > eps:
        f1 = f(x1)
        f2 = f(x2)

        # Вывод текущей итерации
        print("\nИтерация {}:".format(iteration))
        print("  a = {:.6f}, b = {:.6f}".format(a, b))
        print("  x1 = {:.6f}, x2 = {:.6f}".format(x1, x2))
        print("  f(x1) = {:.6f}, f(x2) = {:.6f}".format(f1, f2))

        # Выбираем, какую часть отрезка отбросить
        if f1 > f2:
            # Минимум лежит в [x1, b]
            a = x1
            x1 = x2
            x2 = a + phi * (b - a)
        else:
            # Минимум лежит в [a, x2]
            b = x2
            x2 = x1
            x1 = b - phi * (b - a)

        iteration += 1

    # Когда (b-a) <= eps, считаем, что точность достигнута
    x_min = 0.5 * (a + b)
    f_min = f(x_min)

    print("\nДостигли заданной точности (b - a <= {}).".format(eps))
    print("Итоговый отрезок: [{:.6f}, {:.6f}]".format(a, b))
    return x_min, f_min


if __name__ == "__main__":
    a, b = 1.0, 1.5
    eps = 0.0001

    x_min, f_min = golden_section_search(a, b, eps)

    print("\nНайденный минимум:")
    print("  x ≈ {:.6f},  f(x) ≈ {:.6f}".format(x_min, f_min))

    # Для сравнения, значение функции на концах
    print("\nf(1.0)   = {:.6f}".format(f(1.0)))
    print("f(1.5)   = {:.6f}".format(f(1.5)))

