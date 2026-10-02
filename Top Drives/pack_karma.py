from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal
from itertools import product
import json
from typing import Dict, List


@dataclass(frozen=True)
class Karma:
    S: int = 120
    A: int = 20
    B: int = 4
    C: int = 1
    D: int = 0
    E: int = 0
    F: int = 0


def get_odds(pack_type: str) -> List[Dict[str, Decimal]]:
    with open("pack_odds.json") as f:
        all_odds = json.load(f, parse_float=Decimal)
    if pack_type not in all_odds:
        raise KeyError(f"Pack Type {pack_type} not found.")
    odds = all_odds[pack_type]
    for card in odds:
        if sum(card.values()) != 100:
            raise ValueError("Card odds don't total 100")
        if not all(hasattr(Karma, key) for key in card):
            raise ValueError("Rarity not found!")
    return odds


def calculate_distribution(pack_type: str, karma: Karma = Karma()) -> Dict[int, Decimal]:
    pack_odds = get_odds(pack_type)
    dist = defaultdict(Decimal)
    for combo in product(*[card.items() for card in pack_odds]):
        score, prob = 0, 1
        for rarity, p in combo:
            score += getattr(karma, rarity)
            prob *= p/100  # Probabilities stored as %
        dist[score] += prob
    return dict(dist)


def print_cdf(dist: Dict) -> None:
    d = dict(sorted(dist.items()))
    cur_value = 0
    print("0.00%")
    for key, value in d.items():
        print(f"  Score: {key}")
        cur_value += value * 100
        print(f"{cur_value.normalize():f}%")


def print_pdf(dist: Dict) -> None:
    d = dict(sorted(dist.items()))
    cur_value = 0
    print("0.00%")
    for key, value in d.items():
        print(f"  Score: {key}")
        cur_value += value * 100
        print(f"{cur_value.normalize():f}%")


# print_cdf(calculate_distribution("Ceramic"))
print_cdf(calculate_distribution("Ceramic", Karma(30, 5, 1)))