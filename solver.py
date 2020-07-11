"""solver.py

Solve the Einstein puzzle using Raymond Hettinger's approach.
"""

from __future__ import annotations

from enum import Enum, auto
import functools
from itertools import product
from typing import Iterator, List, Tuple, Type, Union, Literal
from collections.abc import MutableSequence

import sat_utils
from sat_utils import CNF, Element

Element = str
from abc import ABC, abstractmethod
from typing import Iterable
import random


from dataclasses import dataclass, field


class Literal(Enum):
    """Enum subclass to have the member's value be equal to its name."""

    @staticmethod
    def _generate_next_value_(name, start, count, last_values) -> Element:
        return name


def comb(value: Literal, house: int) -> str:
    """Format how a value is shown at a given house"""

    return f"{value} {house}"


from functools import wraps


def capitalize_first(repr_func):
    """
    Decorator for a __repr__ function that capitalizes the first letter without chagning the rest

    (in contrast to str.capitalize(), which capitalizes the first letter and makes the rest lower)
    """

    @wraps(repr_func)
    def wrapper(*args, **kwargs):
        output = repr_func(*args, **kwargs)
        return output[0].upper() + output[1:]

    return wrapper


class Puzzle:
    """
    A Puzzle is defined as a collection of constraints and clues.

    Clues are subclassess of Clue. They represent information about the puzzle that can be used by
    a human to solve it, like "the man who drinks tea owns a cat." Clues aren't converted to CNF
    until the `as_cnf` method is called.

    Constraints are structural properties of the puzzle, given to us in CNF to start. They're
    things like "each house gets exactly one type of flower" and "each flower must be assigned
    to one house."

    We can add constraints and clues with `add_constraint` and `add_clue`. Both of these return
    the instance, so they can be chained together for readability.

    Since in constraint satisfaction land, clues and constraints are the same thing (they're just
    logical clauses), we lump them all together at solve time.
    """

    def __init__(self, n_houses: int = 5) -> None:
        self.houses = range(1, n_houses + 1)
        self.clues: List[Clue] = []
        self.constraints: List[Tuple[str]] = []

    def add_constraint(self, constraints: List[Tuple[str]]) -> Puzzle:
        self.constraints.extend(constraints)
        return self

    def add_clue(self, clue: Clue) -> Puzzle:
        self.clues.append(clue)
        return self

    def as_cnf(self) -> List[Tuple[str]]:
        """Express puzzle as solvable CNF"""

        # this would be a comprehension if we could use iterable unpacking
        cnf = []
        for clue in self.clues:
            cnf.extend(clue.as_cnf())

        cnf.extend(self.constraints)
        return cnf

    def __repr__(self) -> str:

        s = f"This puzzle has {len(self.houses)} houses:\n"
        for i, clue in enumerate(self.clues):
            s += f"{i + 1}. {clue}\n"

        return s


class Clue(ABC):
    """Base class for the types of clues that we allow."""

    @abstractmethod
    def as_cnf(self) -> Iterable[Tuple[str]]:
        ...

    @abstractmethod
    def __repr__(self) -> str:
        ...


@dataclass
class found_at(Clue):
    """
    A literal is known to be at a specific house
    
    Examples:
     - the tea drinker lives in the middle house
     - the fourth house is red
    """

    value: Literal
    house: int

    def as_cnf(self) -> List[Tuple[str]]:
        return [(comb(self.value, self.house),)]

    @capitalize_first
    def __repr__(self) -> str:
        houses = [None, "first", "second", "third", "fourth", "fifth", "sixth"]
        return f"{self.value.value} is in the {houses[self.house]} house."


