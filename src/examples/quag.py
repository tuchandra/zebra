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

from __future__ import annotations

from src import sat_utils
from src.clues import (
    found_at,
    left_of,
    one_between,
    right_of,
    same_house,
    two_between,
)
from src.elements import PuzzleElement
from src.puzzle import Puzzle


class Children(PuzzleElement):
    @classmethod
    def description(cls) -> str:
        return "Each mother is accompanied by their child: Bella, Fred, Meredith, Samantha, Timothy."

    bella = "Bella's mother"
    fred = "the mother Fred"
    meredith = "Meredith's mom"
    samantha = "Samantha's mom"
    timothy = "the mother of Timothy"


class Flower(PuzzleElement):
    @classmethod
    def description(cls) -> str:
        return "They all have a different favorite flower: carnations, daffodils, lilies, roses, tulips."

    carnations = "a carnations arrangement"
    daffodils = "a bouquet of daffodils"
    lilies = "the boquet of lilies"
    roses = "the rose bouquet"
    tulips = "the vase of tulips"


class Food(PuzzleElement):
    @classmethod
    def description(cls) -> str:
        return "Everyone has something different for lunch: grilled cheese, pizza, spaghetti, stew, stir fry."

    grilled_cheese = "the person eating grilled cheese"
    pizza = "the pizza lover"
    spaghetti = "the spaghetti eater"
    stew = "the one having stew"
    stir_fry = "the person with stir fry"


class Mother(PuzzleElement):
    @classmethod
    def description(cls) -> str:
        return "The mothers' names are Aniya, Holly, Janelle, Kaillyn, Penny."

    aniya = "Aniya"
    holly = "Holly"
    janelle = "Janelle"
    kailyn = "Kailyn"
    penny = "Penny"


if __name__ == "__main__":
    enum_classes: list[type[PuzzleElement]] = [Mother, Children, Flower, Food]
    literals = [el for group in enum_classes for el in group]

    # set up the puzzle with constraints and clues
    puzzle = Puzzle(element_types=[Mother, Children, Flower, Food])

    puzzle = (
        puzzle.set_constraints()
        # 1. There is one chair between the place setting with Lilies and the one eating Grilled Cheese.
        .add_clue(one_between(Flower.lilies, Food.grilled_cheese))
        # 2. There is one chair between Timothy's Mom and the one eating Stew.
        .add_clue(one_between(Children.timothy, Food.stew))
        # 3. There are two chairs between the Bella's Mom and Penny's seat on the right.
        .add_clue(two_between(Children.bella, Mother.penny))
        .add_clue(right_of(Mother.penny, Children.bella))
        # 4. There is one chair between the place setting with Roses and the one eating Spaghetti on the left.
        .add_clue(one_between(Flower.roses, Food.spaghetti))
        .add_clue(left_of(Food.spaghetti, Flower.roses))
        # 5. There are two chairs between the place setting with Carnations and Samantha's Mom.
        .add_clue(two_between(Flower.carnations, Children.samantha))
        # 6. There is one chair between Meredith's Mom and Timothy's Mom on the left.
        .add_clue(one_between(Children.meredith, Children.timothy))
        .add_clue(left_of(Children.timothy, Children.meredith))
        # 7. Aniya's place setting has a lovely Carnation bouquet.
        .add_clue(same_house(Mother.aniya, Flower.carnations))
        # 8. There are two chairs between the one eating Grilled Cheese and the one eating Spaghetti.
        .add_clue(two_between(Food.grilled_cheese, Food.spaghetti))
        # 9. The person in the first chair (left-most) is eating Pizza.
        .add_clue(found_at(Food.pizza, 1))
        # 10. The Tulips were placed at one of the place settings somewhere to the left of Penny's chair.
        .add_clue(left_of(Flower.tulips, Mother.penny))
        # 11. There are two chairs between the one eating Spaghetti and Kailyn's seat.
        .add_clue(two_between(Food.spaghetti, Mother.kailyn))
        # 12. There is one chair between the one eating Pizza and Holly's chair on the right.
        .add_clue(one_between(Food.pizza, Mother.holly))
        .add_clue(right_of(Mother.holly, Food.pizza))
    )

    print(puzzle)
    all_solutions = sat_utils.solve_all(puzzle.as_cnf())
    print(f"{len(all_solutions)} solutions found")
    print(all_solutions)
