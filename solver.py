"""solver.py

Solve the Einstein puzzle using Raymond Hettinger's approach.
"""

from __future__ import annotations

from enum import Enum, auto
from itertools import product
from typing import Iterator, List, Tuple, Type, Union, Literal
from collections.abc import MutableSequence

import sat_utils
from sat_utils import CNF, Element

Element = str
from abc import ABC, abstractmethod
from typing import Iterable


from dataclasses import dataclass, field


class Literal(Enum):
    """Enum subclass to have the member's value be equal to its name."""

    @staticmethod
    def _generate_next_value_(name, start, count, last_values) -> Element:
        return name


def comb(value: Literal, house: int) -> str:
    """Format how a value is shown at a given house"""

    return f"{value} {house}"


@dataclass
class Puzzle:
    """Collection of clues for the zebra puzzle"""

    clues: List[Clue] = field(default_factory=list)
    constraints: List[Tuple[str]] = field(default_factory=list)

    def add_clue(self, clue: Clue) -> Puzzle:
        self.clues.append(clue)
        return self

    def add_constraint(self, constraints: List[Tuple[str]]) -> Puzzle:
        self.constraints.extend(constraints)
        return self

    def as_cnf(self) -> List[Tuple[str]]:
        """Express puzzle as solvable CNF"""

        # this would be a comprehension if we could use iterable unpacking
        cnf = []
        for clue in self.clues:
            cnf.extend(clue.as_cnf())

        cnf.extend(self.constraints)
        return cnf


class Clue(ABC):
    """Base class for the types of clues that we allow."""

    @abstractmethod
    def as_cnf(self) -> Iterable[Tuple[str]]:
        """Express clue as a CNF (and-of-ors)."""

        ...


@dataclass
class found_at(Clue):
    """Value known to be at a specific house"""

    value: Literal
    house: int

    def as_cnf(self) -> List[Tuple[str]]:
        return [(comb(self.value, self.house),)]


@dataclass
class same_house(Clue):
    """Value known to be at a specific house"""

    value1: Literal
    value2: Literal

    def as_cnf(self) -> List[Tuple[str]]:
        return sat_utils.from_dnf((comb(self.value1, i), comb(self.value2, i)) for i in houses)


@dataclass
class consecutive(Clue):
    """The values are in consecutive houses: green1 & white2 | green2 & white3 ..."""

    value1: Literal
    value2: Literal

    def as_cnf(self) -> List[Tuple[str]]:
        return sat_utils.from_dnf(
            (comb(self.value1, i), comb(self.value2, j)) for i, j in zip(houses, houses[1:])
        )


@dataclass
class beside(Clue):
    """The values occur side-by-side: blends1 & cat2 | blends2 & cat1 ..."""

    value1: Literal
    value2: Literal

    def as_cnf(self) -> List[Tuple[str]]:
        return sat_utils.from_dnf(
            [(comb(self.value1, i), comb(self.value2, j)) for i, j in zip(houses, houses[1:])]
            + [(comb(self.value2, i), comb(self.value1, j)) for i, j in zip(houses, houses[1:])]
        )


@dataclass
class left_of(Clue):
    """The first value is somewhere to the left of the second value."""

    value1: Literal
    value2: Literal

    def as_cnf(self) -> List[Tuple[str]]:
        return sat_utils.from_dnf(
            (comb(self.value1, i), comb(self.value2, j))
            for i, j in product(houses, houses)
            if i < j
        )


@dataclass
class right_of(Clue):
    """The first value is somewhere to the right of the second value."""

    value1: Literal
    value2: Literal

    def as_cnf(self) -> List[Tuple[str]]:
        return sat_utils.from_dnf(
            (comb(self.value1, i), comb(self.value2, j))
            for i, j in product(houses, houses)
            if i > j
        )


@dataclass
class one_between(Clue):
    """The values have one other value in between: cat1 & x2 & dog3 | dog2 & x3 & cat1 ..."""

    value1: Literal
    value2: Literal

    def as_cnf(self) -> List[Tuple[str]]:
        return sat_utils.from_dnf(
            [(comb(self.value1, i), comb(self.value2, j)) for i, j in zip(houses, houses[2:])]
            + [(comb(self.value2, i), comb(self.value1, j)) for i, j in zip(houses, houses[2:])]
        )


