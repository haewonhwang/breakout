# model.py
# Jake Byman (jsb396) and Haewon Hwang (hh474)
# 12/9/2013
"""Model module for Breakout

This module contains the model classes for the Breakout game. Instances of
Model storee the paddle, ball, and bricks.  The model has methods for resolving
collisions between the various game objects.  A lot of your of your work
on this assignment will be in this class.

This module also has an additional class for the ball.  You may wish to add
more classes (such as a Brick class) to add new features to the game.  What
you add is up to you."""
from constants import *
from game2d import *
import random # To randomly generate the ball velocity

class Model(object):
    """An instance is a single game of breakout.  The model keeps track of the
    state of the game.  It tracks the location of the ball, paddle, and bricks.
    It determines whether the player has won or lost the game.  
    
    To support the game, it has the following instance attributes:
    
        _bricks:  the bricks still remaining 
                  [list of GRectangle, can be empty]
        _paddle:  the paddle to play with 
                  [GRectangle, never None]
        _ball:    the ball 
                  [Ball, or None if waiting for a serve]
        _isPlaying:checks to see that the player is playing the game
        _isWinning:checks to see if the player has won
    As you can see, all of these attributes are hidden.  You may find that you
    want to access an attribute in call Breakout. It is okay if you do, but
    you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter and/or
    setter for any attribute that you need to access in Breakout.  Only add
    the getters and setters that you need.
                  
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """


    def __init__(self):
        """Initializes the attributes and populates bricks for the game"""
        self._bricks = []
        self._isPlaying = True
        self._isWinning = False
        self._ball = None
        self._paddle = GRectangle(x = 0, y = PADDLE_OFFSET,
                                  width = PADDLE_WIDTH, height = PADDLE_HEIGHT,
                                  fillcolor = colormodel.BLACK)
        self.populateBricks()
        self.instantiateBall()


    def populateBricks(self):
        """Adds bricks to the _bricks array"""
        xPosition = BRICK_SEP_H/2
        yPosition = GAME_HEIGHT - BRICK_Y_OFFSET
        for g in range(BRICK_ROWS):
            for i in range(BRICKS_IN_ROW):
                if g > len(BRICK_COLORS)-1:
                    colorIndex = g % len(BRICK_COLORS)
                else:
                    colorIndex = g
                rect = GRectangle(x = xPosition, y= yPosition, width = BRICK_WIDTH,
                                  height = BRICK_HEIGHT, fillcolor = BRICK_COLORS[colorIndex])
                self._bricks.append(rect)
                xPosition += BRICK_SEP_H + BRICK_WIDTH
            yPosition -= BRICK_HEIGHT + BRICK_SEP_V
            xPosition = BRICK_SEP_H/2


    def getBricksList(self):
        """A getter method to access the _bricks list"""
        return self._bricks


    def changePaddlePosition(self, newX):
        """Changes the paddle's x position to newX"""
        self._paddle.x = newX


    def changePaddlePositionPoint(self, x, y):
        """Changes the paddle's x and y position's to x and y, respectively"""
        self._paddle.x = x
        self._paddle.y = y


    def getBrickAtIndex(self, index):
        """Returns: a brick at a given index"""
        return self._bricks[index]


    def instantiateBall(self):
        """Makes the ball with velocity (2, 3)"""
        self._ball = Ball(2, 3)


    def moveBall(self):
        """Moves the ball and checks for collisions"""
        if self._ball._vy > 0:        #While the ball is going up
            if self._ball.y + self._ball._vy <= GAME_HEIGHT:    #If the ball can keep going up without hitting the top
                self._ball.y += abs(self._ball._vy)
            else:        #If the ball is about to hit the top
                self._ball._vy *= -1
                self._ball.y -= abs(self._ball._vy)
        elif self._ball._vy < 0:    #While the ball is going down
            if self._ball.y - abs(self._ball._vy) >= 0:
                self._ball.y -= abs(self._ball._vy)
            else:
                self._isPlaying = False
                self._ball._vy = 0
                self._ball._vx = 0
        if self._ball._vx < 0:        #While the ball is going left
            if self._ball.x + self._ball._vx >= 0:    #If the ball can keep going left
                self._ball.x -= abs(self._ball._vx)
            else:                            #If the ball is about the hit the left side
                self._ball._vx *= -1
                self._ball.x += abs(self._ball._vx)
        elif self._ball._vx > 0:        #While the ball is going right
            if self._ball.x + self._ball._vx <= GAME_WIDTH:        #If the ball can keep going right
                self._ball.x += self._ball._vx
            else:                            #If the ball is about to hit the right side
                self._ball._vx *= -1
                self._ball.x -= abs(self._ball._vx)
                self._ball._right = False
                self._ball._left = True
        collidingObject = self._getCollidingObject()    #Get colliding object
        if collidingObject != None:    #If there is some collision
            if isinstance(collidingObject, GObject):     #If the collision is the paddle
                self._ball._vy *= -1
            else:    #If not, then it has to be a brick
                self._bricks.pop(collidingObject)    #Destroy the colliding brick
                self._ball._vy *= -1
                if len(self._bricks) == 0:
                    self._isPlaying = False
                    self._isWinning = True


    def _getCollidingObject(self):
        """Returns: a GObject that has collided with the ball, if it has done so"""
        if self._paddle.contains(self._ball.x, self._ball.y):
            return GObject() #change this!
        elif self._paddle.contains(self._ball.x + BALL_DIAMETER, self._ball.y):
            return GObject()
        elif self._paddle.contains(self._ball.x, self._ball.y + BALL_DIAMETER):
            return GObject()
        elif self._paddle.contains(self._ball.x + BALL_DIAMETER, self._ball.y + BALL_DIAMETER):
            return GObject()
        for brick in self._bricks:
            if brick.contains(self._ball.x, self._ball.y):
                return (self._bricks.index(brick))
                self._ball._vy = self._ball._vy * -1
            elif brick.contains(self._ball.x + BALL_DIAMETER, self._ball.y):
                return (self._bricks.index(brick))
                self._ball._vy = self._ball._vy * -1
            elif brick.contains(self._ball.x, self._ball.y + BALL_DIAMETER):
                return (self._bricks.index(brick))
                self._ball._vy = self._ball._vy * -1
            elif brick.contains(self._ball.x + BALL_DIAMETER, self._ball.y + BALL_DIAMETER):
                return (self._bricks.index(brick))
                self._ball._vy = self._ball._vy * -1
        return None


class Ball(GEllipse):
    """Instance is a game ball.
    
    We extends GEllipse because a ball in order to add attributes for a 
    velocity. This subclass adds these two attributes.
    
    INSTANCE ATTRIBUTES:
        _vx: Velocity in x direction [int or float]
        _vy: Velocity in y direction [int or float]
    
    The class Model will need to access the attributes. You will
    need getters and setters for these attributes.
    
    In addition to the getters and setter, you should add two
    methods to this class: an initializer to set the starting velocity 
    and a method to "move" the ball. The move method should adjust the 
    ball position according to the velocity.
    
    NOTE: The ball does not have to be a GEllipse. It could be an instance
    of GImage (why?). This change is allowed, but you must modify the class
    header up above.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """


    def __init__(self, vx, vy):
        """Initializes attributes for the Ball and creates one"""
        GEllipse.__init__(self, x = GAME_WIDTH/2, y = GAME_HEIGHT/2, width = BALL_DIAMETER, height = BALL_DIAMETER, fillcolor = colormodel.BLACK)
        self._vx = random.uniform(1.0,5.0)
        self._vx = self._vx * random.choice([-1,1])
        self._vy = -5