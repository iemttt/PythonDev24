from typing import Tuple, Set, List, Optional, Callable
from random import choice
import argparse
from urllib.parse import urlparse
from urllib.request import urlretrieve

from cowsay import cowsay, get_random_cow, read_dot_cow


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


def random_cow_say(message: str) -> str:
    return cowsay(message, cow=get_random_cow()) + '\n'

def thing_say(message: str) -> str:
    cowfile: str = ""
    with open("thing.cow") as f:
        cowfile = read_dot_cow(f)
    return cowsay(message, cowfile=cowfile) + '\n'

def ask(prompt: str, valid: List[str] = None) -> str:
    guess: Optional[str] = None
    while guess is None or (valid is not None and guess not in valid):
        guess = input(thing_say(prompt))
    return guess


def inform(format_string: str, bulls: int, cows: int) -> None:
    print(random_cow_say(format_string.format(bulls, cows)))


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
    return tries


def get_words(url: str, length: int) -> List[str]:
    o = urlparse(url)
    words: List[str] = []
    words_file = None
    if o.scheme == "":
        words_file = url
    else:
        words_file, _ = urlretrieve(url)

    with open(words_file) as f:
        for l in f.readlines():
            w = l.strip()
            if len(w) == length:
                words.append(w)
    return words


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("dictionary", type=str)
    parser.add_argument("length", type=int, nargs="?", default=5)
    args = parser.parse_args()
    words: List[str] = get_words(args.dictionary, args.length)
    tries: int = gameplay(ask, inform, words)
    print("Количество попыток:", tries)
