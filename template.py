#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains the example solution for finding marking
the territory and counting the score and a class representing
a stone group.

The game Model needs to inherit from Terr_Template if it does not
implement those methods itself.
"""

BLACK = True
WHITE = False

class Terr_Template:
    """This class does not work on its own but can be inherited from by
    the Model."""

    def find_territory(self):
        """Tries to automatically claim territory for the proper players.

        Current algorithm:
            It just claims empty areas that are completely surrounded
            by one color.
            Therefore it will not recognise prisoners or dead groups.

        Attributes updated by this function:
            self.score
            self.territory
        """
        area = []
        for y in range(self.size):
            for x in range(self.size):

                if (x, y) in area:
                    continue

                if self.board[y][x] is None:
                    _a, count = self._find_empty(x, y, area=area)
                    area += _a

                    if count[BLACK] == 0 and count[WHITE] > 0:
                        self._claim_empty(x, y, WHITE)
                    elif count[WHITE] == 0 and count[BLACK] > 0:
                        self._claim_empty(x, y, BLACK)

        self._compute_score()

    def mark_territory(self, x, y):
        """Function that can be evoked by user to claim territory for
        one player.
        For empty fields it will also mark all adjacent empty fields,
        for fields that contain a stone it will mark the entire stone
        group and all adjacent empty spaces.

        Arguments:
            x, y (int): coordinates of the field

        Attributes updated by this function:
            self.score
            self.territory
        """
        if not self.game_over:
            return

        if self.board[y][x] is None:
            col_dict = {None: BLACK, BLACK: WHITE, WHITE: None}
            color = col_dict[self.territory[y][x]]
            self._claim_empty(x, y, color)
        else:
            if self.territory[y][x] is None:
                color = not self.board[y][x].color
            else:
                color = None
            self._claim_group(x, y, color)

        self._compute_score()

    def _claim_empty(self, x, y, color, area=None):
        if area is None:
            area = []

        if self.board[y][x] is not None or (x, y) in area:
            return

        area.append((x, y))
        self.territory[y][x] = color

        for (u, v) in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
            if u < 0 or v < 0 or u >= self.size or v >= self.size:
                continue

            if (u, v) not in area and self.board[v][u] is None:
                self._claim_empty(u, v, color, area=area)

    def _claim_group(self, x, y, color, area=None):
        if area is None:
            area = []
        for u, v in self.board[y][x].stones:
            if (u, v) not in area:
                area.append((u, v))
                self.territory[v][u] = color
        for u, v in self.board[y][x].border:
            if self.board[v][u] is None and (u, v) not in area:
                self._claim_empty(u, v, color, area=area)

    def _compute_score(self):
        self.score = [0, 0]
        for j in range(self.size):
            for i in range(self.size):
                if self.territory[j][i] == BLACK:
                    self.score[BLACK] += 1
                    if self.board[j][i] is not None:
                        self.score[BLACK] += 1
                elif self.territory[j][i] == WHITE:
                    self.score[WHITE] += 1
                    if self.board[j][i] is not None:
                        self.score[WHITE] += 1

    def _find_empty(self, x, y, area=None, count=None):
        if area is None:
            area = []
        if count is None:
            count = [0, 0]

        if self.board[y][x] is not None or (x, y) in area:
            return area, count
        area.append((x, y))
        for (u, v) in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
            if u < 0 or v < 0 or u >= self.size or v >= self.size:
                continue
            if (u, v) not in area:
                if self.board[v][u] is None:
                    self._find_empty(u, v, area=area, count=count)
                else:
                    count[self.board[v][u].color] += 1
        return area, count


class Group:
    """Represents a group of connected stones on the board.

    Attributes:
        stones (set): list of all coordinates where the group has a stone
        border (set): list of all fields that are adjacent to the group
                      For a new group empty fields must be added manually
                      since the group does not know about the field size
        color (bool): color of the group

    Property:
        size (int): equal to len(self.stones), the number of stones in
                    the group.
    """

    def __init__(self, stones=None, color=None):
        """
        Initialise group
        """
        if stones is not None:
            self.stones = set(stones)
        else:
            self.stones = set()

        self.border = set()
        self.color = color

    def __add__(self, other):
        """To add two groups of the same color
        The new group contains all the stones of the previous groups and
        the border will be updated correctly.

        Raises:
            TypeError: The colours of the groups do not match
        """
        if self.color != other.color:
            raise ValueError('Only groups of same colour can be added!')
        grp = Group(stones=self.stones.union(other.stones))
        grp.color = self.color
        grp.border = self.border.union(other.border).difference(grp.stones)
        return grp

    @property
    def size(self):
        """Size of the group"""
        return len(self.stones)
