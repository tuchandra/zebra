"""
traptor_elements.py

Elements that are specific to the Traptor puzzles. These make it easier to generate
puzzles repeatably and in natural language.
"""

from src.elements import PuzzleElement


class Tribe(PuzzleElement):
    @classmethod
    def description(cls) -> str:
        return "Each has somehow joined an Altazan tribe."

    quake = "the Quake tribe member"
    cursed = "the Cursed tribe member"
    forest = "the Forest tribe member"
    volcano = "the Volcano tribe member"
    storm = "the Storm tribe member"


class Bottlecap(PuzzleElement):
    @classmethod
    def description(cls) -> str:
        return "Each nest has a different bottlecap in it."

    red = "the red bottlecaps"
    yellow = "the yellow bottlecaps"
    green = "the green bottlecaps"
    blue = "the blue bottlecaps"
    black = "the black bottlecaps"


class Smoothie(PuzzleElement):
    @classmethod
    def description(cls) -> str:
        return "Each nest has a smoothie in it."

    blueberry = "the Blueberry smoothie"
    cherry = "the Cherry smoothie"
    chocolate = "the Chocolate smoothie"
    coconut = "the Coconut smoothie"
    dragonfruit = "the Dragonfruit smoothie"
    grape = "the Grape smoothie"
    lemon = "the Lemon smoothie"
    licorice = "the Licorice smoothie"
    lime = "the Lime smoothie"
    orange = "the Orange smoothie"

    midnight = "the Midnight smoothie"
    poison = "the Poison smoothie"
    flamingle = "the Flamingle smoothie"
    kiwi = "the Kiwi smoothie"
    pomegranate = "the Pomegranate smoothie"
    starfruit = "the Starfruit smoothie"
    watermelon = "the Watermelon smoothie"

    # pastels - excluded

    desert = "the Desert smoothie"
    jungle = "the Jungle smoothie"
    glacier = "the Glacier smoothie"


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


__all__ = [
    "Tribe",
    "Smoothie",
    "Bottlecap",
    "TropicalTraptorPrimary",
    "TropicalTraptorSecondary",
    "TropicalTraptorTertiary",
    "MythicalTraptorPrimary",
    "MythicalTraptorSecondary",
    "MythicalTraptorTertiary",
]
