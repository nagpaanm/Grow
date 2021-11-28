"""
First gaming project. 10/23/16

Anmol Nagpal
"""

import pygame
import random

pygame.init()

# screen
screen_length = 480
screen_height = 400
edge = 10
screen = pygame.display.set_mode((screen_length, screen_height))
pygame.display.set_caption('Grow')


def colors(col):  # colors
    """ Return the color in pygame.

    @type col: str
    @rtype: object
    """
    return pygame.color.Color(col)

# set colors
red = colors('red')
yellow = colors('yellow')
black = colors('black')
white = colors('white')
blue = colors('blue')
green = colors('green')
orange = colors('orange')
pink = colors('pink')
purple = colors('purple')


class Player:
    """ Create a player class. This is the main user.

    === Attributes ===
    @type size: int
        Length and width of Player.
    @type speed: int
    @type x: int
        X coordinate of Player.
    @type y: int
        Y coordinate of Player.
    """
    def __init__(self, size, speed, x=screen_length/2, y=screen_height/2):
        """ Initalize a new player.

        @type self: Player
        @type size: int
        @type speed: int
        @type x: int
        @type y: int
        @rtype: None
        """
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed

    def draw(self):
        """ Draw Player onto pygame screen.

        @type self: Player
        @rtype: Object
        """
        pygame.draw.rect(screen, black, (self.x, self.y, self.size,
                                         self.size), 0)

    def move(self, board):
        """ Move player according to board.

        @type self: Player
        @type board: Pygame Keyboard
        @rtype: Object
        """
        if board[pygame.K_RIGHT]:
            if not self.x > (screen_length - edge):
                self.x += self.speed
        elif board[pygame.K_LEFT]:
            if not (self.x + self.size) < edge:
                self.x -= self.speed
        elif board[pygame.K_UP]:
            if not (self.y + self.size) < edge:
                self.y -= self.speed
        elif board[pygame.K_DOWN]:
            if not self.y > (screen_height - edge):
                self.y += self.speed


class Apple:
    """ Create an Apple object. This is what Player eats.

    === Attributes ===
    @type x: int
        The x-coordinate of Apple.
    @type y: int
        The y-coordinate of Apple.
    @type size: int
        The length and width of Apple.
    """
    def __init__(self, size):
        """ Initalize a new Apple.

        @type self: Apple
        @type size: int
        @rtype: None
        """
        self.size = size
        self.x = random.randint(1, screen_length - self.size)
        self.y = random.randint(1, screen_height - self.size)

    def draw(self):
        """ Draw Apple onto pygame screen.

        @type self: Apple
        @rtype: Object
        """
        pygame.draw.rect(screen, red, (self.x, self.y, self.size, self.size), 0)

    def relocate(self):
        """ Move the Apple to another random position.

        @type self: Apple
        @rtype: object
        """
        self.x = random.randint(1, screen_length - self.size)
        self.y = random.randint(1, screen_height - self.size)


class Fling:
    """ Create shooting Fling objects. If Player is to collide with one of these
    objects then the game is over.

    === Attributes ===
    @type x: int
        X-coordinate of Fling. Randomly chosen.
    @type y: int
        Y-coordinate of Fling. Initally 0.
    @type speed: tuple(int, int)
        Speed of Fling (a given range).
    @type size: int
        Length and width of Fling.
    @type color: object
        Color of Fling.
    """
    def __init__(self, speed, size, color):
        """ Initialize a new Fling object.

        @type self: Fling
        @type speed: tuple[int, int]
        @type size: int
        @type color: object
        @rtype: None
        """
        self.x = random.randint(0 + edge, screen_length - edge)
        self.y = 0 - size
        self.speed_range = speed
        self.speed = random.randint(self.speed_range[0],
                                    self.speed_range[1])
        self.color = color
        self.size = size

    def create(self):
        """ Create Fling onto pygame screen that moves vertically.

        @type self: Fling
        @rtype: object
        """
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size,
                                              self.size), 0)
        self.y += self.speed

    def regenerate(self):
        """ Create a new Fling once the Fling is off the pygame screen.

        @type self: Fling
        @rtype: object
        """
        if self.y > (screen_height + self.size):
            self.x = random.randint(0 + edge, screen_length - edge)
            self.y = 0 - self.size
            # if m.counter >= 25:
            #    self.speed_range = (self.speed_range[0] + 1,
            #                        self.speed_range[1] + 1)
            self.speed = random.randint(self.speed_range[0],
                                        self.speed_range[1])
            self.create()


