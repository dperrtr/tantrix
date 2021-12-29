"""

DavidPerruchoud (created on 27/12/2021)
"""
from itertools import cycle

DIRECTIONS = ['NW', 'NE', 'E', 'SE', 'SW', 'W']


class CyclerA:
    """A helper class to find combination of rotations (direction) of a TantrixHex."""
    def __init__(self):
        self.wheel = cycle(DIRECTIONS)
        self.current = next(self.wheel)

    def set_entry(self, direction):
        """Define the entry of a line (from which direction a line is coming)."""
        assert direction in DIRECTIONS
        while self.current != direction:
            self.current = next(self.wheel)

    def turn(self, number: int):
        """Rotate the Cycler by N ticks."""
        number = number % 6
        if number == 0:
            return
        for __ in range(number - 1):
            next(self.wheel)
        self.current = next(self.wheel)


if __name__ == '__main__':
    cy = Cycler()
    assert cy.current == 'NW'
    cy.turn(2)
    assert cy.current == 'E'
    cy.set_entry('SE')
    assert cy.current == 'SE'
    cy.turn(-1)
    assert cy.current == 'E'
    cy.set_entry('W')
    assert cy.current == 'W'
    cy.turn(3)
    assert cy.current == 'E'
    cy.set_entry('W')
    assert cy.current == 'W'
    cy.turn(-3)
    assert cy.current == 'E'
    cy.turn(12)
    assert cy.current == 'E'
    cy.turn(-8)
    assert cy.current == 'NW'
    cy.turn(0)
    assert cy.current == 'NW'