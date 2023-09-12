import stable_baselines3
from stable_baselines3 import PPO
import os
from env import FlappyBirdEnv



logdir = "logs"

# Create directories for logging and model saving if they don't exist:
if not os.path.exists("models"):
    os.makedirs("models")

if not os.path.exists(logdir):
    os.makedirs(logdir)

# Find the next available run index:
run_index = 0
run_index_str = "000"
while os.path.exists(f"models/PPO_{run_index_str}"):
    run_index += 1
    run_index_str = format(run_index, "03d")

# Create directory for model saving:
models_dir = "models/PPO_"+run_index_str
if not os.path.exists(models_dir):
    os.makedirs(models_dir)

# Create environment:
env = FlappyBirdEnv()

# Start Model from scratch:
model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=logdir)

# Continue training from saved model:
# model = PPO.load("models/PPO_000/1000.zip", env=env, verbose=1, tensorboard_log=logdir)

TIMESTEPS = 10000
i = 0
while True:
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name="PPO_"+run_index_str)
    model.save(f"{models_dir}/{TIMESTEPS*i}")
    i+=1