"""
Простые тесты для проверки реализаций факториала.
"""

import pytest
import sys
import os

# Добавляем путь к основному файлу
sys.path.insert(0, os.path.dirname(__file__))

# Импортируем функции из основного файла
from factorial_compare import (
    factorial_recursive,
    factorial_iterative,
    factorial_memoized
)


def test_recursive():
    """Тест рекурсивной реализации."""
    assert factorial_recursive(0) == 1
    assert factorial_recursive(1) == 1
    assert factorial_recursive(5) == 120
    assert factorial_recursive(7) == 5040


def test_iterative():
    """Тест итеративной реализации."""
    assert factorial_iterative(0) == 1
    assert factorial_iterative(1) == 1
    assert factorial_iterative(5) == 120
    assert factorial_iterative(7) == 5040


def test_memoized():
    """Тест мемоизированной реализации."""
    assert factorial_memoized(0) == 1
    assert factorial_memoized(1) == 1
    assert factorial_memoized(5) == 120
    assert factorial_memoized(7) == 5040


def test_all_same():
    """Проверка, что все реализации дают одинаковый результат."""
    for n in range(10):
        assert factorial_recursive(n) == factorial_iterative(n) == factorial_memoized(n)


def test_negative():
    """Проверка, что отрицательные числа вызывают ошибку."""
    with pytest.raises(ValueError):
        factorial_recursive(-1)

    with pytest.raises(ValueError):
        factorial_iterative(-5)

    with pytest.raises(ValueError):
        factorial_memoized(-10)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])