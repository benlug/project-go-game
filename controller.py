#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" This document contains the game's controller. It receives and passes data on between the view and the model.
"""

from client import Window
from game_model import Model
import pyglet

BLACK = True
WHITE = False

class Controller:
    '''In this class the controler of the Go game is defined.'''

    def __init__(self):
        """This method creates an object of the class controler.

               creates Variables:
                   self.window: calls the class Window with the attributes n and controller.

                        Attributes:
                            n: defines the size of the board game.
                            controller: gives attribute self (>c) to the window.

                    self.model: calls the class Model.

               Variables updated by this method:
                   self.update_window()
               """
        self.window = Window(n=9, controller=self)
        self.model = Model()
        self.update_window()

    def new_game(self):
        """This method creates a new game.

               creates Variables:
                    self.model: calls the class Model.
                    self.window.info.text: prints out a message to the user.

               calls methods:
                    self.update_window(): it calls the method update_window out of the controller class.
               """
        self.model = Model()
        self.update_window()
        self.window.info.text = "It's black's turn"

    def update_window(self):
        """This method updates the user window.

               creates Variables:
                   self.data: calls the get_data method out of the model and returns a data dictionary.

               Variables updated by this method:
                   self.window.receive_data(self.data): calls the receive_data method out of the window.

                        Attributes:
                            self.data: a dictionary with data out of the model.
               """
        self.data = self.model.get_data()
        self.window.receive_data(self.data)

    def play(self, pos):
        """This method runs the place_stone method out of the model,
                updates the window and prints out a corresponding message to the user .


               Arguments:
                   pos: a 2-tuple of integers

               creates objects:
                   posx: the first position of the tuple pos
                   posy: the second position of the tuple pos

               calls methods:
                   self.model.place_stone(posx,posy): calls the method passing() out of the model,
                        which checks the validity of a stone to be placed.

                       Arguments:
                           posx: the first position of the tuple pos
                           posy: the second position of the tuple pos

                   self.update_window(): it calls the method update_window out of the controller class.

               calls Variables:
                   self.data: looks up a key-value pair out of the data dictionary.

               creates Variables:
                    self.window.info.text: prints out a corresponding message to the user.
               """
        posx, posy = pos

        if self.model.place_stone(posx, posy):
            self.update_window()
            if self.data["color"] == BLACK:
                self.window.info.text = "It's black's turn"
            else:
                self.window.info.text = "It's white's turn"
        else:
            self.window.info.text = "Invalid move!"

    def passing(self):
        """This method runs the place_stone method out of the model,
        updates the window and prints out a corresponding message to the user.


               calls methods:
                   self.model.passing(): calls the method passing() out of the model, which checks if the player has passed.
                   self.update_window(): it calls the method update_window out of the controller class.

               calls Variables:
                   self.data: looks up a key-value pair out of the data dictionary.

               creates Variables:
                    self.window.info.text: prints out a corresponding message to the user.
               """
        if self.model.passing():
            self.update_window()
            if not self.data["game_over"]:
                if self.data["color"] == BLACK:
                    self.window.info.text = "It's black's turn"
                else:
                    self.window.info.text = "It's white's turn"
            else:
                self.window.info.text = "Game over!"
        self.update_window()

    def mark_territory(self, pos):
        """This method calls the mark_territory function of the model.


               Arguments:
                   pos: a 2-tuple of integers

               creates objects:
                   posx: the first position of the tuple pos
                   posy: the second position of the tuple pos

               calls methods:
                   self.model.mark_territory(posx,posy): calls the method mark_territory() out of the model,
                        which allows the user to claim territory for one player.

                       Arguments:
                           posx: the first position of the tuple pos
                           posy: the second position of the tuple pos

                    self.update_window(): it calls the method update_window out of the controller class.
               """
        posx, posy = pos

        self.model.mark_territory(posx, posy)
        self.update_window()


if __name__ == '__main__':
    c = Controller()
    pyglet.app.run()
