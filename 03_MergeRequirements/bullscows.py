from typing import Tuple, Set


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