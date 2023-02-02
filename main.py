# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |  |  \  \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |  |   \  \ /(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#  |__|    \__\

import random
import typing
import math


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "",  # TODO: Your Battlesnake Username
        "color": "#684380",  # TODO: Choose color
        "head": "default",  # TODO: Choose head
        "tail": "default",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

    possible_next = {"x": 0, "y": 0}

    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]
    print(f"My head is at {my_head}")  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"
    print(f"My neck is at {my_neck}")
    
    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False

    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False

    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False

    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False

    # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
    board_width = game_state['board']['width']
    print(f"Width {board_width}")
    if my_head["x"] == 0:
        print("Head x is 0, cant go left")
        is_move_safe["left"] = False
    if my_head["x"] == board_width - 1:
        print("Head x is board_width, cant go right")
        is_move_safe["right"] = False
    board_height = game_state['board']['height']
    print(f"Height {board_height}")
    if my_head["y"] == 0:
        is_move_safe["down"] = False
        print("Head y is 0, cant go down")
    if my_head["y"] == board_height - 1:
        is_move_safe["up"] = False
        print("Head y is board_heigth, cant go up")


    # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
    my_body = game_state['you']['body']
    print(f"My body {my_body}")
    head_x = my_head["x"]
    head_y = my_head["y"]

    body_coords = [(b["x"], b["y"]) for b in my_body[1:]]
    opponents = game_state['board']['snakes']
    opponent_bodies = [o["body"] for o in opponents]
    for b in opponent_bodies:
        body_coords.extend(b)

    if any(b == (head_x + 1, head_y) for b in body_coords):
        is_move_safe["right"] = False

    if any(b == (head_x - 1, head_y) for b in body_coords):
        is_move_safe["left"] = False

    if any(b == (head_x, head_y + 1) for b in body_coords):
        is_move_safe["up"] = False

    if any(b == (head_x, head_y - 1) for b in body_coords):
        is_move_safe["down"] = False

    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes

    print(f"Opponents {opponents}")

    food = game_state['board']['food']
    print(f"Food {food}")

    opponent_bodies = [o["body"] for o in opponents]
    opponent_heads = [o[1] for o in opponent_bodies]

    opponent_distances = {}

    for i, f in enumerate(opponent_heads):
        opponent_distances[euclidian_distance(my_head, f)] = f

    closest_opponent = min(opponent_distances)
    closest_opntnetn_coords = opponent_distances[closest_opponent]

    if my_head["x"] < closest_opntnetn_coords["x"]:
        is_move_safe["right"] = False

    if my_head["x"] > closest_opntnetn_coords["x"]:
        is_move_safe["left"] = False

    if my_head["y"] < closest_opntnetn_coords["y"]:
        is_move_safe["up"] = False

    if my_head["y"] > closest_opntnetn_coords["y"]:
        is_move_safe["down"] = False

    food_distances = {}
    
    for i, f in enumerate(food):
        food_distances[euclidian_distance(my_head, f)] = f
        
    print(f"food_distances: {food}")

    closest_food = min(food_distances)
    closest_food_coords = food_distances[closest_food]
    print(f"Closest food: {closest_food_coords}")

    if my_head["x"] < closest_food_coords["x"]:
        if is_move_safe["right"]:
            return {"move": "right"}

    if my_head["x"] > closest_food_coords["x"]:
        if is_move_safe["left"]:
            return {"move": "left"}

    if my_head["y"] < closest_food_coords["y"]:
        if is_move_safe["up"]:
            return {"move": "up"}

    if my_head["y"] > closest_food_coords["y"]:
        if is_move_safe["down"]:
            return {"move": "down"}

    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return random.choice(["right", "left", "down", "up"])

    # Choose a random move from the safe ones
    next_move = random.choice(safe_moves)

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}

def euclidian_distance(point1, point2):
    x = point2["x"] - point1["x"]
    x = x * x
    
    y = point2["y"] - point1["y"]
    y = y * y
    
    total = x + y
    
    return math.sqrt(total)
    
    

# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
