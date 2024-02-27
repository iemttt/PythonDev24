from typing import Tuple, Set, List, Optional

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