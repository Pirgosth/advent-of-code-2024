def push_boxes(box_position: tuple[int, int], direction: tuple[int, int], map: list[str], w: int, h: int) -> bool:
    current_position = box_position
    
    while map[current_position[1] * w + current_position[0]] != ".":
        current_position = current_position[0] + direction[0], current_position[1] + direction[1]
        # print(current_position)
        if map[current_position[1] * w + current_position[0]] == "#":
            return False
        
    map[box_position[1] * w + box_position[0]] = "@"
    current_position = box_position
    
    while True:
        current_position = current_position[0] + direction[0], current_position[1] + direction[1]
        last_box = map[current_position[1] * w + current_position[0]] == "."
        map[current_position[1] * w + current_position[0]] = "O"
        if last_box:
            break

    return True

def move_robot(position: tuple[int, int], map: list[str], w: int, h: int, move: str):
    directions = {
        "^": (0, -1),
        ">": (1, 0),
        "<": (-1, 0),
        "v": (0, 1),
    }

    direction = directions[move]
    
    next_robot_position = position[0] + direction[0], position[1] + direction[1]

    # Facing a wall
    if map[next_robot_position[1] * w + next_robot_position[0]] == "#":
        return position
    
    # Facing a box
    if map[next_robot_position[1] * w + next_robot_position[0]] == "O":
        # Behind a wall
        if not push_boxes(next_robot_position, direction, map, w, h):
            return position

        # Abled to push
        map[position[1] * w + position[0]] = "."
        return position[0] + direction[0], position[1] + direction[1]
    
    # No constraint
    map[position[1] * w + position[0]] = "."
    map[next_robot_position[1] * w + next_robot_position[0]] = "@"
    return position[0] + direction[0], position[1] + direction[1]

def apply_robot_moves(map: list[str], w: int, h: int, moves: list[str]):
    robot_position = get_initial_position(map, w, h)
    
    for move in moves:
        robot_position = move_robot(robot_position, map, w, h, move)

def get_initial_position(map: list[str], w: int, h: int) -> tuple[int, int]:
    for j in range(h):
        for i in range(w):
            if map[j * w + i] == "@":
                return (i, j)
        
    return (-1, -1)

def print_map(map: list[str], w: int, h: int):
    for j in range(h):
        line = ""
        for i in range(w):
            line += map[j * w + i]
        print(line)

def compute_score(map: list[str], w: int, h: int) -> int:
    score = 0

    for j in range(h):
        for i in range(w):
            if map[j * w + i] == "O":
                score += 100 * j + i

    return score

def compute_score_2(map: list[str], w: int, h: int) -> int:
    score = 0

    for j in range(h):
        for i in range(w):
            if map[j * w + i] == "[":
                score += 100 * j + i

    return score

def double_map(map: list[str], w: int, h: int) -> tuple[list[str], int, int]:
    doubled_map = []
    
    mapping = {
        "#": ["#", "#"],
        "O": ["[", "]"],
        ".": [".", "."],
        "@": ["@", "."]
    }

    for j in range(h):
        for i in range(w):
            for d in mapping[map[j * w + i]]:
                doubled_map.append(d)

    return doubled_map, 2 * w, h

def get_next_boxes(position: tuple[int, int], direction: tuple[int, int], map: list[str], w: int, h: int) -> tuple[list[tuple[int, int]], bool]:
    next_box_position = position[0], position[1] + direction[1]
    
    next_type = map[next_box_position[1] * w + next_box_position[0]]

    if next_type == "[":
        return [next_box_position, (next_box_position[0] + 1, next_box_position[1])], True

    elif next_type == "]":
        return [next_box_position, (next_box_position[0] - 1, next_box_position[1])], True

    else:
        return [], next_type != "#"


