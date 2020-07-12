"""
literals.py

This is a collection of "puzzle elements"---categories, literals, whatever you want to call
them---which are used as the building blocks of zebra puzzles. Examples include people's
favorite colors, preferred drinks, pets, etc.

Each class must provide (but we have no way of enforcing this) a description of each
puzzle element. These get used to make human-readable clues. The classes must also provide
a custom __repr__ method that gets used in the puzzle description.

Included is a base Literal class from which all literals should inherit. To extend these,
just import Literal and implement a class like the ones here.

"""

from enum import Enum


class Literal(Enum):
    """
    Common parent class for all puzzle elements (colors, occupations, pets, etc.).

    We can't make this an ABC because ABC and Enum have different metaclasses, and that'd be
    super confusing. But override the description method!
    """

    @classmethod
    def description(cls) -> str:
        return "".join(cls.__members__)  # type:ignore


class Color(Literal):
    @classmethod
    def description(cls) -> str:
        return f"Each person has a favorite color: yellow, red, white, green, or blue."

    yellow = "the person who loves yellow"
    red = "the person whose favorite color is red"
    white = "the person who loves white"
    green = "the person whose favorite color is green"
    blue = "the person who loves blue"


class Nationality(Literal):
    @classmethod
    def description(cls) -> str:
        return f"The people are of nationalities: Danish, British, Swedish, Norwegian, German."

    dane = "the Dane"
    brit = "the British person"
    swede = "the Swedish person"
    norwegian = "the Norwegian"
    german = "the German"


class Animal(Literal):
    @classmethod
    def description(cls) -> str:
        return f"The people keep different animals: horses, cats, birds, fish, and dogs."

    horse = "the person who keeps horses"
    cat = "the cat lover"
    bird = "the bird keeper"
    fish = "the fish enthusiast"
    dog = "the dog owner"


class Drink(Literal):
    @classmethod
    def description(cls) -> str:
        return f"Each person has a favorite drink: water, tea, milk, coffee, and root beer."

    water = "the one who only drinks water"
    tea = "the tea drinker"
    milk = "the person who likes milk"
    coffee = "the coffee drinker"
    root_beer = "the root beer lover"


class Cigar(Literal):
    @classmethod
    def description(cls) -> str:
        return f"Everyone has a different favorite cigar: Pall Mall, Prince, Blue Master, Dunhill, and blends."

    pall_mall = "the person partial to Pall Mall"
    prince = "the Prince smoker"
    blue_master = "the person who smokes Blue Master"
    dunhill = "the Dunhill smoker"
    blends = "the person who smokes many different blends"


class Mothers(Literal):
    @classmethod
    def description(cls) -> str:
        return f"The mothers' names are Aniya, Holly, Janelle, Kaillyn, Penny."

    aniya = "Aniya"
    holly = "Holly"
    janelle = "Janelle"
    kailyn = "Kailyn"
    penny = "Penny"


class Children(Literal):
    @classmethod
    def description(cls) -> str:
        return (
            f"Each mother is accompanied by their child: Bella, Fred, Meredith, Samantha, Timothy."
        )

    bella = "Bella's mother"
    fred = "the mother Fred"
    meredith = "Meredith's mom"
    samantha = "Samantha's mom"
    timothy = "the mother of Timothy"


class Flowers(Literal):
    @classmethod
    def description(cls) -> str:
        return f"They all have a different favorite flower: carnations, daffodils, lilies, roses, tulips."

    carnations = "a carnations arrangement"
    daffodils = "a bouquet of daffodils"
    lilies = "the boquet of lilies"
    roses = "the rose bouquet"
    tulips = "the vase of tulips"


class Foods(Literal):
    @classmethod
    def description(cls) -> str:
        return f"Everyone has something different for lunch: grilled cheese, pizza, spaghetti, stew, stir fry."

    grilled_cheese = "the person eating grilled cheese"
    pizza = "the pizza lover"
    spaghetti = "the spaghetti eater"
    stew = "the one having stew"
    stir_fry = "the person with stir fry"

