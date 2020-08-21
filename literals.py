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
        return f"Each house has a different type of Kiro"

    kaya = "the Kaya Kiro"
    sugar_sketch = "the Sugar Sketch Kiro"
    silosaur = "the Kiro disguised as a Silosaur"
    skyrant = "the Kiro in a Skyrant costume "
    traptor_costume = "the Kiro in a Traptor costume"
    terasaur_costume = "the Terasaur Costume Kiro"
    skeleko = "the Skeleko Kiro"
    zodiac_dragon = "the Zodiac Dragon Kiro"
    gem_dragon = "the Gem Dragon Kiro"
    plushie = "the Plushie Kiro"
    gloray = "the Gloray Kiro"
    rabbit = "the Rabbit Kiro"
    holiday_sweets = "the Holiday Sweets Kiro"
    baby = "the Baby Kiro"
    zaeris = "the Zaeris Kiro"


class Smoothie(Literal):
    @classmethod
    def description(cls) -> str:
        return f"Everyone has a favorite smoothie"

    cherry = "the adoptable who likes Cherry smoothies"
    desert = "the Desert smoothie lover"
    watermelon = "the Watermelon smoothie lover"
    dragonfruit = "the Dragonfruit smoothie lover"
    lime = "the adoptable who drinks Lime smoothies"
    blueberry = "the adoptable who drinks Blueberry smoothies"
    lemon = "the Lemon smoothie lover"
    dusk = "the adoptable whose favorite smoothie is Dusk"
    dawn = "the adoptable who likes Dawn smoothies"
    spring = "the adoptable who likes Spring smoothies"
    seafoam = "the adoptable who likes Seafoam smoothies"
    phantom_spring = "the adoptable who likes Phantom Spring smoothies"
    abyss = "the adoptable whose favorite smoothie is Abyss"
    butterscotch = "the Butterscotch smoothie drinker"
    lilac = "the Lilac smoothie drinker"
    sakura = "the adoptable whose favorite smoothie is Sakura"
    life = "the Life smoothie drinker"
    darkness = "the Darkness smoothie drinker"
    earth = "the adoptable who likes Earth smoothies"


class Bottlecap(Literal):
    @classmethod
    def description(cls) -> str:
        return f"Everyone keeps a certain type of Bottlecap"

    red = "the adoptable who has red bottlecaps"
    yellow = "the adoptable who likes YBC"
    green = "the GBC keeper"
    blue = "the blue bottlecap hoarder"
    silver = "the SBC winner"


class RecolorMedal(Literal):
    @classmethod
    def description(cls) -> str:
        return f"Everyone has a recolor or medal"

    top_level = "the top level adoptable"
    second_ed = "the 2nd edition adoptable"
    ghost = "the ghost recolor"
    pink = "the pink adoptable"
    gold = "the adoptable with a heart of gold"


class NPC(Literal):
    @classmethod
    def description(cls) -> str:
        return f"Each is an NPC on the site"

    jim = "Dirt Digger Jim"
    amelia = "Amelia"
    chip = "Fishin' Chip"
    riley = "Ringmaster Riley"
    crowley = "Crowley"
    silver = "Silver the Kua"
    jagger = "Jagger"


class FavoriteGame(Literal):
    @classmethod
    def description(cls) -> str:
        return f"Everyone has a favorite game"

    dirt_digger = "the adoptable who likes Dirt Digger"
    guess_the_number = "the one who plays Guess the Number"
    fishing_fever = "the Fishing Fever lover"
    sock_summoning = "the adoptable who plays Sock Summoning"
    wonder_wheel = "the adoptable who spins the Wonder Wheel"
    fetch = "the adoptable playing Fetch"
    quality_assurance = "the adoptable who plays Quality Assurance"
    stop_and_swap = "the one who often plays Stop and Swap"
    uchi_fusion = "the one who plays Uchi Fusion"
    freedom_forest = "the one in Freedom Forest"


class Tribe(Literal):
    @classmethod
    def description(cls) -> str:
        return f"Everyone has an Altazan tribe"

    quake = "the one in the Quake tribe"
    cursed = "the Cursed tribe member"
    forest = "the Forest tribe member"
    volcano = "the adoptable in the Volcano tribe"
    storm = "the adoptable in the Storm tribe"


class Kaya(Literal):
    @classmethod
    def description(cls) -> str:
        return f"They are five different types of Kaya"

    joy = "the Kaya of Joy"
    life = "the Kaya of Life"
    harmony = "the Kaya of Harmony"
    wisdom = "the Kaya of Wisdom"
    love = "the Kaya of Love"


class TraptorPrimary(Literal):
    @classmethod
    def description(cls) -> str:
        return f"They have different primary colors"

    majestic = "the Majestic Traptor"
    grand = "the Grand Traptor"
    stunning = "the Stunning Traptor"
    marvellous = "the Marvellous Traptor"
    heroic = "the Heroic Traptor"


class TraptorSecondary(Literal):
    @classmethod
    def description(cls) -> str:
        return f"They have different secondary colors"

    sky = "the Sky Traptor"
    forest = "the Forest Traptor"
    night = "the Night Traptor"
    sun = "the Sun Traptor"
    sand = "the Sand Traptor"


class TraptorTertiary(Literal):
    @classmethod
    def description(cls) -> str:
        return f"They have different tertiary colors"

    soarer = "the Soarer Traptor"
    diver = "the Diver Traptor"
    screecher = "the Screecher Traptor"
    hunter = "the Hunter Traptor"
    nurturer = "the Nurturer Traptor"


class Egg(Literal):
    @classmethod
    def description(cls) -> str:
        return f"They are each giving out a type of egg"

    golden = "the one giving out Golden Eggs"
    trollden = "the one who keeps Trollden Eggs"
    topaz = "the one with Topaz Eggs"
    crystal = "the one giving out Crystal Eggs"
    traptor = "the one who has Traptor Eggs"
    marinodon = "the one giving out Marinodon Eggs"


class Dinomon(Literal):
    @classmethod
    def description(cls) -> str:
        return f"Each is a different species of Dinomon"

    terasaur = "the Terasaur"
    carnodon = "the Carnodon"
    silosaur = "the Silosaur"
    marinodon = "the Marinodon"
    traptor = "the Traptor"


class UchiType(Literal):
    @classmethod
    def description(cls) -> str:
        return f"Each is a different type of Uchi"

    skunk = "the Skunk Uchi"
    eyes = "the Eyes Uchi"
    umbral = "the Umbral Uchi"
    mummy = "the Mummy Uchi"


class UchiPrimary(Literal):
    @classmethod
    def description(cls) -> str:
        return f"Each Uchi has a different body color"

    blue = "the blue body Uchi"
    red = "the Uchi with a red body"
    yellow = "the yellow body Uchi"
    green = "the Uchi with a green body"


class UchiSecondary(Literal):
    @classmethod
    def description(cls) -> str:
        return f"Each Uchi has a different secondary color (e.g., eyes, umbral, etc.)"

    black = "the Uchi with secondary color black"
    orange = "the Uchi with secondary color orange"
    purple = "the Uchi with secondary color purple"
    white = "the Uchi with secondary color white"
