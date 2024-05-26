#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" This part contains the View. All the images and sprites and the window are initialized
    in here and get constantly updated if there was a event. 
"""

import pyglet
from pyglet.sprite import Sprite
from graphics import Grid, Circle, Button

BLACK = True
WHITE = False

class Window(pyglet.window.Window):

    def __init__(self, n=9, controller=None): 
        super(Window, self).__init__(700, 700, fullscreen=False, caption='Project Go')

        def center_image(image):
            """Sets an image's anchor point to its center."""
            image.anchor_x = image.width / 2
            image.anchor_y = image.height / 2

        self.controller = controller
        self.data = {
            'size': n,
            'stones': [[None for _ in range(n)] for _ in range(n)],
            'territory': [[None for _ in range(n)] for _ in range(n)],
            'color': None,
            'game_over': False,
            'score': [0, 0]
        }

        self.image_background = pyglet.resource.image('images/Background.PNG')
        self.image_black_stone = pyglet.resource.image('images/BlackStone.PNG')
        self.image_white_stone = pyglet.resource.image('images/WhiteStone.PNG')

        center_image(self.image_black_stone)
        center_image(self.image_white_stone)

        self.init_display()

    def receive_data(self, data):
        """ Updates the data received from the controller updates the view.

            Arguments:
                data    : data received from controller (dict)
        """
        self.data.update(data)
        self.update()

    def init_display(self):
        """ Contains all the none changing images and labels to be drawn."""

        self.batch = pyglet.graphics.Batch()
        self.batch_stones = pyglet.graphics.Batch()

        pyglet.gl.glClearColor(255, 255, 255, 255)

        self.grp_back = pyglet.graphics.OrderedGroup(0)
        self.grp_fore = pyglet.graphics.OrderedGroup(1)
        self.grp_grid = pyglet.graphics.OrderedGroup(2)
        self.grp_label = pyglet.graphics.OrderedGroup(3)
        self.grp_stones = pyglet.graphics.OrderedGroup(4)
        self.grp_territory = pyglet.graphics.OrderedGroup(5)

        self.text_turn = pyglet.text.Label(x=500, y=650, text='Your color:', color=(0, 0, 0, 255),
                                           font_size=12, batch=self.batch, bold=True, group=self.grp_label)

        self.text_score = pyglet.text.Label(x=100, y=650, text='Score:', color=(0, 0, 0, 255),
                                           font_size=12, batch=self.batch, group=self.grp_label)

        self.score_black = pyglet.text.Label(x=350, y=650, text='0', bold=True, color=(0, 0, 0, 255),
                                           font_size=12, batch=self.batch, group=self.grp_label)

        self.score_white = pyglet.text.Label(x=260, y=650, text='0', bold=True, color=(0, 0, 0, 255),
                                           font_size=12, batch=self.batch, group=self.grp_label)

        self.info = pyglet.text.Label(x=310, y=50, text='Welcome!', color=(0, 0, 0, 255),
                                      font_size=12, batch=self.batch, bold=True, group=self.grp_label)

        self.graphical_obj = []
        self.background = Sprite(self.image_background, batch=self.batch, group=self.grp_back)
        self.grid = Grid(350, 350, n=self.data['size'], width=self.width - 200, height=self.height - 200,
                         batch=self.batch, group=self.grp_grid)

        self.graphical_obj.append(self.background)
        self.graphical_obj.append(self.grid)

        black_score_img = Sprite(self.image_black_stone, x=230, y=655, batch=self.batch, group=self.grp_label)
        white_score_img = Sprite(self.image_white_stone, x=320, y=655, batch=self.batch, group=self.grp_label)

        black_score_img.scale = 1./4
        white_score_img.scale = 1./4

        self.graphical_obj.append(black_score_img)
        self.graphical_obj.append(white_score_img)

        self.button_pass = Button(pos=(635, 30), text='Pass', batch=self.batch)
        self.button_newgame = Button(pos=(65, 30), text='New Game', batch=self.batch)

    def on_draw(self):
        """Draws the interface.

        This function should only draw the graphics without
        doing any computations.
        """
        self.clear()
        self.batch.draw()
        self.batch_stones.draw()

    def on_mouse_press(self, mousex, mousey, button, modifiers):
        """Function called on any mouse button press.

        Arguments:
            mousex    : x-coord of the click
            mousey    : y-coord of the click
            button    :
            modifiers :


        The buttons are saved as constants in pyglet.window.mouse,
        the modifiers under pyglet.window.key
        """
        self.update()

        if button == pyglet.window.mouse.LEFT:
            pos = self.grid.get_indices(mousex, mousey)

            if (mousex, mousey) in self.button_pass:
                self.controller.passing()
            elif (mousex, mousey) in self.button_newgame and self.data['game_over']:
                self.controller.new_game()
            elif pos is not None:
                if self.data['game_over']:
                    self.controller.mark_territory(pos)
                else:
                    self.controller.play(pos)

    def update(self, *args):
        """This function does all the calculations when the data gets updated.

        Arguments:
            *args   : all items that need to be updated

        Side note: Has to be called manually.
                   For other games that require permanent simulations you would add
                   the following line of code at the end of __init__():

                   pyglet.clock.schedule_interval(self.update, 1/30)
        """
        if self.data['size'] != self.grid.size:
            self.init_display()

        self.batch_stones = pyglet.graphics.Batch()
        self.stones_sprites = []
        self.score_black.text = str(self.data['score'][0])
        self.score_white.text = str(self.data['score'][1])

        for i in range(self.data['size']):
            for j in range(self.data['size']):

                color = self.data['stones'][j][i]
                x, y = self.grid.get_coords(i, j)

                if color == BLACK:
                    img_stone = self.image_black_stone
                    _s = Sprite(img_stone, x=x, y=y, batch=self.batch_stones, group=self.grp_stones)
                    _s.scale = 1. / 3
                    self.stones_sprites.append(_s)
                elif color == WHITE:
                    img_stone = self.image_white_stone
                    _s = Sprite(img_stone, x=x, y=y, batch=self.batch_stones, group=self.grp_stones)
                    _s.scale = 1. / 3
                    self.stones_sprites.append(_s)

        self.img_turn = {None: self.image_black_stone, True: self.image_black_stone, False: self.image_white_stone}
        self.img_turn_updated = Sprite(self.img_turn[self.data['color']], x=620, y=655,
                                       batch=self.batch, group=self.grp_label)
        self.img_turn_updated.scale = 1./4

        if self.data['game_over']:
            for i in range(self.data['size']):
                for j in range(self.data['size']):

                    color = self.data['territory'][j][i]
                    x, y = self.grid.get_coords(i, j)

                    if color == BLACK:
                        _s = Circle(x=x, y=y, color=(0, 0, 0, 255), r=5, batch=self.batch_stones,
                                    group=self.grp_territory)

                        self.stones_sprites.append(_s)
                    if color == WHITE:
                        _s = Circle(x=x, y=y, color=(255, 255, 255, 255), r=5, batch=self.batch_stones,
                                    group=self.grp_territory)

                        self.stones_sprites.append(_s)
