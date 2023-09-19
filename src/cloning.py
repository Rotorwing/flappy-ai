import numpy as np
from env import FlappyBirdEnv
from stable_baselines3.common.evaluation import evaluate_policy
import pickle
import os

from imitation.algorithms import bc
from imitation.data import types

rng = np.random.default_rng(0)
env = FlappyBirdEnv()

def load_transitions(path):
    # transitions = np.load(path)
    index = 0
    data = []
    # print (path+"_"+str(index).zfill(3)+".p")
    while os.path.exists(path+"_"+str(index).zfill(3)+".p"):
        print (path+"_"+str(index).zfill(3)+".p")
        data += pickle.load(open(path+"_"+str(index).zfill(3)+".p", "rb"))
        index += 1
    # print(transitions)
    observations = []
    actions = []
    infos = []
    terminals = []
    for i in range(len(data)):
        observations.append(data[i][0])
        actions.append(data[i][1])
        infos.append(data[i][2])
        terminals.append(data[i][3])

    print("observations", observations)
    print(actions)
    # print(infos)
    # print(terminals)
    trajectory = types.Transitions(np.array(observations[:-1]), np.array(actions[:-1]), np.array(infos[:-1]), np.array(observations[1:]), np.array(terminals[:-1]))

    return trajectory


transitions = load_transitions("recordings/recording")
# print(transitions)

bc_trainer = bc.BC(
    observation_space=env.observation_space,
    action_space=env.action_space,
    demonstrations=transitions,
    rng=rng,
)
bc_trainer.train(n_epochs=100)
bc_trainer.policy.save("clone_models/clone_model_007")
reward, _ = evaluate_policy(bc_trainer.policy, env, 500)
# policy.save(f"clone_models/clone_model_{000}")

print("Reward:", reward)
