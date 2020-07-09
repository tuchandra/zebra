"""solver.py

Solve the Einstein puzzle using Raymond Hettinger's approach.
"""


from enum import Enum, auto
from itertools import product
from typing import List, Tuple, Type, Union, Literal

import sat_utils
from sat_utils import CNF, Element

Element = str


class Literal(Enum):
    """Enum subclass to have the member's value be equal to its name."""

    @staticmethod
    def _generate_next_value_(name, start, count, last_values) -> Element:
        return name


def comb(value: Literal, house: int) -> Element:
    """Format how a value is shown at a given house"""

    return f"{value} {house}"


def found_at(value: Literal, house: int) -> List[Tuple[Element]]:
    """Value known to be at a specific house"""

    return [(comb(value, house),)]


def same_house(value1: Literal, value2: Literal):
    """The two values occur in the same house: brit1 & red1 | brit2 & red2 ..."""

    return sat_utils.from_dnf((comb(value1, i), comb(value2, i)) for i in houses)


def consecutive(value1: Literal, value2: Literal):
    """The values are in consecutive houses: green1 & white2 | green2 & white3 ..."""

    return sat_utils.from_dnf(
        (comb(value1, i), comb(value2, j)) for i, j in zip(houses, houses[1:])
    )


def beside(value1: Literal, value2: Literal):
    """The values occur side-by-side: blends1 & cat2 | blends2 & cat1 ..."""

    return sat_utils.from_dnf(
        [(comb(value1, i), comb(value2, j)) for i, j in zip(houses, houses[1:])]
        + [(comb(value2, i), comb(value1, j)) for i, j in zip(houses, houses[1:])]
    )


def left_of(value1: Literal, value2: Literal):
    """The first value is somewhere to the left of the second value."""

    return sat_utils.from_dnf(
        (comb(value1, i), comb(value2, j)) for i, j in product(houses, houses) if i < j
    )


def right_of(value1: Literal, value2: Literal):
    """The first value is somewhere to the right of the second value."""

    return sat_utils.from_dnf(
        (comb(value1, i), comb(value2, j)) for i, j in product(houses, houses) if i > j
    )


def one_between(value1: Literal, value2: Literal):
    """The values have one other value in between: cat1 & x2 & dog3 | dog2 & x3 & cat1 ..."""

    return sat_utils.from_dnf(
        [(comb(value1, i), comb(value2, j)) for i, j in zip(houses, houses[2:])]
        + [(comb(value2, i), comb(value1, j)) for i, j in zip(houses, houses[2:])]
    )


def two_between(value1: Literal, value2: Literal):
    """The values have two other values in between: cat1 & x2 & y3 & dog4 | ..."""

    return sat_utils.from_dnf(
        [(comb(value1, i), comb(value2, j)) for i, j in zip(houses, houses[3:])]
        + [(comb(value2, i), comb(value1, j)) for i, j in zip(houses, houses[3:])]
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
literals: List[Literal] = [el.value for group in enum_classes for el in group]

# set up the puzzle with constraints and clues
cnf: CNF = []

# # each house gets exactly one value from each attribute group
for house in houses:
    for enum_type in enum_classes:
        cnf += sat_utils.one_of(comb(value, house) for value in enum_type)

# each value gets assigned to exactly one house
for literal in literals:
    cnf += sat_utils.one_of(comb(literal, house) for house in houses)

cnf += same_house(Nationality.brit, Color.red)
cnf += same_house(Nationality.swede, Animal.dog)
cnf += same_house(Nationality.dane, Drink.tea)
cnf += consecutive(Color.green, Color.white)
cnf += same_house(Color.green, Drink.coffee)
cnf += same_house(Cigar.pall_mall, Animal.bird)
cnf += same_house(Color.yellow, Cigar.dunhill)
cnf += found_at(Drink.milk, 3)
cnf += found_at(Nationality.norwegian, 1)
cnf += beside(Cigar.blends, Animal.cat)
cnf += beside(Animal.horse, Cigar.dunhill)
cnf += same_house(Cigar.blue_master, Drink.root_beer)
cnf += same_house(Nationality.german, Cigar.prince)
cnf += beside(Nationality.norwegian, Color.blue)
cnf += beside(Cigar.blends, Drink.water)

sol = sat_utils.solve_one(cnf)
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
cnf: CNF = []

# each house gets exactly one value from each attribute group
for house in houses:
    for group in enum_classes:
        cnf += sat_utils.one_of(comb(value, house) for value in group)

# each value gets assigned to exactly one house
for value in literals:
    cnf += sat_utils.one_of(comb(value, house) for house in houses)


# 1. There is one chair between the place setting with Lilies and the one eating Grilled Cheese.
cnf += one_between(Flowers.lilies, Foods.grilled_cheese)

# 2. There is one chair between Timothy's Mom and the one eating Stew.
cnf += one_between(Children.timothy, Foods.stew)

# 3. There are two chairs between the Bella's Mom and Penny's seat on the right.
cnf += two_between(Children.bella, Mothers.penny)
cnf += right_of(Mothers.penny, Children.bella)

# 4. There is one chair between the place setting with Roses and the one eating Spaghetti on the left.
cnf += one_between(Flowers.roses, Foods.spaghetti)
cnf += left_of(Foods.spaghetti, Flowers.roses)

# 5. There are two chairs between the place setting with Carnations and Samantha's Mom.
cnf += two_between(Flowers.carnations, Children.samantha)

# 6. There is one chair between Meredith's Mom and Timothy's Mom on the left.
cnf += one_between(Children.meredith, Children.timothy)
cnf += left_of(Children.timothy, Children.meredith)

# 7. Aniya's place setting has a lovely Carnation bouquet.
cnf += same_house(Mothers.aniya, Flowers.carnations)

# 8. There are two chairs between the one eating Grilled Cheese and the one eating Spaghetti.
cnf += two_between(Foods.grilled_cheese, Foods.spaghetti)

# 9. The person in the first chair (left-most) is eating Pizza.
cnf += found_at(Foods.pizza, 1)

# 10. The Tulips were placed at one of the place settings somewhere to the left of Penny's chair.
cnf += left_of(Flowers.tulips, Mothers.penny)

# 11. There are two chairs between the one eating Spaghetti and Kailyn's seat.
cnf += two_between(Foods.spaghetti, Mothers.kailyn)

# 12. There is one chair between the one eating Pizza and Holly's chair on the right.
cnf += one_between(Foods.pizza, Mothers.holly)
cnf += right_of(Mothers.holly, Foods.pizza)

all_solutions = sat_utils.solve_all(cnf)
print(f"{len(all_solutions)} solutions found")
print(all_solutions)