@dataclass
class same_house(Clue):
    """
    Two values are known to be at the same house
    
    Examples:
     - the musician drinks tea
     - the red house contains a cat
    """

    value1: Literal
    value2: Literal
    houses: List[int] = field(default_factory=lambda: [1, 2, 3, 4, 5])

    def as_cnf(self) -> List[Tuple[str]]:
        return sat_utils.from_dnf((comb(self.value1, i), comb(self.value2, i)) for i in self.houses)

    def __repr__(self) -> str:
        index = random.randint(0, 2)
        return [
            f"The same house has {self.value1.value} and {self.value2.value}.",
            f"The {self.value1.value} and {self.value2.value} are in the same house.",
            f"A single house contains both {self.value1.value} and {self.value2.value}.",
        ][index]


@dataclass
class consecutive(Clue):
    """
    The first value is directly to the left of the second value
    
    Examples:
     - the green house is directly to the left of the white house
       (green in 1, white in 2 OR green in 2, white in 3 OR etc.)
     - the house with the kittens is directly to the right of the tea drinker's home
       (kittens in 2, tea in 1 OR kittens in 3, tea in 2 OR etc.)
    """

    value1: Literal
    value2: Literal
    houses: List[int] = field(default_factory=lambda: [1, 2, 3, 4, 5])

    def as_cnf(self) -> List[Tuple[str]]:
        return sat_utils.from_dnf(
            (comb(self.value1, i), comb(self.value2, j))
            for i, j in zip(self.houses, self.houses[1:])
        )

    @capitalize_first
    def __repr__(self) -> str:
        return f"{self.value1.value} is directly left of {self.value2.value}."


@dataclass
class beside(Clue):
    """
    The two values occur side-by-side (either left or right)
    
    Examples:
     - the coffee drinker is (left or right) of the tea drinker
     - the cat owner is (left or right) of the green house
    """

    value1: Literal
    value2: Literal
    houses: List[int] = field(default_factory=lambda: [1, 2, 3, 4, 5])

    def as_cnf(self) -> List[Tuple[str]]:
        return sat_utils.from_dnf(
            [
                (comb(self.value1, i), comb(self.value2, j))
                for i, j in zip(self.houses, self.houses[1:])
            ]
            + [
                (comb(self.value2, i), comb(self.value1, j))
                for i, j in zip(self.houses, self.houses[1:])
            ]
        )

    @capitalize_first
    def __repr__(self) -> str:
        return f"{self.value1.value} and {self.value2.value} are next to each other."


@dataclass
class left_of(Clue):
    """
    The first value is somewhere to the left of the second value
    
    Examples:
     - the tea drinker is in house 1 and the musician in 2, 3, 4, or 5;
       OR the tea drinker in 2, and musician in 3, 4, or 5;
       OR the tea drinker in 3, musician in 4, 5; OR tea 4, musician 5.
    """

    value1: Literal
    value2: Literal
    houses: List[int] = field(default_factory=lambda: [1, 2, 3, 4, 5])

    def as_cnf(self) -> List[Tuple[str]]:
        return sat_utils.from_dnf(
            (comb(self.value1, i), comb(self.value2, j))
            for i, j in product(self.houses, self.houses)
            if i < j
        )

    @capitalize_first
    def __repr__(self) -> str:
        return f"{self.value1.value} is somewhere to the left of {self.value2.value}."


@dataclass
class right_of(Clue):
    """
    The first value is somewhere to the right of the second value.
    
    Examples:
     - the coffee drinker is in house 5 and the artist in 1, 2, 3, 4;
       OR the coffee drinker in 4, and artist in 1, 2, or 3;
       OR the coffee drinker in 3, artist in 1, 2; OR coffee 2, artist 1.
    """

    value1: Literal
    value2: Literal
    houses: List[int] = field(default_factory=lambda: [1, 2, 3, 4, 5])

    def as_cnf(self) -> List[Tuple[str]]:
        return sat_utils.from_dnf(
            (comb(self.value1, i), comb(self.value2, j))
            for i, j in product(self.houses, self.houses)
            if i > j
        )

    @capitalize_first
    def __repr__(self) -> str:
        return f"{self.value1.value} is somewhere to the right of {self.value2.value}."


