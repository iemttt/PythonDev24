from typing import Tuple, Set, List, Optional, Callable
from random import choice

def bullscows(guess: str, secret: str) -> Tuple[int, int]:
    bulls: int = 0
    cows: int = 0
    checked_chars: Set[str] = set()
    for i, c in enumerate(guess):
        if c == secret[i]:
            bulls += 1
        if c not in checked_chars:
            checked_chars.add(c)
            if c in secret:
                cows += 1
    return bulls, cows

assert(bullscows("ропот", "полип") == (1, 2))


def ask(prompt: str, valid: List[str] = None) -> str:
    guess: Optional[str] = None
    while guess is None or (valid is not None and guess not in valid):
        guess = input(prompt)
    return guess


def inform(format_string: str, bulls: int, cows: int) -> None:
    print(format_string.format(bulls, cows))


def gameplay(ask: Callable, inform: Callable, words: List[str]) -> int:
    # Задумывает случайное слово из списка слов words: list[str]
    secret: str = choice(words)
    guess: Optional[str] = None
    tries: int = 0
    while guess != secret:
        tries += 1
        #Спрашивает у пользователя слово с помощью функции ask("Введите слово: ", words)
        guess: str = ask("Введите слово: ", words)
        #Выводит пользователю результат с помощью функции inform("Быки: {}, Коровы: {}", b, c)
        inform("Быков: {}, Коров: {}", *bullscows(guess, secret))
        #Если слово не отгадано, переходит к п. 1

    #Если слово отгадано, возвращает количество попыток — вызовов ask() 
    print("Количество попыток:", tries)

WORDS: List[str] = list(set((
    "ропот",
    "полип",
    "топор"
)))

gameplay(ask, inform, WORDS)