# controller.py
# Jake Byman (jsb396) and Haewon Hwang (hh474)
# 12/9/2013
"""Primary module for Breakout application

This module contains the controller class for the Breakout application.
There should not be any need for additional classes in this module.
If you need more classes, 99% of the time they belong in the model 
module. If you are ensure about where a new class should go, post a
question on Piazza."""
from constants import *
from game2d import *
from model import *


class Breakout(Game):
    """Instance is a Breakout Application

    This class extends Game and implements the various methods necessary 
    for running the game.

        Method init starts up the game.

        Method update updates the model objects (e.g. move ball, remove bricks)

        Method draw displays all of the models on the screen

    Because of some of the weird ways that Kivy works, you do not need to make
    an initializer __init__ for this class.  Any initialization should be done
    in the init method instead.

    Most of the work handling the game is actually provided in the class Model.
    Model should have a method called moveBall() that moves the ball and processes
    all of the game physics. This class should simply call that method in update().

    The primary purpose of this class is managing the game state: when is the 
    game started, paused, completed, etc. It keeps track of that in an attribute
    called _state.

    Instance Attributes:
        view:   the game view, used in drawing 
                [Immutable instance of GView, it is inherited from Game]
        _state: the current state of the game
                [one of STATE_INACTIVE, STATE_COUNTDOWN, STATE_PAUSED, 
                 STATE_ACTIVE, or STATE_COMPLETE]
        _model: the game model, which stored the paddle, ball, and bricks
                [GModel, or None if there is no game currently active
                 It is only None if _state is STATE_INACTIVE]
        _timer: the timer for STATE_COUNTDOWN
        _lives: the number of lives that the player has remaining
        _hasAlreadyDrawnBricks: boolean that states if bricks have been drawn
        _hasAlreadyMadeModel: boolean that states if model has been made
        _message: current message displayed on screen

    You may have more attributes if you wish (you might need an attribute to store
    any text messages you display on the screen). If you add new attributes, they
    need to be documented here.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """


    def init(self):
        """Initialize the game state.

        This method is distinct from the built-in initializer __init__.
        This method is called once the game is running. You should use
        it to initialize any game specific attributes.

        This method should initialize any state attributes as necessary 
        to statisfy invariants. When done, set the _state to STATE_INACTIVE
        and create a message saying that the user should press to play a game."""

        self._model = None
        self._timer = TIMER_AMOUNT
        self._lives = 3
        self._hasAlreadyDrawnBricks = False
        self._hasAlreadyMadeModel = False
        self._state = STATE_INACTIVE

        self._message = GLabel(text = 'Press to Play!')
        self._message.x = GAME_WIDTH/2 - 50
        self._message.y = GAME_HEIGHT/2


    def update(self,dt):
        """Animate a single frame in the game.

        It is the method that does most of the work. Of course, it should
        rely on helper methods in order to keep the method short and easy
        to read.  Some of the helper methods belong in this class, and
        others belong in class Model.

        The first thing this method should do is to check the state of the
        game. We recommend that you have a helper method for every single
        state: STATE_INACTIVE, STATE_COUNTDOWN, STATE_PAUSED, STATE_ACTIVE.
        The game does different things in each state.

        In STATE_INACTIVE, the method checks to see if the player clicks
        the mouse. If so, it starts the game and switches to STATE_COUNTDOWN.

        STATE_PAUSED is similar to STATE_INACTIVE. However, instead of 
        restarting the game, it simply switches to STATE_COUNTDOWN.

        In STATE_COUNTDOWN, the game counts down until the ball is served.
        The player is allowed to move the paddle, but there is no ball.
        This state should delay at least one second.

        In STATE_ACTIVE, the game plays normally.  The player can move the
        paddle and the ball moves on its own about the board.  Both of these
        should be handled by methods inside of class Model (not in the class).
        Model should have methods named movePaddle and moveBall.

        While in STATE_ACTIVE, if the ball goes off the screen and there
        are tries left, it switches to STATE_PAUSED.  If the ball is lost 
        with no tries left, or there are no bricks left on the screen, the
        game is over and it switches to STATE_INACTIVE.

        While in STATE_COMPLETE, this method does nothing.

        You are allowed to add more states if you wish. Should you do so,
        you should describe them here.

        Precondition: dt is the time since last update (a float).  This
        parameter can be safely ignored. It is only relevant for debugging
        if your game is running really slowly."""


        if self._state == STATE_INACTIVE:
            self.inactiveStateHelper()
        elif self._state == STATE_COUNTDOWN:
            self.counterStateHelper()
        elif self._state == STATE_ACTIVE:
            self.activeStateHelper()
        elif self._state == STATE_COMPLETE:
            self.completeStateHelper()
        elif self._state == STATE_PAUSED:
            self.pausedStateHelper()


    def inactiveStateHelper(self):
        """Helper method for STATE_INACTIVE"""
        if type(self.view.touch) == GPoint:
            self._state = STATE_COUNTDOWN
            self._message = None


    def counterStateHelper(self):
        """Helper method for STATE_COUNTDOWN"""
        if self._timer <= 180 and self._timer > 0:
            a = self._timer/60 + 1
            self._timer -= 1
            self._message = GLabel(text = str(a), x = GAME_WIDTH/2, y = GAME_HEIGHT/2, font_size = 20)
        elif self._timer == 0:
            self._message = None
            self._state = STATE_ACTIVE


    def activeStateHelper(self):
        """Helper method for STATE_ACTIVE"""
        self._message = GLabel(text = "Lives: " + str(self._lives), x = 0, y = GAME_HEIGHT-18)
        if self._hasAlreadyMadeModel == False:
            self._model = Model()
            self._hasAlreadyMadeModel = True
        if type(self.view.touch) == GPoint:
            if self.view.touch.x + PADDLE_WIDTH <= GAME_WIDTH and self.view.touch.x >= 0:
                self.setPaddlePosition(self.view.touch.x)
            elif self.view.touch.x + PADDLE_WIDTH >= GAME_WIDTH:
                self.setPaddlePosition(self.view.touch.x - PADDLE_WIDTH)
        if self._model._isPlaying == False:
            if self._model._isWinning == True:
                self._state = STATE_COMPLETE
                self._message = GLabel(text = "You win! Yay!", x = GAME_WIDTH/2 - 50,
                                       y = GAME_HEIGHT/2, font_size = 20)
            else:
                self._state= STATE_COMPLETE
                self.decrementLives()
                if self._lives == 0:
                    self._message = GLabel(text = "GAME OVER", x = GAME_WIDTH/2 - 50,
                                           y = GAME_HEIGHT/2)
                    self._state = STATE_COMPLETE
                else:
                    self._state = STATE_PAUSED


    def completeStateHelper(self):
        """Helper method for STATE_COMPLETE"""
        self.clearScreen()


    def pausedStateHelper(self):
        """Helper method for STATE_HELPER"""
        self._message = GLabel(text ="Click screen to try again", x = GAME_WIDTH/2 - 75,
                               y = GAME_HEIGHT/2)
        self._timer = 180
        self._hasAlreadyMadeModel = False
        if type(self.view.touch) == GPoint:
            self._state = STATE_COUNTDOWN


    def clearScreen(self):
        """Clears the paddle and bricks from the screen"""
        self._model._paddle = None
        self._model._bricks = None


    def drawBricksToScreen(self):
        """Draws brick to screen for each brick in the _bricks array"""
        for b in self._model._bricks:
            b.draw(self.view)


    def drawPaddleToScreen(self):
        """Draws the paddle to the screen"""
        self._model._paddle.draw(self.view)


    def drawBallToScreen(self):
        """Draws the ball to the screen"""
        self._model._ball.draw(self.view)


    def setPaddlePosition(self, x):
        """Sets the paddle's x position"""
        self._model.changePaddlePosition(x)


    def decrementLives(self):
        """Decrements the player's lives by 1"""
        self._lives -= 1


    def draw(self):
        """Draws the game objects to the view.

        Every single thing you want to draw in this game is a GObject. 
        To draw a GObject g, simply use the method g.draw(view).  It is 
        that easy!

        Many of the GObjects (such as the paddle, ball, and bricks) are
        attributes in Model. In order to draw them, you either need to
        add getters for these attributes or you need to add a draw method
        to class Model.  Which one you do is up to you."""

        if self._message != None:
            self._message.draw(self.view)
        if self._model != None and self._state != STATE_COMPLETE:
               self.drawBricksToScreen()
               self.drawPaddleToScreen()
               self.drawBallToScreen()
               self._hasAlreadyDrawnBricks = True
               self._model.moveBall()