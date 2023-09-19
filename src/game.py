import pygame
import random
import os
import numpy as np

os.chdir(os.path.dirname(os.path.realpath(__file__)))


class FlappyBird:
    def __init__(self) -> None:
        self.MAX_FRAMERATE = 1500 # note that the normal speed is 15 FPS

        # VARIABLES
        self.SCREEN_WIDTH = 400
        self.SCREEN_HEIGHT = 600
        self.SPEED = 20
        self.GRAVITY = 2.5
        self.GAME_SPEED = 15

        self.GROUND_WIDTH = 2 * self.SCREEN_WIDTH
        self.GROUND_HEIGHT= 100

        self.PIPE_WIDTH = 80
        self.PIPE_HEIGHT = 500

        self.PIPE_GAP = 150

        self.BIRD_Y_RANGE = [0, self.SCREEN_HEIGHT]
        self.BIRD_V_RANGE = [-10, 10]
        self.PIPE_X_RANGE = [0, self.SCREEN_WIDTH]
        self.PIPE_Y_RANGE = [0, self.SCREEN_HEIGHT]

        self.score = 0

        self.bird_images = None
        self.pipe_image = None
        self.ground_image = None
        self.background_image = None


        self.ground_group = pygame.sprite.Group()
        self.pipe_group = pygame.sprite.Group()
        self.bird_group = pygame.sprite.Group()

        self.setup()

        self.bird = Bird(self)
        self.bird_group.add(self.bird)

        self.jumping = False


        self.clock = pygame.time.Clock()

        # set up font for FPS, score and other text
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 24)
        self.large_font = pygame.font.SysFont(None, 48)

        self.game_over = False

        
        
    def setup(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption('Flappy Bird')
        # Cache the loaded images
        self.bird_images = [pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha(),
                    pygame.image.load('assets/sprites/bluebird-midflap.png').convert_alpha(),
                    pygame.image.load('assets/sprites/bluebird-downflap.png').convert_alpha()]

        self.pipe_image = pygame.image.load('assets/sprites/pipe-green.png').convert_alpha()
        self.pipe_image = pygame.transform.scale(self.pipe_image, (self.PIPE_WIDTH, self.PIPE_HEIGHT))

        self.ground_image = pygame.image.load('assets/sprites/base.png').convert_alpha()
        self.ground_image = pygame.transform.scale(self.ground_image, (self.GROUND_WIDTH, self.GROUND_HEIGHT))

        self.background_image = pygame.image.load('assets/sprites/background-day.png')
        self.background_image = pygame.transform.scale(self.background_image, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.create_starting_objects()

    def create_starting_objects(self):
        # Create the ground and pipes for the start of the game
        self.ground_group.empty()
        for i in range (2):
            self.ground = Ground(self, self.GROUND_WIDTH * i)
            self.ground_group.add(self.ground)

        self.pipe_group.empty()
        for i in range (2):
            self.pipes = self.get_random_pipes(self.SCREEN_WIDTH * i + 800)
            self.pipe_group.add(self.pipes[0])
            self.pipe_group.add(self.pipes[1])


    def is_off_screen(self, sprite):
        return sprite.rect[0] < -(sprite.rect[2])

    def get_random_pipes(self, xpos):
        size = random.randint(100, 300)
        pipe = Pipe(self, False, xpos, size)
        pipe_inverted = Pipe(self, True, xpos, self.SCREEN_HEIGHT - size - self.PIPE_GAP)
        return pipe, pipe_inverted
        

    def update(self):
        ''' Update the game state (bird position, pipe positions, etc.)'''
        # bird.bump() # This makes the bird jump

        if self.game_over:
            self.reset()
            self.game_over = False
            return

        self.jumping = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    self.bird.bump()
                    self.jumping = True



        
        # Optimized collision detection
        for pipe in self.pipe_group:
            if pipe.rect[0] + self.PIPE_WIDTH > 0:  # Only if pipe is on screen
                if pygame.sprite.collide_mask(self.bird, pipe):
                    self.game_over = True


        self.bird_group.update()
        self.ground_group.update()
        self.pipe_group.update()

        if self.is_off_screen(self.ground_group.sprites()[0]):
            self.ground_group.remove(self.ground_group.sprites()[0])

            new_ground = Ground(self, self.GROUND_WIDTH - 20)
            self.ground_group.add(new_ground)

        if self.is_off_screen(self.pipe_group.sprites()[0]):
            self.pipe_group.remove(self.pipe_group.sprites()[0])
            self.pipe_group.remove(self.pipe_group.sprites()[0])

            pipes = self.get_random_pipes(self.SCREEN_WIDTH * 2)

            self.pipe_group.add(pipes[0])
            self.pipe_group.add(pipes[1])

            self.score += 1
        

        # Optimized off-screen pipe check and removal
        to_remove = []
        for pipe in self.pipe_group:
            if pipe.rect[0] + self.PIPE_WIDTH < 0:
                to_remove.append(pipe)

        for item in to_remove:
            self.pipe_group.remove(item)

        # Optimized collision detection
        for pipe in self.pipe_group:
            if pipe.rect[0] + self.PIPE_WIDTH > 0:  # Only if pipe is on screen
                if pygame.sprite.collide_mask(self.bird, pipe):
                    # pygame.mixer.music.load(hit)
                    # pygame.mixer.music.play()
                    self.game_over = True
        
        if pygame.sprite.groupcollide(self.bird_group, self.ground_group, False, False, pygame.sprite.collide_mask):
            self.game_over = True

    def render(self): # This should be up to date as of our first meeting
        ''' Render the game (unfinished)'''
        self.clock.tick(self.MAX_FRAMERATE)
        
        # Clear screen (Draw empty background)
        self.screen.blit(self.background_image, (0, 0))

        self.bird_group.draw(self.screen)
        self.pipe_group.draw(self.screen)
        self.ground_group.draw(self.screen)

        # FPS Counter
        self.fps = int(self.clock.get_fps())
        self.fps_text = self.font.render("FPS: " + str(self.fps), True, (255, 255, 255))
        self.screen.blit(self.fps_text, (2, 2))

        # Current score Counter
        self.current_score = int(self.score)
        self.current_score_text = self.large_font.render(str(self.current_score), True, (255, 255, 255))
        self.screen.blit(self.current_score_text, (self.SCREEN_WIDTH - self.SCREEN_WIDTH / 2, 64))


        pygame.display.update()

    def get_bird_y_position(self):
        ''' Return the y position of the bird (finished)'''
        return self.bird.rect[1]
    
    def get_bird_speed(self):
        ''' Return the y velocity of the bird (finished)'''
        return self.bird.speed
    
    def get_closest_pipe_position(self):
        ''' Return the x and y position of the closest pipe (top left corner of bottom pipe) (unfinished)'''
        closest_pipe = self.pipe_group.sprites()[0]  # Update this to switch to the next pipe sooner
        return closest_pipe.rect[0], closest_pipe.rect[1]

    def jump(self):
        ''' Simulate a click on the screen (unfinished)'''
        self.bird.bump()

    def get_score(self):
        ''' Return the current score (finished)'''
        return self.score

    def is_game_over(self):
        ''' Return True if the game is over, False otherwise (unfinished)'''
        return self.game_over
    
    def reset(self):
        ''' Reset the game state (finished)'''
        self.bird.reset()
        self.create_starting_objects()
        self.score = 0
    
    def normalize(self, x, range):
        return (x - range[0]) / (range[1] - range[0])
    
    def get_observation(self):
        pipe_position = self.get_closest_pipe_position()
        return np.array([
            self.normalize(self.get_bird_y_position(), self.BIRD_Y_RANGE),
            self.normalize(self.get_bird_speed(), self.BIRD_V_RANGE),
            self.normalize(pipe_position[0], self.PIPE_X_RANGE),
            self.normalize(pipe_position[1], self.PIPE_Y_RANGE)
        ])


class Bird(pygame.sprite.Sprite):

    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game

        self.images = self.game.bird_images

        self.speed = -self.game.SPEED

        self.current_image = 0
        self.image = pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = self.game.SCREEN_WIDTH / 6
        
        self.reset()

    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]
        self.speed += self.game.GRAVITY

        #UPDATE HEIGHT
        self.rect[1] += self.speed

        if (self.rect[1] < 0):
            self.rect[1] = 0
            self.speed = 0


    def bump(self):
        self.speed = -self.game.SPEED

    def begin(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]
        
    def reset(self):
        self.rect[1] = self.game.SCREEN_HEIGHT / 2
        self.speed = -self.game.SPEED





class Pipe(pygame.sprite.Sprite):

    def __init__(self, game, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)
        self.game = game

        self.image = self.game.pipe_image
        self.image = pygame.transform.scale(self.image, (self.game.PIPE_WIDTH, self.game.PIPE_HEIGHT))


        self.rect = self.image.get_rect()
        self.rect[0] = xpos

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ysize)
        else:
            self.rect[1] = self.game.SCREEN_HEIGHT - ysize


        self.mask = pygame.mask.from_surface(self.image)


    def update(self):
        self.rect[0] -= self.game.GAME_SPEED

        

class Ground(pygame.sprite.Sprite):
    
    def __init__(self, game, xpos):
        pygame.sprite.Sprite.__init__(self)
        self.game = game

        self.image = self.game.ground_image
        self.image = pygame.transform.scale(self.image, (self.game.GROUND_WIDTH, self.game.GROUND_HEIGHT))

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = self.game.SCREEN_HEIGHT - self.game.GROUND_HEIGHT
    def update(self):
        self.rect[0] -= self.game.GAME_SPEED



if __name__ == '__main__':
    game = FlappyBird()
    # game.setup()
    game.reset()

    while True:
        game.update()
        game.render()