@dataclass
class two_between(Clue):
    """The values have two other values in between: cat1 & x2 & y3 & dog4 | ..."""

    value1: Literal
    value2: Literal

    def as_cnf(self) -> List[Tuple[str]]:
        return sat_utils.from_dnf(
            [(comb(self.value1, i), comb(self.value2, j)) for i, j in zip(houses, houses[3:])]
            + [(comb(self.value2, i), comb(self.value1, j)) for i, j in zip(houses, houses[3:])]
        )


"""
Original version

Taken straight from rhettinger.github.io and the associated talk.

Entities:
 * There are five houses in unique colors: Blue, green, red, white and yellow.
 * In each house lives a person of unique nationality: British, Danish, German, Norwegian and Swedish.
 * Each person drinks a unique beverage: Beer, coffee, milk, tea and water.
 * Each person smokes a unique cigar brand: Blue Master, Dunhill, Pall Mall, Prince and blend.
 * Each person keeps a unique pet: Cats, birds, dogs, fish and horses.

Constraints:
 * The Brit lives in a red house.
 * The Swede keeps dogs as pets.
 * The Dane drinks tea.
 * The green house is on the left of the white, next to it.
 * The green house owner drinks coffee.
 * The person who smokes Pall Mall rears birds.
 * The owner of the yellow house smokes Dunhill.
 * The man living in the house right in the center drinks milk.
 * The Norwegian lives in the first house.
 * The man who smokes blend lives next to the one who keeps cats.
 * The man who keeps horses lives next to the man who smokes Dunhill.
 * The owner who smokes Blue Master drinks beer.
 * The German smokes Prince.
 * The Norwegian lives next to the blue house.
 * The man who smokes blend has a neighbor who drinks water.

For each house, find out what color it is, who lives there, what they drinkk, what
they smoke, and what pet they own.
"""

houses = [1, 2, 3, 4, 5]


class Color(Literal):
    yellow = auto()
    red = auto()
    white = auto()
    green = auto()
    blue = auto()


class Nationality(Literal):
    dane = auto()
    brit = auto()
    swede = auto()
    norwegian = auto()
    german = auto()


class Animal(Literal):
    horse = auto()
    cat = auto()
    bird = auto()
    fish = auto()
    dog = auto()


class Drink(Literal):
    water = auto()
    tea = auto()
    milk = auto()
    coffee = auto()
    root_beer = auto()


class Cigar(Literal):
    pall_mall = auto()
    prince = auto()
    blue_master = auto()
    dunhill = auto()
    blends = auto()


enum_classes: List[Type[Literal]] = [Color, Nationality, Animal, Drink, Cigar]
literals: List[Literal] = [el for group in enum_classes for el in group]

# set up the puzzle with constraints and clues
puzzle = Puzzle()

# # each house gets exactly one value from each attribute group
for house in houses:
    for enum_type in enum_classes:
        puzzle.add_constraint(sat_utils.one_of(comb(value, house) for value in enum_type))

# each value gets assigned to exactly one house
for literal in literals:
    puzzle.add_constraint(sat_utils.one_of(comb(literal, house) for house in houses))

puzzle = (
    puzzle.add_clue(same_house(Nationality.brit, Color.red))
    .add_clue(same_house(Nationality.swede, Animal.dog))
    .add_clue(same_house(Nationality.dane, Drink.tea))
    .add_clue(consecutive(Color.green, Color.white))
    .add_clue(same_house(Color.green, Drink.coffee))
    .add_clue(same_house(Cigar.pall_mall, Animal.bird))
    .add_clue(same_house(Color.yellow, Cigar.dunhill))
    .add_clue(found_at(Drink.milk, 3))
    .add_clue(found_at(Nationality.norwegian, 1))
    .add_clue(beside(Cigar.blends, Animal.cat))
    .add_clue(beside(Animal.horse, Cigar.dunhill))
    .add_clue(same_house(Cigar.blue_master, Drink.root_beer))
    .add_clue(same_house(Nationality.german, Cigar.prince))
    .add_clue(beside(Nationality.norwegian, Color.blue))
    .add_clue(beside(Cigar.blends, Drink.water))
)

sols = sat_utils.solve_all(puzzle.as_cnf())
print(f"{len(sols)} solutions found")
for sol in sols:
    print(sol)

