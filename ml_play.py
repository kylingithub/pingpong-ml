"""
The template of the script for the machine learning process in game pingpong
"""

# Import the necessary modules and classes
import pickle
import os
import games.pingpong.communication as comm
from games.pingpong.communication import (
    SceneInfo, GameStatus, PlatformAction
)

def ml_loop(side: str):
    """
    The main loop for the machine learning process

    The `side` parameter can be used for switch the code for either of both sides,
    so you can write the code for both sides in the same script. Such as:
    ```python
    if side == "1P":
        ml_loop_for_1P()
    else:
        ml_loop_for_2P()
    ```

    @param side The side which this script is executed for. Either "1P" or "2P".
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here
    filename = "regressor.sav"
    filepath = os.path.join(os.path.dirname(__file__), filename)
    super_sid = pickle.load(open(filepath,'rb'))
    # super_sid = pickle.load(open(filename,'rb'))
    last_x = 0
    last_y = 0
    # 2. Inform the game process that ml process is ready
    comm.ml_ready()

    # 3. Start an endless loop
    while True:
        # 3.1. Receive the scene information sent from the game process
        scene_info = comm.get_scene_info()

        # 3.2. If either of two sides wins the game, do the updating or
        #      resetting stuff and inform the game process when the ml process
        #      is ready.
        if scene_info.status == GameStatus.GAME_1P_WIN or \
           scene_info.status == GameStatus.GAME_2P_WIN:
            # Do something updating or resetting stuff

            # 3.2.1 Inform the game process that
            #       the ml process is ready for the next round
            comm.ml_ready()
            continue

        ball_X = scene_info.ball[0]
        ball_Y = scene_info.ball[1]
        plat_X = scene_info.platform_2P[0]
        if side == '2P':
            ball_Y = reflector(scene_info, scene_info.ball[1])
            plat_X = scene_info.platform_2P[0]
        direct = [1, 1]
        if ball_X - last_x < 0:
            direct[0] = -1
        if ball_Y - last_y < 0:
            direct[1] = -1
        # 3.3 Put the code here to handle the scene information
        expect_pos = super_sid.predict([[ball_X, ball_Y, direct[0], direct[1]]])

        threshhold = 3
        if plat_X + 16 - expect_pos > threshhold:
            des = -1 # go left
        elif plat_X + 16 - expect_pos < -threshhold:
            des = 1 # go right
        elif expect_pos < 42:
            des = -1
        elif expect_pos > 358:
            des = 1
        else:
            des = 0

        last_x = ball_X
        last_y = ball_Y
        # 3.4 Send the instruction for this frame to the game process
        if des == 1:
            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
        elif des == -1:
            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
        else:
            comm.send_instruction(scene_info.frame, PlatformAction.NONE)


def reflector(scene_info, position_Y):
    mid_line = (scene_info.platform_1P[1] + 35 + scene_info.platform_2P[1] - 0) / 2
    out_y = mid_line + mid_line - position_Y
    return out_y
