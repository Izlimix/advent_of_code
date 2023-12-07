#!/usr/bin/env python3
import re
from collections import Counter

# https://adventofcode.com/2023/day/7


def play_hands(data, jokers):
    pattern = r"(.{5}) (\d+)"
    hands = [Hand(cards, bet, jokers) for (cards, bet) in re.findall(pattern, data)]
    ranked = sorted(hands, key=lambda h: h.get_score())
    
    total_winnings = sum(rank * h.bet for (rank, h) in enumerate(ranked, 1))
    print(f"{total_winnings=}")
    

card_strength = {c: i for (i, c) in enumerate("23456789TJQKA", 2)}
card_strength_jokers = {c: i for (i, c) in enumerate("J23456789TQKA", 1)}

class Hand:
    def __init__(self, cards: str, bet: str, jokers=False) -> None:
        self.cards = cards
        self.bet = int(bet)
        # Hand score = tuple of hand type, then list of card_strengths to be a tiebreaker
        self.score = None
        self.jokers = jokers
        
    def get_score(self) -> tuple:
        if self.score is not None:
            return self.score
        
        # How many cards do we have of each type?
        hand = Counter(self.cards)
        # If we're playing with jokers, set them aside (unless they're the only card we have)
        if self.jokers:
            js = hand["J"]
            if js != 5:
                # Jokers copy our most common card
                hand["J"] = 0
                [(best_card, _)] = hand.most_common(1)
                hand[best_card] += js
        counts = [n for (_, n) in hand.most_common()]

        # Test for each of the 7 hand types
        match counts:
            case 5, *_:
                # 5 of a kind
                s = 7
            case 4, *_:
                # 4 of a kind
                s = 6
            case 3, 2, *_:
                # Full house
                s = 5
            case 3, *_:
                # 3 of a kind
                s = 4
            case 2, 2, *_:
                # Two pair
                s = 3
            case 2, *_:
                # One pair
                s = 2
            case _:
                # High card
                s = 1

        # Use card strengths in order for tiebreaker
        if not self.jokers:
            card_strengths = [card_strength[c] for c in self.cards]
        else:
            card_strengths = [card_strength_jokers[c] for c in self.cards]
        self.score = (s, *card_strengths)

        return self.score


# Command-line execution:
if __name__ == "__main__":
    import sys
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        data = f.read().strip()

    print("Part 1:")
    play_hands(data, jokers=False)
    print("--------")
    print("Part 2:")
    play_hands(data, jokers=True)
    