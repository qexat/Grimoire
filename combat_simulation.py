"""
A fun little combat simulator between pre-defined warriors.

The backstory of this idea came from me thinking aloud about how to explain
classes and their purpose to someone who has done little to no programming.
"""

import abc
import argparse
import math
import os
import random
import sys
import time
import typing


only_essential: bool = False  # only show essential information
action_length: float = 1.0


class Soldier(abc.ABC):
    name: str
    color: int
    hp: int
    DAMAGE: typing.ClassVar[int]

    def __repr__(self) -> str:
        if self.is_dead():
            return f"{self.pretty_name} (dead)"

        return f"{self.pretty_name} \x1b[2m({self.hp} PV)\x1b[22m"

    @property
    def pretty_name(self) -> str:
        return f"\x1b[3{self.color}m[{self.__class__.__name__}] \x1b[1m{self.name}\x1b[22;39m"

    def attack_when_dead(self) -> None:
        self.do("is dead and cannot attack.")

    def attack(self) -> int:
        self.tell("Take this!")

        return self.DAMAGE

    def suffer(self, damage: int) -> None:
        if not self.is_dead():
            if damage:
                self.tell("Aouch!")
                self.do(f"lost {damage} health points.")

            self.hp -= damage

        if self.is_dead():
            self.do("perished as a result of this blow")

    def tell(self, parole: str, *, important: bool = False) -> None:
        if important or not only_essential:
            print(f"{self!r}: {parole}")

    def do(self, action: str) -> None:
        print(f"{self.pretty_name} \x1b[3{self.color};3m{action}\x1b[23;39m")

    def is_dead(self) -> bool:
        return self.hp <= 0

    def claim_victory(self) -> None:
        self.tell("I won!", important=True)


class Knight(Soldier):
    DAMAGE = 10

    def __init__(self, name: str, color: int) -> None:
        self.name = name
        self.color = color
        self.hp = 50

    def attack(self) -> int:
        if self.is_dead():
            self.attack_when_dead()

            return 0

        return super().attack()


class Archer(Soldier):
    DAMAGE = 10

    def __init__(self, name: str, color: int, arrows: int = 12) -> None:
        self.name = name
        self.color = color
        self.hp = 100
        self.arrows = arrows

    def attack(self) -> int:
        if self.is_dead():
            self.attack_when_dead()

            return 0

        if self.arrows <= 0:
            self.tell("Crap, I'm out of arrows !")
            return 0

        if random.randint(0, 5) >= 3:
            self.arrows -= 1

            return super().attack()
        else:
            self.tell("Missed, what a waste!")

            return 0


class Mage(Soldier):
    DAMAGE = 20

    def __init__(self, name: str, color: int, spells: int = 6) -> None:
        self.name = name
        self.color = color
        self.hp = 40
        self.spells = spells

    def attack(self) -> int:
        if self.is_dead():
            self.attack_when_dead()

            return 0

        if self.spells <= 0:
            self.tell("Crap, I'm out of spells!")
            return 0

        if random.randint(False, True):
            self.spells -= 1

            return super().attack()
        else:
            self.tell("Missed, what a waste!")

            return 0


def strike(attacker: Soldier, defender: Soldier, fastforward: bool) -> bool:
    damage = attacker.attack()
    fastforward = pause(fastforward)
    defender.suffer(damage)

    return pause(fastforward)


def pause(fastforward: bool) -> bool:
    if not fastforward:
        try:
            time.sleep(action_length)
        except KeyboardInterrupt:
            print("\nFast-forwarding...")
            return True
        else:
            return False

    return fastforward


# deadass <insert skull emoji>
COMBAT_SYNOPSIS = "\x1b[1;3;4;53m\x1b[38;5;118mC\x1b[38;5;119mO\x1b[38;5;120mM\x1b[38;5;121mB\x1b[38;5;122mA\x1b[38;5;123mT\x1b[22;23;39;24;55m"


def get_winner(s1: Soldier, s2: Soldier) -> Soldier:
    fastforward = False

    print(COMBAT_SYNOPSIS, s1, "vs", s2)
    print("—" * 64)

    soldiers = [s1, s2]
    random.shuffle(soldiers)

    s1, s2 = soldiers

    s1.do("was faster ! They will strike the first blow.")
    fastforward = pause(fastforward)

    turn = 1

    while not (s1.is_dead() or s2.is_dead()):
        print(f"[Turn {turn}]")

        fastforward = strike(s1, s2, fastforward)
        fastforward = strike(s2, s1, fastforward)

        print("End of turn.")
        print(s1, "|", s2, "\n")

        turn += 1

    return s2 if s1.is_dead() else s1


def _positive_float(raw: str) -> float:
    value = float(raw)

    if value in {float("inf"), float("-inf")}:
        raise ValueError("cannot be infinity")

    if math.isnan(value):
        raise ValueError("cannot be NaN")

    if value < 0.0:
        raise ValueError("must be non-negative")

    return value


SoldierName: typing.TypeAlias = typing.Literal[
    "Matthew",
    "Belle",
    "Richard",
    "Daisy",
    "Kyo",
    "Zaire",
    "Hoanh",
    "Noellia",
]

SOLDIERS: dict[SoldierName, Soldier] = {
    "Matthew": Knight("Matthew", 4),
    "Belle": Mage("Belle", 1),
    "Richard": Mage("Richard", 2),
    "Daisy": Archer("Daisy", 3),
    "Kyo": Knight("Kyo", 0),
    "Zaire": Archer("Zaire", 5),
    "Hoanh": Mage("Hoanh", 6),
    "Noellia": Knight("Noellia", 7),
}


class CombatNamespace(typing.Protocol):
    player1: SoldierName
    player2: SoldierName

    only_essential: bool
    action_length: float


def parse_args() -> CombatNamespace:
    parser = argparse.ArgumentParser()

    parser.add_argument("player1", choices=SOLDIERS.keys())
    parser.add_argument("player2", choices=SOLDIERS.keys())
    parser.add_argument("--only-essential", "-s", action="store_true")
    parser.add_argument("--action-length", "-al", type=_positive_float, default=1.0)

    return typing.cast(CombatNamespace, parser.parse_args())


def main() -> int:
    namespace = parse_args()

    if namespace.player1 == namespace.player2:
        print(f"{namespace.player1} cannot fight themselves!", file=sys.stderr)

        return os.EX_DATAERR

    global only_essential, action_length

    only_essential = namespace.only_essential
    action_length = namespace.action_length

    s1 = SOLDIERS[namespace.player1]
    s2 = SOLDIERS[namespace.player2]

    get_winner(s1, s2).claim_victory()

    return os.EX_OK


if __name__ == "__main__":
    raise SystemExit(main())
