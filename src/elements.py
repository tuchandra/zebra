"""
elements.py

This is a collection of "puzzle elements"---categories, literals, whatever you want to call
them---which are used as the building blocks of zebra puzzles. Examples include people's
favorite colors, preferred drinks, pets, etc.

Each class must provide (but we have no way of enforcing this) a description of each
puzzle element. These get used to make human-readable clues. The classes must also provide
a custom __repr__ method that gets used in the puzzle description.

Included is a base PuzzleElement class from which all literals should inherit. To extend these,
just import PuzzleElement and implement a class like the ones here.
"""

from enum import StrEnum


class PuzzleElement(StrEnum):
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


class Kaya(PuzzleElement):
    @classmethod
    def description(cls) -> str:
        return "They are five different types of Kaya"

    joy = "the Kaya of Joy"
    life = "the Kaya of Life"
    harmony = "the Kaya of Harmony"
    wisdom = "the Kaya of Wisdom"
    love = "the Kaya of Love"


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
    "RecolorMedal",
    "NPC",
    "FavoriteGame",
    "Kaya",
    "Egg",
    "Dinomon",
    "UchiType",
    "UchiPrimary",
    "UchiSecondary",
]
