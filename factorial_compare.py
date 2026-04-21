"""
Сравнение производительности различных реализаций факториала.

Программа сравнивает четыре реализации факториала:
- math.factorial (эталон)
- итеративная
- рекурсивная
- мемоизированная

Результаты выводятся в виде таблицы и графика.
"""

import math
import timeit
from typing import List, Tuple, Callable
import matplotlib.pyplot as plt


def factorial_recursive(n: int) -> int:
    """Вычислить факториал рекурсивным способом.

    Функция вызывает саму себя для вычисления факториала.
    Базовый случай: при n <= 1 возвращает 1.

    Args:
        n (int): Неотрицательное целое число.

    Returns:
        int: Факториал числа n.

    Raises:
        ValueError: Если n < 0, так как факториал определён только
            для неотрицательных чисел.

    Examples:
        >>> factorial_recursive(5)
        120
        >>> factorial_recursive(0)
        1
    """
    if n < 0:
        raise ValueError("Факториал определён только для неотрицательных чисел")
    if n <= 1:
        return 1
    return n * factorial_recursive(n - 1)


def factorial_iterative(n: int) -> int:
    """Вычислить факториал итеративным способом.

    Функция использует цикл for для последовательного умножения чисел
    от 2 до n. Этот подход эффективнее рекурсии по памяти.

    Args:
        n (int): Неотрицательное целое число.

    Returns:
        int: Факториал числа n.

    Raises:
        ValueError: Если n < 0.

    Examples:
        >>> factorial_iterative(5)
        120
        >>> factorial_iterative(0)
        1
    """
    if n < 0:
        raise ValueError("Факториал определён только для неотрицательных чисел")

    result: int = 1
    for i in range(2, n + 1):
        result *= i
    return result


# Кэш для хранения ранее вычисленных значений факториала.
# Используется функцией factorial_memoized для оптимизации повторных вызовов.
_factorial_cache: dict[int, int] = {0: 1, 1: 1}


def factorial_memoized(n: int) -> int:
    """Вычислить факториал с использованием мемоизации.

    Функция сохраняет вычисленные значения в словаре-кэше.
    При повторном вызове с тем же аргументом значение берётся из кэша,
    что значительно ускоряет работу при многократных вычислениях.

    Args:
        n (int): Неотрицательное целое число.

    Returns:
        int: Факториал числа n.

    Raises:
        ValueError: Если n < 0.

    Examples:
        >>> factorial_memoized(5)
        120
        >>> factorial_memoized(5)  # Берётся из кэша
        120
    """
    global _factorial_cache
    if n < 0:
        raise ValueError("Факториал определён только для неотрицательных чисел")

    if n not in _factorial_cache:
        _factorial_cache[n] = n * factorial_memoized(n - 1)

    return _factorial_cache[n]


def measure_time(func: Callable[[int], int], n: int, number: int = 10) -> float:
    """Измерить среднее время выполнения функции для заданного аргумента.

    Использует модуль timeit для точного измерения времени выполнения.
    Выполняет number повторений и возвращает среднее время одного вызова.

    Args:
        func (Callable[[int], int]): Измеряемая функция, принимающая int
            и возвращающая int.
        n (int): Аргумент, передаваемый в функцию.
        number (int, optional): Количество повторений для усреднения.
            По умолчанию 10. Чем больше значение, тем точнее результат.

    Returns:
        float: Среднее время одного вызова в секундах.

    Examples:
        >>> t = measure_time(factorial_iterative, 10, number=100)
        >>> isinstance(t, float)
        True
        >>> t > 0
        True
    """
    timer: timeit.Timer = timeit.Timer(lambda: func(n))
    total_time: float = timer.timeit(number=number)
    return total_time / number


