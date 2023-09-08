import gymnasium as gym
import numpy as np
from gymnasium import spaces
from game import FlappyBird

class FlappyBirdEnv(gym.Env):

    # I don't think this actually does anything:
    metadata = {"render_modes": ["human"], "render_fps": 30}

    def __init__(self):
        super().__init__()

        self.game = FlappyBird()
        
        self.N_INPUTS = 4
        # 0: bird y position
        # 1: bird y velocity
        # 2: x distance to next pipe
        # 3: height of next pipe

        # Ranges used for normalization
        self.BIRD_Y_RANGE = [0, self.game.SCREEN_HEIGHT]
        self.BIRD_V_RANGE = [-10, 10]
        self.PIPE_X_RANGE = [0, self.game.SCREEN_WIDTH]
        self.PIPE_Y_RANGE = [0, self.game.SCREEN_HEIGHT]
        
        self.action_space = spaces.Discrete(2) # Number of actions the agent can take
        
        # Expects normalized inputs!
        self.observation_space = spaces.Box(low=0, high=1,
                                            shape=(self.N_INPUTS,), dtype=np.float32)
        
        self.last_action = None
    
    def normalize(self, x, range):
        return (x - range[0]) / (range[1] - range[0])
    
    def create_observation(self):
        pipe_position = self.game.get_closest_pipe_position()
        return np.array([
            self.normalize(self.game.get_bird_y_position(), self.BIRD_Y_RANGE),
            self.normalize(self.game.get_bird_speed(), self.BIRD_V_RANGE),
            self.normalize(pipe_position[0], self.PIPE_X_RANGE),
            self.normalize(pipe_position[1], self.PIPE_Y_RANGE)
        ])

    def calculate_reward(self):
        return self.game.get_score()

    def step(self, action):

        print(action) # DEBUG

        # Send action to game:
        if action == 1:
            self.game.click()

        # Update game state:
        self.game.update()

        observation = self.create_observation()
        reward = self.calculate_reward()
        terminated = self.game.is_game_over()

        self.render() # Render the game

        self.last_action = action
        return observation, reward, terminated, False, {}

    def reset(self, seed=None, options=None):
        ''' Reset the game state when the agent dies '''
        self.game.reset()
        # self.game = FlappyBird()
        observation = self.create_observation()
        return observation, {}

    def render(self):
        self.game.render()

    def close(self):
        pass
        # self.game.close()