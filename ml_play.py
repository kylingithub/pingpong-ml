"""
The template of the script for the machine learning process in game pingpong

Only "2P"
"""
import pickle, os
import numpy as np

class MLPlay:
    def __init__(self, side):
        """
        Constructor

        @param side A string "1P" or "2P" indicates that the `MLPlay` is used by
               which side.
        """
        self.ball_served = False
        self.side = side
        # Need scikit-learn==0.22.2 
        with open(os.path.join(os.path.dirname(__file__),'save','model.pickle'), 'rb') as f:
            self.model = pickle.load(f)

    def update(self, scene_info):
        """
        Generate the command according to the received scene information
        """
        if scene_info["status"] != "GAME_ALIVE":
            return "RESET"

        if not self.ball_served:
            self.ball_served = True
            return "SERVE_TO_LEFT"
        else:
            if scene_info["ball_speed"][1] > 0 :
                if scene_info["ball_speed"][0] > 0:
                    direction = 0
                else :
                    direction = 1
            else :
                if scene_info["ball_speed"][0] > 0:
                    direction = 2
                else:
                    direction = 3
            X = [scene_info["ball"][0], scene_info["ball"][1], direction, scene_info["blocker"][0],scene_info["ball_speed"][0],scene_info["ball_speed"][1]]
            X = np.array(X).reshape((1,-1))
            pred = self.model.predict(X)
            if scene_info["platform_2P"][0]+20  > (pred-10)and scene_info["platform_2P"][0]+20 < (pred+10):
                if scene_info["platform_2P"][1]+30-scene_info["ball_speed"][1] > scene_info["ball"][1] : #slice
                    return "NONE"
                else :
                    return "NONE" # NONE
            elif scene_info["platform_2P"][0]+20 <= (pred-10) : return "MOVE_RIGHT" # goes right
            else : return "MOVE_LEFT" # goes left

    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
