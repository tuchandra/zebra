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

from __future__ import annotations

from elements import PuzzleElement

from src import sat_utils
from src.clues import beside, consecutive, found_at, same_house
from src.puzzle import Puzzle


class Color(PuzzleElement):
    @classmethod
    def description(cls) -> str:
        return "Each person has a favorite color: yellow, red, white, green, or blue."

    yellow = "the person who loves yellow"
    red = "the person whose favorite color is red"
    white = "the person who loves white"
    green = "the person whose favorite color is green"
    blue = "the person who loves blue"


class Nationality(PuzzleElement):
    @classmethod
    def description(cls) -> str:
        return "The people are of nationalities: Danish, British, Swedish, Norwegian, German."

    dane = "the Dane"
    brit = "the British person"
    swede = "the Swedish person"
    norwegian = "the Norwegian"
    german = "the German"


class Animal(PuzzleElement):
    @classmethod
    def description(cls) -> str:
        return "The people keep different animals: horses, cats, birds, fish, and dogs."

    horse = "the person who keeps horses"
    cat = "the cat lover"
    bird = "the bird keeper"
    fish = "the fish enthusiast"
    dog = "the dog owner"


class Drink(PuzzleElement):
    @classmethod
    def description(cls) -> str:
        return "Each person has a favorite drink: water, tea, milk, coffee, and root beer."

    water = "the one who only drinks water"
    tea = "the tea drinker"
    milk = "the person who likes milk"
    coffee = "the coffee drinker"
    root_beer = "the root beer lover"


class Cigar(PuzzleElement):
    @classmethod
    def description(cls) -> str:
        return "Everyone has a different favorite cigar: Pall Mall, Prince, Blue Master, Dunhill, and blends."

    pall_mall = "the person partial to Pall Mall"
    prince = "the Prince smoker"
    blue_master = "the person who smokes Blue Master"
    dunhill = "the Dunhill smoker"
    blends = "the person who smokes many different blends"


if __name__ == "__main__":
    enum_classes: list[type[PuzzleElement]] = [Color, Nationality, Animal, Drink, Cigar]
    literals: list[PuzzleElement] = [el for group in enum_classes for el in group]

    # set up the puzzle with constraints and clues
    puzzle = Puzzle(element_types=[Color, Nationality, Drink, Cigar, Animal])

    puzzle = (
        puzzle.set_constraints()
        .add_clue(same_house(Nationality.brit, Color.red))
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
