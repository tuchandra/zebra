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


class Mother(Literal):
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


class Flower(Literal):
    @classmethod
    def description(cls) -> str:
        return f"They all have a different favorite flower: carnations, daffodils, lilies, roses, tulips."

    carnations = "a carnations arrangement"
    daffodils = "a bouquet of daffodils"
    lilies = "the boquet of lilies"
    roses = "the rose bouquet"
    tulips = "the vase of tulips"


class Food(Literal):
    @classmethod
    def description(cls) -> str:
        return f"Everyone has something different for lunch: grilled cheese, pizza, spaghetti, stew, stir fry."

    grilled_cheese = "the person eating grilled cheese"
    pizza = "the pizza lover"
    spaghetti = "the spaghetti eater"
    stew = "the one having stew"
    stir_fry = "the person with stir fry"


class Kiro(Literal):
    @classmethod
    def description(cls) -> str:
        return f"Each house has a different type of Kiro: Kaya, Silosaur Costume, Sugar Sketch, Traptor Costume, and Skeleko."

    kaya = "the Kaya Kiro"
    silosaur = "the Kiro disguised as a Silosaur"
    sugar_sketch = "the Sugar Sketch Kiro"
    traptor_costume = "the Kiro in a Traptor costume"
    skeleko = "the Skeleko Kiro"


class Smoothie(Literal):
    @classmethod
    def description(cls) -> str:
        return f"Everyone has a favorite smoothie: Cherry, Watermelon, Spring, Dusk, Lilac."

    cherry = "the adoptable who likes Cherry smoothies"
    watermelon = "the Watermelon smoothie lover"
    spring = "the adoptable who likes Spring smoothies"
    dusk = "the adoptable whose favorite smoothie is Dusk"
    lilac = "the Lilac smoothie drinker"


class Smoothie2(Literal):
    @classmethod
    def description(cls) -> str:
        return f"Everyone has a favorite smoothie: Blueberry, Lemon, Phantom Spring, Sakura, Butterscotch."

    blueberry = "the adoptable who likes Blueberry smoothies"
    lemon = "the Lemon smoothie lover"
    phantom_spring = "the adoptable who likes Phantom Spring smoothies"
    sakura = "the adoptable whose favorite smoothie is Sakura"
    butterscotch = "the Butterscotch smoothie drinker"


class Smoothie3(Literal):
    @classmethod
    def description(cls) -> str:
        return f"Everyone has a favorite smoothie: Dawn, Desert, Lime, Abyss, Life."

    dawn = "the adoptable who likes Dawn smoothies"
    desert = "the Desert smoothie lover"
    lime = "the adoptable who likes Lime smoothies"
    abyss = "the adoptable whose favorite smoothie is Abyss"
    life = "the Life smoothie drinker"


class Bottlecap(Literal):
    @classmethod
    def description(cls) -> str:
        return f"Everyone keeps a certain type of Bottlecap: red, yellow, green, blue, silver."

    red = "the adoptable who has red bottlecaps"
    yellow = "the adoptable who likes YBC"
    green = "the GBC keeper"
    blue = "the blue bottlecap hoarder"
    silver = "the SBC winner"


class RecolorMedal(Literal):
    @classmethod
    def description(cls) -> str:
        return f"Everyone is special in some way: 1st place, 2nd ed, ghost, pink, gold."

    first = "the 1st place adoptable"
    second_ed = "the 2nd edition adoptable"
    ghost = "the ghost recolor"
    pink = "the pink adoptable"
    gold = "the adoptable with a heart of gold"


class FavoriteGame(Literal):
    @classmethod
    def description(cls) -> str:
        return f"Everyone has a favorite game: Dirt Digger, Guess the Number, Fishing Fever, Wonder Wheel, Quality Assurance."

    dirt_digger = "the adoptable who likes Dirt Digger"
    guess_the_number = "the one who plays Guess the Number"
    fishing_fever = "the Fishing Fever lover"
    wonder_wheel = "the adoptable who spins the Wonder Wheel"
    quality_assurance = "the adoptable who plays Quality Assurance"


class Tribe(Literal):
    @classmethod
    def description(cls) -> str:
        return f"Everyone has an Altazan tribe: Quake, Cursed, Forest, Volcano, Storm."

    quake = "the one in the Quake tribe"
    cursed = "the Cursed tribe member"
    forest = "the Forest tribe member"
    volcano = "the adoptable in the Volcano tribe"
    storm = "the adoptable in the Storm tribe"


class Kaya(Literal):
    @classmethod
    def description(cls) -> str:
        return f"They are of five different types: Joy, Life, Harmony, Wisdom, Love."

    joy = "the Kaya of Joy"
    life = "the Kaya of Life"
    harmony = "the Kaya of Harmony"
    wisdom = "the Kaya of Wisdom"
    love = "the Kaya of Love"

