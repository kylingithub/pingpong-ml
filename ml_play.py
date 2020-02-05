"""
The template of the script for the machine learning process in game pingpong
"""

# Import the necessary modules and classes
import games.pingpong.communication as comm
from games.pingpong.communication import (
    SceneInfo, GameStatus, PlatformAction
)


def compute_x_end_1P(ball, ball_last):
    direction_x = ball[0] - ball_last[0]
    direction_y = ball[1] - ball_last[1]
    ball_x_end = 0
    # y = mx + c
    if direction_y>0 and direction_x!=0:
        m = direction_y / direction_x
        c = ball[1] - m*ball[0]
        ball_x_end = (420 - c )/m
    else:
        ball_x_end = 110

    while ball_x_end < 0 or ball_x_end > 200:
        if ball_x_end<0:
            ball_x_end = -ball_x_end
        elif ball_x_end>200:
            ball_x_end = 400-ball_x_end

    return ball_x_end

def compute_x_end_2P(ball, ball_last):
    direction_x = ball[0] - ball_last[0]
    direction_y = ball[1] - ball_last[1]
    ball_x_end = 0
    # y = mx + c
    if direction_y < 0 and direction_x!=0:
        m = direction_y / direction_x
        c = ball[1] - m*ball[0]
        ball_x_end = (80 - c )/m
    else:
        ball_x_end = 110

    while ball_x_end < 0 or ball_x_end > 200:
        if ball_x_end<0:
            ball_x_end = -ball_x_end
        elif ball_x_end>200:
            ball_x_end = 400-ball_x_end
    # print(ball_x_end)
    return ball_x_end


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

    # 2. Inform the game process that ml process is ready
    comm.ml_ready()

    if side == "1P":
        ml_loop_for_1P()
    else:
        ml_loop_for_2P()

def ml_loop_for_1P():
    ball_last = [101, 101]
    # 3. Start an endless loop
    while True:
        # 3.1. Receive the scene information sent from the game process
        scene_info = comm.get_scene_info()

        # 3.2. If either of two sides wins the game, do the updating or
        #      resetting stuff and inform the game process when the ml process
        #      is ready.
        if scene_info.status == GameStatus.GAME_1P_WIN or \
                scene_info.status == GameStatus.GAME_2P_WIN:
            # Do some updating or resetting stuff

            # 3.2.1 Inform the game process that
            #       the ml process is ready for the next round
            comm.ml_ready()
            continue

        # 3.3 Put the code here to handle the scene information

        # print(scene_info.ball)
        ball_x_end = compute_x_end_1P(scene_info.ball, ball_last)
        ball_last = scene_info.ball
        move = (ball_x_end) - (scene_info.platform_1P[0] + 15)
        # motion direction of ball
        # compute the location of falling

        # 3.4. Send the instruction for this frame to the game process
        if move > 0:
            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
        elif move < 0:
            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
        else:
            comm.send_instruction(scene_info.frame, PlatformAction.NONE)


def ml_loop_for_2P():
    ball_last = [101, 101]

    # 3. Start an endless loop
    while True:
        # 3.1. Receive the scene information sent from the game process
        scene_info = comm.get_scene_info()

        # 3.2. If either of two sides wins the game, do the updating or
        #      resetting stuff and inform the game process when the ml process
        #      is ready.
        if scene_info.status == GameStatus.GAME_1P_WIN or \
                scene_info.status == GameStatus.GAME_2P_WIN:
            # Do some updating or resetting stuff

            # 3.2.1 Inform the game process that
            #       the ml process is ready for the next round
            comm.ml_ready()
            continue

        # 3.3 Put the code here to handle the scene information

        # print(scene_info.ball)
        ball_x_end = compute_x_end_2P(scene_info.ball, ball_last)
        ball_last = scene_info.ball
        move = (ball_x_end) - (scene_info.platform_2P[0] + 15)
        # motion direction of ball
        # compute the location of falling

        # 3.4. Send the instruction for this frame to the game process
        if move > 0:
            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
        elif move < 0:
            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
        else:
            comm.send_instruction(scene_info.frame, PlatformAction.NONE)