def compare_factorials(numbers: List[int]) -> Tuple[List[float], List[float], List[float], List[float]]:
    """Сравнить время выполнения четырёх реализаций факториала.

    Для каждого числа из списка измеряется время работы:
    - math.factorial (эталонная реализация на C)
    - итеративной версии
    - рекурсивной версии
    - мемоизированной версии

    Args:
        numbers (List[int]): Список неотрицательных целых чисел для тестирования.

    Returns:
        Tuple[List[float], List[float], List[float], List[float]]: Кортеж из
        четырёх списков времён (в секундах) для каждой функции в порядке:
        (math.factorial, iterative, recursive, memoized).

    Examples:
        >>> times = compare_factorials([0, 1, 2])
        >>> len(times[0]) == 3
        True
        >>> all(isinstance(t, float) for t in times[0])
        True
    """
    math_times: List[float] = []
    iterative_times: List[float] = []
    recursive_times: List[float] = []
    memoized_times: List[float] = []

    for n in numbers:
        # math.factorial — эталонная реализация на C
        math_times.append(measure_time(math.factorial, n))
        iterative_times.append(measure_time(factorial_iterative, n))
        recursive_times.append(measure_time(factorial_recursive, n))
        memoized_times.append(measure_time(factorial_memoized, n))

    return math_times, iterative_times, recursive_times, memoized_times


def plot_results(numbers: List[int], math_times: List[float], iterative_times: List[float],
                 recursive_times: List[float], memoized_times: List[float]) -> None:
    """Построить график зависимости времени выполнения от входного числа.

    На одном графике отображаются четыре кривые для разных реализаций.
    Используются разные маркеры и цвета для наглядности.

    Args:
        numbers (List[int]): Список входных чисел (ось X).
        math_times (List[float]): Времена для math.factorial.
        iterative_times (List[float]): Времена для итеративной версии.
        recursive_times (List[float]): Времена для рекурсивной версии.
        memoized_times (List[float]): Времена для мемоизированной версии.

    Returns:
        None: Функция ничего не возвращает, только отображает график.

    Examples:
        >>> # Обычно вызывается после compare_factorials
        >>> plot_results([1, 2, 3], [0.001, 0.002, 0.003],
        ...              [0.002, 0.003, 0.004], [0.01, 0.02, 0.03],
        ...              [0.01, 0.02, 0.03])
    """
    plt.figure(figsize=(10, 6))
    plt.plot(numbers, math_times, 'o-', label='math.factorial')
    plt.plot(numbers, iterative_times, 's-', label='Итеративный')
    plt.plot(numbers, recursive_times, '^-', label='Рекурсивный')
    plt.plot(numbers, memoized_times, 'd-', label='Мемоизированный')

    plt.xlabel('Входное число n')
    plt.ylabel('Время выполнения (сек)')
    plt.title('Сравнение времени выполнения реализаций факториала')
    plt.legend()
    plt.grid(True)
    plt.show()


