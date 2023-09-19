import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from env import FlappyBirdEnv
from stable_baselines3.common.evaluation import evaluate_policy
import pickle
import os

from imitation.algorithms import bc
from imitation.algorithms.dagger import SimpleDAggerTrainer
import tempfile
from imitation.data import types

rng = np.random.default_rng(0)
env = FlappyBirdEnv()
env.disable_rendering()
venv = DummyVecEnv([lambda: env])

def load_transitions(path):
    # transitions = np.load(path)
    index = 0
    data = []
    # print (path+"_"+str(index).zfill(3)+".p")
    while os.path.exists(path+"_"+str(index).zfill(3)+".p"):
        print (path+"_"+str(index).zfill(3)+".p")
        data += pickle.load(open(path+"_"+str(index).zfill(3)+".p", "rb"))
        data[-1][3] = True
        index += 1
    # print(transitions)
    trajectories = []
    observations = []
    actions = []
    infos = []
    terminals = []
    for i in range(len(data)):
        observations.append(data[i][0])
        actions.append(data[i][1])
        infos.append(data[i][2])
        terminals.append(data[i][3])
        print(data[i][0], data[i][1], data[i][2], data[i][3])
        if data[i][3]:
            print("new trajectory", len(observations))
            trajectories.append(types.Trajectory(np.array(observations), np.array(actions[:-1]), np.array(infos[:-1]), True))
            observations = []
            actions = []
            infos = []
            terminals = []

    # print("observations", observations)
    # print(actions)
    # print(infos)
    # print(terminals)
    # types.Transitions
    # transitions = types.Transitions(np.array(observations[:-1]), np.array(actions[:-1]), np.array(infos[:-1]), np.array(observations[1:]), np.array(terminals[:-1]))

    

    return trajectories


transitions = load_transitions("recordings/recording")
# print(transitions)

bc_trainer = bc.BC(
    observation_space=env.observation_space,
    action_space=env.action_space,
    demonstrations=transitions,
    rng=rng,
)
# bc_trainer.train(n_epochs=100)

# model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=logdir)

with tempfile.TemporaryDirectory(prefix="dagger_example_") as tmpdir:
    print(tmpdir)
    dagger_trainer = SimpleDAggerTrainer(
        venv=venv,
        scratch_dir=tmpdir,
        bc_trainer=bc_trainer,
        expert_trajs=transitions,
        expert_policy=bc_trainer.policy,
        rng=rng,
    )
    dagger_trainer.train(15_000)

    dagger_trainer.policy.save("clone_models/clone_model_DAgger_001")
    env.enable_rendering()
    reward, _ = evaluate_policy(dagger_trainer.policy, env, 500)
# policy.save(f"clone_models/clone_model_{000}")

print("Reward:", reward)