"""
Quag's version

In honor of Mother's Day, a feast is being held to celebrate five Moms: Aniya, Holly,
Janelle, Kailyn, and Penny. Each Mom will be served by their son or daughter (Bella,
Fred, Meredith, Samantha, and Timothy), who will also place a bouquet of flowers
(Carnations, Daffodils, Lilies, Roses, or Tulips) at their Mom's place setting and
prepare a meal for them (Grilled Cheese, Pizza, Spaghetti, Stew, or Stir Fry).

The seats are arranged in a straight line at the head table, with the first being
the furthest to the left (from our perspective, not the Mom's perspectives).

Also, when it says there is "one chair" between two people, it means one person might
be in the second chair while the other person is in the fourth (i.e. there is one chair
in between them that neither is sitting in).
"""

houses = [1, 2, 3, 4, 5]


class Mothers(Literal):
    aniya = auto()
    holly = auto()
    janelle = auto()
    kailyn = auto()
    penny = auto()


class Children(Literal):
    bella = auto()
    fred = auto()
    meredith = auto()
    samantha = auto()
    timothy = auto()


class Flowers(Literal):
    carnations = auto()
    daffodils = auto()
    lilies = auto()
    roses = auto()
    tulips = auto()


class Foods(Literal):
    grilled_cheese = auto()
    pizza = auto()
    spaghetti = auto()
    stew = auto()
    stir_fry = auto()


enum_classes: List[Type[Literal]] = [Mothers, Children, Flowers, Foods]
literals = [el for group in enum_classes for el in group]

# set up the puzzle with constraints and clues
puzzle = Puzzle()

# each house gets exactly one value from each attribute group
for house in houses:
    for group in enum_classes:
        puzzle.add_constraint(sat_utils.one_of(comb(value, house) for value in group))

# each value gets assigned to exactly one house
for value in literals:
    puzzle.add_constraint(sat_utils.one_of(comb(value, house) for house in houses))


# 1. There is one chair between the place setting with Lilies and the one eating Grilled Cheese.
puzzle = puzzle.add_clue(one_between(Flowers.lilies, Foods.grilled_cheese))

# 2. There is one chair between Timothy's Mom and the one eating Stew.
puzzle = puzzle.add_clue(one_between(Children.timothy, Foods.stew))

# 3. There are two chairs between the Bella's Mom and Penny's seat on the right.
puzzle = puzzle.add_clue(two_between(Children.bella, Mothers.penny))
puzzle = puzzle.add_clue(right_of(Mothers.penny, Children.bella))

# 4. There is one chair between the place setting with Roses and the one eating Spaghetti on the left.
puzzle = puzzle.add_clue(one_between(Flowers.roses, Foods.spaghetti))
puzzle = puzzle.add_clue(left_of(Foods.spaghetti, Flowers.roses))

# 5. There are two chairs between the place setting with Carnations and Samantha's Mom.
puzzle = puzzle.add_clue(two_between(Flowers.carnations, Children.samantha))

# 6. There is one chair between Meredith's Mom and Timothy's Mom on the left.
puzzle = puzzle.add_clue(one_between(Children.meredith, Children.timothy))
puzzle = puzzle.add_clue(left_of(Children.timothy, Children.meredith))

# 7. Aniya's place setting has a lovely Carnation bouquet.
puzzle = puzzle.add_clue(same_house(Mothers.aniya, Flowers.carnations))

# 8. There are two chairs between the one eating Grilled Cheese and the one eating Spaghetti.
puzzle = puzzle.add_clue(two_between(Foods.grilled_cheese, Foods.spaghetti))

# 9. The person in the first chair (left-most) is eating Pizza.
puzzle = puzzle.add_clue(found_at(Foods.pizza, 1))

# 10. The Tulips were placed at one of the place settings somewhere to the left of Penny's chair.
puzzle = puzzle.add_clue(left_of(Flowers.tulips, Mothers.penny))

# 11. There are two chairs between the one eating Spaghetti and Kailyn's seat.
puzzle = puzzle.add_clue(two_between(Foods.spaghetti, Mothers.kailyn))

# 12. There is one chair between the one eating Pizza and Holly's chair on the right.
puzzle = puzzle.add_clue(one_between(Foods.pizza, Mothers.holly))
puzzle = puzzle.add_clue(right_of(Mothers.holly, Foods.pizza))

all_solutions = sat_utils.solve_all(puzzle.as_cnf())
print(f"{len(all_solutions)} solutions found")
print(all_solutions)
