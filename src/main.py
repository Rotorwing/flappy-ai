import stable_baselines3
from stable_baselines3 import PPO
import os
from env import FlappyBirdEnv

models_dir = "models/PPO"
logdir = "logs"

if not os.path.exists(models_dir):
    os.makedirs(models_dir)

if not os.path.exists(logdir):
    os.makedirs(logdir)

env = FlappyBirdEnv()

model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=logdir)

# model.load("models/PPO/100000")

TIMESTEPS = 10000
iters = 0
for i in range(30):
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name="PPO")
    model.save(f"{models_dir}/{TIMESTEPS*i}")