@dataclass
class one_between(Clue):
    """
    The values are separated by one house
    
    Examples (if 5 houses):
     - the cat is in house 1 and tea drinker in house 3; OR cat 2, tea 4;
       OR cat 4 house 5
     - the green house is #1 and the musician in house 3; or green house 2, musician 4;
       OR green house 3, musician 5.
    """

    value1: Literal
    value2: Literal
    houses: List[int] = field(default_factory=lambda: [1, 2, 3, 4, 5])

    def as_cnf(self) -> List[Tuple[str]]:
        return sat_utils.from_dnf(
            [
                (comb(self.value1, i), comb(self.value2, j))
                for i, j in zip(self.houses, self.houses[2:])
            ]
            + [
                (comb(self.value2, i), comb(self.value1, j))
                for i, j in zip(self.houses, self.houses[2:])
            ]
        )

    def __repr__(self) -> str:
        return f"There is one house between the {self.value1.value} and the {self.value2.value}."


@dataclass
class two_between(Clue):
    """
    The values are separated by two houses

    Examples (if 5 houses):
     - the cat is in house 1 and artist in house 4; or cat 2, artist 5
     - the dog is in house 1 and red house is #4; or dog 2, red house 5
    """

    value1: Literal
    value2: Literal
    houses: List[int] = field(default_factory=lambda: [1, 2, 3, 4, 5])

    def as_cnf(self) -> List[Tuple[str]]:
        return sat_utils.from_dnf(
            [
                (comb(self.value1, i), comb(self.value2, j))
                for i, j in zip(self.houses, self.houses[3:])
            ]
            + [
                (comb(self.value2, i), comb(self.value1, j))
                for i, j in zip(self.houses, self.houses[3:])
            ]
        )

    def __repr__(self) -> str:
        return f"There are two houses between the {self.value1.value} and the {self.value2.value}."


