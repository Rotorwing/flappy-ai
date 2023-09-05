import gymnasium as gym
import numpy as np
from gymnasium import spaces

class FlappyBirdEnv(gym.Env):

    metadata = {"render_modes": ["human"], "render_fps": 30}


    def __init__(self):
        super().__init__()

        game = FlappyBird()
        
        N_INPUTS = 4
        # 0: bird y position
        # 1: bird y velocity
        # 2: x distance to next pipe
        # 3: height of next pipe

        BIRD_Y_RANGE = [0, 800]
        BIRD_V_RANGE = [-10, 10]
        PIPE_X_RANGE = [0, 800]
        PIPE_Y_RANGE = [0, 800]
        
        self.action_space = spaces.Discrete(2)
        
        # Expects normalized inputs!
        self.observation_space = spaces.Box(low=0, high=1,
                                            shape=(N_INPUTS), dtype=np.float32)
    
    def normalize(self, x, range):
        return (x - range[0]) / (range[1] - range[0])
    
    def create_observation(self):
        return np.array([
            self.normalize(self.game.bird_position_y, self.BIRD_Y_RANGE),
            self.normalize(self.game.bird_velocity, self.BIRD_V_RANGE),
            self.normalize(self.game.pipe_position_x[0], self.PIPE_X_RANGE),
            self.normalize(self.game.pipe_position_y[0], self.PIPE_Y_RANGE)
        ])

    def calculate_reward(self):
        return self.game.score

    def step(self, action):

        print(action)
        self.game.perform_action(action)

        self.game.update()

        observation = self.create_observation()
        reward = self.calculate_reward()
        terminated = self.game.game_over
        return observation, reward, terminated, False, {}

    def reset(self, seed=None, options=None):
        self.game.reset()
        observation = self.create_observation()
        return observation, {}

    def render(self):
        self.game.render()

    def close(self):
        self.game.close()