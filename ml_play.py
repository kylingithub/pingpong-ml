import games.pingpong.communication as comm
from games.pingpong.communication import (
    SceneInfo, GameStatus, PlatformAction
)

def ml_loop(side: str):
    print("For {}".format(side))
    comm.ml_ready()

    while True:
        scene_info = comm.get_scene_info()

        if scene_info.status == GameStatus.GAME_1P_WIN or \
           scene_info.status == GameStatus.GAME_2P_WIN:
            comm.ml_ready()
            continue

        comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