def push_boxes_vertical(box_position: tuple[int, int], direction: tuple[int, int], map: list[str], w: int, h: int) -> bool:
    print("TRYING TO PUSH BOXES FROM", box_position)
    boxes_to_push = []
    next_boxes = [box_position]

    if map[box_position[1] * w + box_position[0]] == "[":
        next_boxes.append((box_position[0] + 1, box_position[1]))
    else:
        next_boxes.append((box_position[0] - 1, box_position[1]))

    # print(next_boxes)

    while len(next_boxes) != 0:
        next_box = next_boxes.pop()
        boxes_to_push.append(next_box)

        boxes, able_to_move = get_next_boxes(next_box, direction, map, w, h)
        if not able_to_move:
            print("BOXES ARE STUCK", box_position)
            return False

        for box in boxes:
            next_boxes.append(box)

    boxes_to_push = set(boxes_to_push)
    print(boxes_to_push)

    for box in sorted(boxes_to_push, key=lambda x: x[1], reverse=(direction[1] > 0)):
        next_box = box[0], box[1] + direction[1]
        map[next_box[1] * w + next_box[0]] = map[box[1] * w + box[0]]
        map[box[1] * w + box[0]] = "."

    map[box_position[1] * w + box_position[0]] = "@"

    return True

def push_boxes_2(box_position: tuple[int, int], direction: tuple[int, int], map: list[str], w: int, h: int) -> bool:
    if direction[1] == 0:
        current_position = box_position
        
        while map[current_position[1] * w + current_position[0]] != ".":
            current_position = current_position[0] + direction[0], current_position[1] + direction[1]
            # print(current_position)
            if map[current_position[1] * w + current_position[0]] == "#":
                return False
            
        map[box_position[1] * w + box_position[0]] = "@"
        current_position = box_position
        
        i = 0 if direction[0] > 0 else -1
        while True:
            current_position = current_position[0] + direction[0], current_position[1] + direction[1]
            last_box = map[current_position[1] * w + current_position[0]] == "."
            map[current_position[1] * w + current_position[0]] = "[" if i % 2 == 0 else "]"
            i += 1
            if last_box:
                break

        return True

    return push_boxes_vertical(box_position, direction, map, w, h)

def move_robot_2(position: tuple[int, int], map: list[str], w: int, h: int, move: str):
    directions = {
        "^": (0, -1),
        ">": (1, 0),
        "<": (-1, 0),
        "v": (0, 1),
    }

    direction = directions[move]
    
    next_robot_position = position[0] + direction[0], position[1] + direction[1]

    # Facing a wall
    if map[next_robot_position[1] * w + next_robot_position[0]] == "#":
        return position
    
    # Facing a box
    if map[next_robot_position[1] * w + next_robot_position[0]] in ["[", "]"]:
        # Behind a wall
        if not push_boxes_2(next_robot_position, direction, map, w, h):
            return position

        # Abled to push
        map[position[1] * w + position[0]] = "."
        return position[0] + direction[0], position[1] + direction[1]
    
    # No constraint
    map[position[1] * w + position[0]] = "."
    map[next_robot_position[1] * w + next_robot_position[0]] = "@"
    return position[0] + direction[0], position[1] + direction[1]

def apply_robot_moves_2(map: list[str], w: int, h: int, moves: list[str]):
    robot_position = get_initial_position(map, w, h)
    
    for move in moves:
        robot_position = move_robot_2(robot_position, map, w, h, move)

def main():
    with open("input.txt", "r", encoding="utf-8") as input:
        map = []
        moves = []
        raw_input = input.read()[:-1]
        raw_map, raw_moves = raw_input.split("\n\n")

        w, h = 0, 0

        for line in raw_map.split("\n"):
            w = len(line)
            h += 1
            for c in line:
                map.append(c)

        for c in raw_moves:
            if c == "\n":
                continue
                
            moves.append(c)

    dmap, dw, dh = double_map(map, w, h)

    apply_robot_moves(map, w, h, moves)
    score = compute_score(map, w, h)
    print("[Part1] Score is", score)

    print_map(dmap, dw, dh)
    # print(moves)
    apply_robot_moves_2(dmap, dw, dh, moves)
    print_map(dmap, dw, dh)

    score_2 = compute_score_2(dmap, dw, dh)
    print("[Part2] Score is", score_2)

main()