def main() -> None:
    """Основная функция программы.

    Предоставляет пользователю выбор режима работы:
    1 - вычисление для одного числа
    2 - вычисление для нескольких чисел
    3 - использование готового набора чисел (0,2,4,...,28)

    После вычислений отображает результаты и строит график сравнения.

    Returns:
        None
    """
    global _factorial_cache

    print("=" * 50)
    print("СРАВНЕНИЕ РЕАЛИЗАЦИЙ ФАКТОРИАЛА")
    print("=" * 50)
    print("1 - Одно число")
    print("2 - Несколько чисел через пробел")
    print("3 - Готовый набор (0,2,4,...,28)")

    choice: str = input("\nВыберите (1/2/3): ")

    # Режим 1: одно число
    if choice == '1':
        while True:
            try:
                user_input: str = input("Введите число: ")
                if not user_input.lstrip('-').isdigit():
                    print("Ошибка: нужно ввести целое число, а не буквы")
                    continue
                n: int = int(user_input)
                if n < 0:
                    print("Ошибка: число не может быть отрицательным")
                    continue
                break
            except ValueError:
                print("Ошибка: введите целое число")

        # Очищаем кэш
        _factorial_cache = {0: 1, 1: 1}

        # Замеряем время для одного числа
        numbers: List[int] = [n]
        math_times, iter_times, rec_times, mem_times = compare_factorials(numbers)

        # Выводим результат
        print(f"\n{n}! = {math.factorial(n)}")
        print("\nВремя выполнения:")
        print(f"  math.factorial:    {math_times[0]:.8f} сек")
        print(f"  Итеративный:       {iter_times[0]:.8f} сек")
        print(f"  Рекурсивный:       {rec_times[0]:.8f} сек")
        print(f"  Мемоизированный:   {mem_times[0]:.8f} сек")

        # Генерируем числа для графика
        test_numbers: List[int]
        if n <= 20:
            test_numbers = list(range(0, n + 1, max(1, n // 5)))
        else:
            test_numbers = [0, n // 4, n // 2, n]
        test_numbers = sorted(set(test_numbers))

        # Замеряем для графика
        _factorial_cache = {0: 1, 1: 1}
        m_times, i_times, r_times, mem_times = compare_factorials(test_numbers)
        plot_results(test_numbers, m_times, i_times, r_times, mem_times)

    # Режим 2: несколько чисел
    elif choice == '2':
        while True:
            try:
                nums_str: str = input("Введите числа через пробел (например: 5 10 15): ")
                if not nums_str.strip():
                    print("Ошибка: нужно ввести хотя бы одно число")
                    continue

                parts: List[str] = nums_str.strip().split()
                numbers = []
                error: bool = False

                for p in parts:
                    if not p.lstrip('-').isdigit():
                        print(f"Ошибка: '{p}' - это не число, нужно вводить только цифры")
                        error = True
                        break
                    num: int = int(p)
                    if num < 0:
                        print(f"Ошибка: число {num} не может быть отрицательным")
                        error = True
                        break
                    numbers.append(num)

                if error:
                    continue

                unique_numbers: List[int] = sorted(set(numbers))
                if len(unique_numbers) < 2:
                    print("Ошибка: нужно ввести хотя бы 2 разных числа (например: 5 10)")
                    continue

                numbers = unique_numbers
                print(f"Будут проверены числа: {numbers}")
                break

            except Exception:
                print("Ошибка: введите целые числа через пробел")

        # Очищаем кэш
        _factorial_cache = {0: 1, 1: 1}

        # Замеряем время
        math_times, iter_times, rec_times, mem_times = compare_factorials(numbers)

        # Выводим результаты
        print(f"\nРезультаты для чисел {numbers}:")
        print(f"  math.factorial:    среднее = {sum(math_times) / len(math_times):.8f} сек")
        print(f"  Итеративный:       среднее = {sum(iter_times) / len(iter_times):.8f} сек")
        print(f"  Рекурсивный:       среднее = {sum(rec_times) / len(rec_times):.8f} сек")
        print(f"  Мемоизированный:   среднее = {sum(mem_times) / len(mem_times):.8f} сек")

        # Рисуем график
        plot_results(numbers, math_times, iter_times, rec_times, mem_times)

    # Режим 3: готовый набор
    else:
        numbers = list(range(0, 30, 2))
        print(f"\nТестовые числа: {numbers}")

        # Очищаем кэш
        _factorial_cache = {0: 1, 1: 1}

        # Замеряем время
        math_times, iter_times, rec_times, mem_times = compare_factorials(numbers)

        # Выводим результаты
        print("\nСреднее время:")
        print(f"  math.factorial:    {sum(math_times) / len(math_times):.8f} сек")
        print(f"  Итеративный:       {sum(iter_times) / len(iter_times):.8f} сек")
        print(f"  Рекурсивный:       {sum(rec_times) / len(rec_times):.8f} сек")
        print(f"  Мемоизированный:   {sum(mem_times) / len(mem_times):.8f} сек")

        # Рисуем график
        plot_results(numbers, math_times, iter_times, rec_times, mem_times)


if __name__ == "__main__":
    main()