#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" This document contains the game's model. In here the games logic and tests are implemented.
"""

from template import Group, Terr_Template

BLACK = True
WHITE = False

class Model(Terr_Template):

    def __init__(self, n=11):
        """
        Initialises Game attributes.
        """
        # Gameplay attributes
        self.size = n  # size of board (int)
        self.turn = BLACK
        self.blocked_field = None  # Ko-rule
        self.has_passed = False
        self.game_over = False

        self.board = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.territory = [[None for _ in range(self.size)] for _ in range(self.size)]

        self.score = [0, 0]
        self.captured = [0, 0]

    def passing(self):
        """Checks if player has passed and changes the respective attributes accordingly.

        Returns:
            (bool): True if a player has passed or not, False if both players have passed
        """
        if self.game_over:
            return False

        if not self.has_passed:
            self.turn = not self.turn
            self.blocked_field = None
            self.has_passed = True
            return True

        self.game_over = True
        return True

    def _stones(self):
        """Creates a multidimensional list of the same shape as self.board containing the
        color of the stones on their respective coordinates (or None for no stone).

        Returns:
            (2d list): color of stones (shape of self.board)
        """
        stones = [[None for _ in range(self.size)] for _ in range(self.size)]
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[j][i] is None:
                    stones[j][i] = None
                else:
                    stones[j][i] = self.board[j][i].color
        return stones

    def get_data(self):
        """Prepares data for the GUI.

        Returns:
            (dict): all relevant information for the GUI (e.g. score, game status etc.)
        """
        data = {
            'size': self.size,
            'stones': self._stones(),
            'territory': self.territory,
            'game_over': self.game_over,
            'score': (self.score[0] + self.captured[0], self.score[1] + self.captured[1]),
            'color': self.turn
        }
        return data

    def _add(self, grp):
        """Iterates over group of stones and adds coordinate tuple to the board.

        Arguments:
            grp (Group): A group of stones
        """
        for i, j in grp.stones:
            self.board[j][i] = grp

    def _remove(self, grp):
        """Iterates over group of stones and sets the corresponding coordinates of the board to None.

        Arguments:
            grp (Group): A group of stones
        """
        for i, j in grp.stones:
            self.board[j][i] = None

    def _kill(self, grp):
        """Removes a group of stones from the game and increases the counter of
        captured stones.

        Arguments:
            grp (Group): The group that should be killed

        Attributes updated by this function:
            self.board
            self.captured
            self.group
        """
        self.captured[not grp.color] += grp.size
        self._remove(grp)

    def _liberties(self, grp):
        """ Counts the number of empty fields adjacent to the group.

            Arguments:
                grp (Group) : A group of stones

            Returns:
                (int)       : nr. of liberties of that group
        """
        count = 0
        for i in grp.border:
            if self.board[i[1]][i[0]] is None:
                count += 1
        return count

    def place_stone(self, x, y):
        """ Checks the validity of the stone to be placed.

            Arguments:
                x       : x-coordinate of stone to place
                y       : y-coordinate of stone to place
            Return:
                (bool)  : True if move is valid, False otherwise.
        """
        if self.blocked_field == (x, y):
            return False

        if self.game_over:
            return False
        if self.board[y][x] is not None:
            return False

        new = Group(stones=[(x, y)], color=self.turn)

        groups_to_remove = []
        self.groups_to_kill = []

        neighbouring_stones = ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))

        is_valid = False
        n = self.size

        for neighbour in neighbouring_stones:
            u, v = neighbour
            if u in range(n) and v in range(n):
                new.border.add(neighbour)
            else:
                continue
            other = self.board[v][u]

            if other is None:
                is_valid = True
            elif other.color == new.color:
                groups_to_remove.append(other)
                new = new + other
            elif self._liberties(other) == 1:
                is_valid = True
                self.groups_to_kill.append(other)

        if self._liberties(new):
            is_valid = True

        if is_valid:
            set_to_kill = set()
            set_to_remove = set()

            for i in self.groups_to_kill:
                set_to_kill.add(i)
            for i in groups_to_remove:
                set_to_remove.add(i)
            for i in set_to_kill:
                self._kill(i)
            for i in set_to_remove:
                self._remove(i)

            self._add(new)
            self.has_passed = False
            self.turn = not self.turn

        if len(new.stones) == 1 and len(self.groups_to_kill) == 1:
            for stone_block in self.groups_to_kill:
                self.blocked_field = next(iter(stone_block.stones))
        else:
            self.blocked_field = None

        return True