"""
Original version

Taken straight from rhettinger.github.io and the associated talk.

Entities:
 * There are five houses in unique colors: Blue, green, red, white and yellow.
 * In each house lives a person of unique nationality: British, Danish, German, Norwegian and Swedish.
 * Each person drinks a unique beverage: Beer, coffee, milk, tea and water.
 * Each person smokes a unique cigar brand: Blue Master, Dunhill, Pall Mall, Prince and blend.
 * Each person keeps a unique pet: Cats
 , birds, dogs, fish and horses.

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


class Color(Literal):
    yellow = "the person who loves yellow"
    red = "the person whose favorite color is red"
    white = "the person who loves white"
    green = "the person whose favorite color is green"
    blue = "the person who loves blue"


class Nationality(Literal):
    dane = "the Dane"
    brit = "the British person"
    swede = "the Swedish person"
    norwegian = "the Norwegian"
    german = "the German"


class Animal(Literal):
    horse = "the person who keeps horses"
    cat = "the cat lover"
    bird = "the bird keeper"
    fish = "the fish enthusiast"
    dog = "the dog owner"


class Drink(Literal):
    water = "the one who only drinks water"
    tea = "the tea drinker"
    milk = "the person who likes milk"
    coffee = "the coffee drinker"
    root_beer = "the root beer lover"


class Cigar(Literal):
    pall_mall = "the person partial to Pall Mall"
    prince = "the Prince smoker"
    blue_master = "the person who smokes Blue Master"
    dunhill = "the Dunhill smoker"
    blends = "the person who smokes many different blends"


enum_classes: List[Type[Literal]] = [Color, Nationality, Animal, Drink, Cigar]
literals: List[Literal] = [el for group in enum_classes for el in group]

# set up the puzzle with constraints and clues
puzzle = Puzzle()

# # each house gets exactly one value from each attribute group
for house in puzzle.houses:
    for enum_type in enum_classes:
        puzzle.add_constraint(sat_utils.one_of(comb(value, house) for value in enum_type))

# each value gets assigned to exactly one house
for literal in literals:
    puzzle.add_constraint(sat_utils.one_of(comb(literal, house) for house in puzzle.houses))

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

print(puzzle)

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


class Mothers(Literal):
    aniya = "Aniya"
    holly = "Holly"
    janelle = "Janelle"
    kailyn = "Kailyn"
    penny = "Penny"


class Children(Literal):
    bella = "Bella's mother"
    fred = "the mother Fred"
    meredith = "Meredith's mom"
    samantha = "Samantha's mom"
    timothy = "the mother of Timothy"


class Flowers(Literal):
    carnations = "the carnations"
    daffodils = "a bouquet of daffodils"
    lilies = "some lilies"
    roses = "the rose bouquet"
    tulips = "the tulips"


class Foods(Literal):
    grilled_cheese = "the person eating grilled cheese"
    pizza = "the pizza lover"
    spaghetti = "the spaghetti eater"
    stew = "the one having stew"
    stir_fry = "the person with stir fry"


enum_classes: List[Type[Literal]] = [Mothers, Children, Flowers, Foods]
literals = [el for group in enum_classes for el in group]

# set up the puzzle with constraints and clues
puzzle = Puzzle()

# each house gets exactly one value from each attribute group
for house in puzzle.houses:
    for group in enum_classes:
        puzzle.add_constraint(sat_utils.one_of(comb(value, house) for value in group))

# each value gets assigned to exactly one house
for literal in literals:
    puzzle.add_constraint(sat_utils.one_of(comb(literal, house) for house in puzzle.houses))


puzzle = (
    # 1. There is one chair between the place setting with Lilies and the one eating Grilled Cheese.
    puzzle.add_clue(one_between(Flowers.lilies, Foods.grilled_cheese))
    # 2. There is one chair between Timothy's Mom and the one eating Stew.
    .add_clue(one_between(Children.timothy, Foods.stew))
    # 3. There are two chairs between the Bella's Mom and Penny's seat on the right.
    .add_clue(two_between(Children.bella, Mothers.penny))
    .add_clue(right_of(Mothers.penny, Children.bella))
    # 4. There is one chair between the place setting with Roses and the one eating Spaghetti on the left.
    .add_clue(one_between(Flowers.roses, Foods.spaghetti))
    .add_clue(left_of(Foods.spaghetti, Flowers.roses))
    # 5. There are two chairs between the place setting with Carnations and Samantha's Mom.
    .add_clue(two_between(Flowers.carnations, Children.samantha))
    # 6. There is one chair between Meredith's Mom and Timothy's Mom on the left.
    .add_clue(one_between(Children.meredith, Children.timothy))
    .add_clue(left_of(Children.timothy, Children.meredith))
    # 7. Aniya's place setting has a lovely Carnation bouquet.
    .add_clue(same_house(Mothers.aniya, Flowers.carnations))
    # 8. There are two chairs between the one eating Grilled Cheese and the one eating Spaghetti.
    .add_clue(two_between(Foods.grilled_cheese, Foods.spaghetti))
    # 9. The person in the first chair (left-most) is eating Pizza.
    .add_clue(found_at(Foods.pizza, 1))
    # 10. The Tulips were placed at one of the place settings somewhere to the left of Penny's chair.
    .add_clue(left_of(Flowers.tulips, Mothers.penny))
    # 11. There are two chairs between the one eating Spaghetti and Kailyn's seat.
    .add_clue(two_between(Foods.spaghetti, Mothers.kailyn))
    # 12. There is one chair between the one eating Pizza and Holly's chair on the right.
    .add_clue(one_between(Foods.pizza, Mothers.holly))
    .add_clue(right_of(Mothers.holly, Foods.pizza))
)

print(puzzle)
all_solutions = sat_utils.solve_all(puzzle.as_cnf())
print(f"{len(all_solutions)} solutions found")
print(all_solutions)
