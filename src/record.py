from game import FlappyBird
import os
import pygame
import numpy as np
import pickle

print(os.getcwd())

def save_transitions(data, path):
    pickle.dump(data, open(path+".p", "wb"))
    # np.save(path, data)

if not os.path.exists('recordings'):
    os.mkdir('recordings')

recording_path = "recordings/"
record_index = 0
record_index_str = "recording_"+str(record_index).zfill(3)

# check if file already exists
while os.path.exists(recording_path + record_index_str+".p"):
    record_index += 1
    record_index_str = "recording_"+str(record_index).zfill(3)

path = recording_path + record_index_str

if __name__ == '__main__':
    game = FlappyBird()
    # game.setup()
    game.reset()

    recorded_input_data = []

    while pygame.display.get_init():
        game.update()


        # save input data to a list
        recorded_input_data.append([game.get_observation().tolist(), game.jumping, {}, game.is_game_over()])

        if pygame.display.get_init():
            game.render()
    
    save_transitions(recorded_input_data, path)

print("Recording saved to", path+".p")