class Zapper:
    """ Create a Zapper object.

    Note: Zapper moves horizontally.

    === Attributes ===
    @type x: int
        X-coordinate of Fling. Randomly chosen.
    @type y: int
        Y-coordinate of Fling. Initally 0.
    @type speed: tuple(int, int)
        Speed of Fling (a given range).
    @type size: int
        Length and width of Fling.
    @type color: object
        Color of Fling.
    """
    def __init__(self, speed, size, color):
        """ Initialize a new Fling object.

        @type self: Fling
        @type speed: tuple[int, int]
        @type size: int
        @type color: object
        @rtype: None
        """
        self.x = 0 - size
        self.y = random.randint(0 + edge, screen_height - edge)
        self.speed_range = speed
        self.speed = random.randint(self.speed_range[0],
                                    self.speed_range[1])
        self.color = color
        self.size = size

    def create(self):
        """ Create a Zapper object onto the pygame screen.

        @type self: Zapper
        @rtype: object
        """
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size,
                                              self.size), 0)
        self.x += self.speed
        if self.x > (screen_length + self.size):
            self.y = random.randint(0 + edge, screen_height - edge)
            self.x = 0 - self.size
            self.speed = random.randint(self.speed_range[0],
                                        self.speed_range[1])
            self.create()


def collision(ob1, ob2):
    """ Detect whether there is a collision between 2 objects <object1> and
    <object2> and return True if there is.

    @rtype: Bool
    """
    x_axis = (ob1.x > ob2.x and (ob1.x < (ob2.x + ob2.size))) or \
             ((ob1.x + ob1.size) < (ob2.x + ob2.size) and
              ((ob1.x + ob1.size) > ob2.x))
    y_axis = ((ob1.y + ob1.size) < (ob2.y + ob2.size)) and \
             (ob1.y + ob1.size) > ob2.y or \
             (ob1.y < (ob2.y + ob2.size) and (ob1.y > ob2.y))

    return x_axis and y_axis


class Message:
    """ On screen messages.
    === Attributes ===
    @type counter: int
        Keeps track of the score.
    """
    def __init__(self):
        """ Initialize Score.

        @type self: Score
        @rtype: None
        """
        self.counter = 0

    def message_display(self, size, color, msg):
        """ Put and update the score on the screen.

        @type self: Score
        @type size: int
        @type color: object
        @type msg: str
        @rtype: object
        """
        msg = msg
        size = size
        color = color
        font = pygame.font.SysFont(None, size)  # set the font size
        screen_text = font.render(msg + str(self.counter), True, color)
        # place the message on the screen
        screen.blit(screen_text, [(screen_length - 3.5*size),
                                  screen_height - size])

    def end_game(self, size, color, msg):
        """ Display the message once the game has ended.

        @type self: Score
        @type size: int
        @type color: object
        @type msg: str
        @rtype: object
        """
        msg = msg
        size = size
        color = color
        font = pygame.font.SysFont(None, size)  # set the font size
        screen_text = font.render(msg + str(self.counter), True, color)
        # place the message on the screen
        screen.blit(screen_text, [screen_length/4, screen_height/2])


def play():
    """ Play the game. """

    # set up
    player = Player(25, 4)
    apple = Apple(25)
    fling = Fling((2, 5), 20, purple)
    zapper = Zapper((2, 5), 20, green)
    m = Message()
    end_game = False
    orig_player_speed = player.speed

    # mainloop
    while True:
        for event in pygame.event.get():  # gets any event that happens
            if event.type == pygame.QUIT:
                pygame.quit()
            # screen.fill(white)
        screen.fill(white)
        keyboard = pygame.key.get_pressed()

        if not end_game:
            m.message_display(25, blue, 'Score: ')
            player.draw()
            apple.draw()
            fling.create()
            fling.regenerate()
            player.move(keyboard)

            if m.counter >= 10:
                zapper.create()
            if m.counter == 20 and player.speed == orig_player_speed:
                player.speed += 1

            if collision(player, apple) or collision(apple, player):
                apple.relocate()
                player.size += 2
                m.counter += 1
            if collision(apple, fling) or collision(fling, apple):
                apple.relocate()
            if collision(player, fling) or collision(fling, player):
                end_game = True
            if collision(player, zapper) or collision(zapper, player):
                end_game = True
            if collision(apple, zapper) or collision(zapper, apple):
                apple.relocate()

            pygame.time.delay(15)
            pygame.display.update()

        else:
            m.end_game(50, red, 'Final Score: ')
            pygame.display.update()
            if keyboard[pygame.K_SPACE]:
                play()

if __name__ == '__main__':
    play()
