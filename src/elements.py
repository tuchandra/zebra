"""
literals.py

This is a collection of "puzzle elements"---categories, literals, whatever you want to call
them---which are used as the building blocks of zebra puzzles. Examples include people's
favorite colors, preferred drinks, pets, etc.

Each class must provide (but we have no way of enforcing this) a description of each
puzzle element. These get used to make human-readable clues. The classes must also provide
a custom __repr__ method that gets used in the puzzle description.

Included is a base PuzzleElement class from which all literals should inherit. To extend these,
just import PuzzleElement and implement a class like the ones here.
"""

from enum import Enum


class PuzzleElement(Enum):
    """
    Common parent class for all puzzle elements (colors, occupations, pets, etc.).

    We can't make this an ABC because ABC and Enum have different metaclasses, and that'd be
    super confusing. But override the description method!
    """

    @classmethod
    def description(cls) -> str:
        return "".join(cls.__members__)  # type:ignore


class Kiro(PuzzleElement):
    @classmethod
    def description(cls) -> str:
        return "Each house has a different type of Kiro"

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


class Smoothie(PuzzleElement):
    @classmethod
    def description(cls) -> str:
        return "Everyone has a favorite smoothie"

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


class Bottlecap(PuzzleElement):
    @classmethod
    def description(cls) -> str:
        return "Everyone keeps a certain type of Bottlecap"

    red = "the adoptable who has red bottlecaps"
    yellow = "the adoptable who likes YBC"
    green = "the GBC keeper"
    blue = "the blue bottlecap hoarder"
    silver = "the SBC winner"


class RecolorMedal(PuzzleElement):
    @classmethod
    def description(cls) -> str:
        return "Everyone has a recolor or medal"

    top_level = "the top level adoptable"
    second_ed = "the 2nd edition adoptable"
    ghost = "the ghost recolor"
    pink = "the pink adoptable"
    gold = "the adoptable with a heart of gold"


class NPC(PuzzleElement):
    @classmethod
    def description(cls) -> str:
        return "Each is an NPC on the site"

    jim = "Dirt Digger Jim"
    amelia = "Amelia"
    chip = "Fishin' Chip"
    riley = "Ringmaster Riley"
    crowley = "Crowley"
    silver = "Silver the Kua"
    jagger = "Jagger"


class FavoriteGame(PuzzleElement):
    @classmethod
    def description(cls) -> str:
        return "Everyone has a favorite game"

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


class Tribe(PuzzleElement):
    @classmethod
    def description(cls) -> str:
        return "Everyone has an Altazan tribe"

    quake = "the one in the Quake tribe"
    cursed = "the Cursed tribe member"
    forest = "the Forest tribe member"
    volcano = "the adoptable in the Volcano tribe"
    storm = "the adoptable in the Storm tribe"


class Kaya(PuzzleElement):
    @classmethod
    def description(cls) -> str:
        return "They are five different types of Kaya"

    joy = "the Kaya of Joy"
    life = "the Kaya of Life"
    harmony = "the Kaya of Harmony"
    wisdom = "the Kaya of Wisdom"
    love = "the Kaya of Love"


class TropicalTraptorPrimary(PuzzleElement):
    @classmethod
    def description(cls) -> str:
        return "They have different primary colors"

    majestic = "the Majestic Traptor"
    grand = "the Grand Traptor"
    stunning = "the Stunning Traptor"
    marvellous = "the Marvellous Traptor"
    heroic = "the Heroic Traptor"


class TropicalTraptorSecondary(PuzzleElement):
    @classmethod
    def description(cls) -> str:
        return "They have different secondary colors"

    sky = "the Sky Traptor"
    forest = "the Forest Traptor"
    night = "the Night Traptor"
    sun = "the Sun Traptor"
    sand = "the Sand Traptor"


class TropicalTraptorTertiary(PuzzleElement):
    @classmethod
    def description(cls) -> str:
        return "They have different tertiary colors"

    soarer = "the Soarer Traptor"
    diver = "the Diver Traptor"
    screecher = "the Screecher Traptor"
    hunter = "the Hunter Traptor"
    nurturer = "the Nurturer Traptor"


class MythicalTraptorPrimary(PuzzleElement):
    @classmethod
    def description(cls) -> str:
        return "They have different primary colors"

    greater = "the Greater Traptor"
    lesser = "the Lesser Traptor"
    fierce = "the Fierce Traptor"
    restless = "the Restless Traptor"
    ancient = "the Ancient Traptor"


class MythicalTraptorSecondary(PuzzleElement):
    @classmethod
    def description(cls) -> str:
        return "They have different secondary colors"

    lake = "the Lake Traptor"
    swamp = "the Swamp Traptor"
    cave = "the Cave Traptor"
    volcano = "the Volcano Traptor"
    mountain = "the Mountain Traptor"


class MythicalTraptorTertiary(PuzzleElement):
    @classmethod
    def description(cls) -> str:
        return "They have different tertiary colors"

    dweller = "the Dweller Traptor"
    crawler = "the Crawler Traptor"
    stalker = "the Stalker Traptor"
    hoarder = "the Hoarder Traptor"
    snapper = "the Snapper Traptor"


class Egg(PuzzleElement):
    @classmethod
    def description(cls) -> str:
        return "They are each giving out a type of egg"

    golden = "the one giving out Golden Eggs"
    trollden = "the one who keeps Trollden Eggs"
    topaz = "the one with Topaz Eggs"
    crystal = "the one giving out Crystal Eggs"
    traptor = "the one who has Traptor Eggs"
    marinodon = "the one giving out Marinodon Eggs"


class Dinomon(PuzzleElement):
    @classmethod
    def description(cls) -> str:
        return "Each is a different species of Dinomon"

    terasaur = "the Terasaur"
    carnodon = "the Carnodon"
    silosaur = "the Silosaur"
    marinodon = "the Marinodon"
    traptor = "the Traptor"


class UchiType(PuzzleElement):
    @classmethod
    def description(cls) -> str:
        return "Each is a different type of Uchi"

    skunk = "the Skunk Uchi"
    eyes = "the Eyes Uchi"
    umbral = "the Umbral Uchi"
    mummy = "the Mummy Uchi"


class UchiPrimary(PuzzleElement):
    @classmethod
    def description(cls) -> str:
        return "Each Uchi has a different body color"

    blue = "the blue body Uchi"
    red = "the Uchi with a red body"
    yellow = "the yellow body Uchi"
    green = "the Uchi with a green body"


class UchiSecondary(PuzzleElement):
    @classmethod
    def description(cls) -> str:
        return "Each Uchi has a different secondary color (e.g., eyes, umbral, etc.)"

    black = "the Uchi with secondary color black"
    orange = "the Uchi with secondary color orange"
    purple = "the Uchi with secondary color purple"
    white = "the Uchi with secondary color white"


__all__ = [
    "PuzzleElement",
    "Smoothie",
    "Bottlecap",
    "RecolorMedal",
    "NPC",
    "FavoriteGame",
    "Tribe",
    "Kaya",
    "TropicalTraptorPrimary",
    "TropicalTraptorSecondary",
    "TropicalTraptorTertiary",
    "Egg",
    "Dinomon",
    "UchiType",
    "UchiPrimary",
    "UchiSecondary",
]
