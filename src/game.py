import pygame

GRAVITY = 0.25
class FlappyBird:
    def __init__(self) -> None:
        self.SCREEN_HEIGHT = 600
        self.SCREEN_WIDTH = 400

    def update(self):
        ''' Update the game state (bird position, pipe positions, etc.)'''
        pass

    def render(self):
        ''' Render the game '''
        pass

    def get_bird_y_position(self):
        ''' Return the y position of the bird '''
        return 0
    
    def get_bird_speed(self):
        ''' Return the y velocity of the bird '''
        return 0
    
    def get_closest_pipe_position(self):
        ''' Return the x and y position of the closest pipe (top left corner of bottom pipe)'''
        return 0, 0

    def click(self):
        ''' Simulate a click on the screen '''
        pass

    def get_score(self):
        ''' Return the current score '''
        return 0

    def is_game_over(self):
        ''' Return True if the game is over, False otherwise '''
        return False
    
    def reset(self):
        ''' Reset the game state '''
        pass

