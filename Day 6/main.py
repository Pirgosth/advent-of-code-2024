
from copy import deepcopy


def find_start_pos(map: list[str], size: tuple[int, int]):
    w, h = size
    for j in range(h):
        for i in range(w):
            if map[j * w + i] == "^":
                return (i, j)
            
    return (-1, -1)

def look_for_guard_path(map: list[str], size: tuple[int, int]):
    pos = find_start_pos(map, size)

    w, h = size

    known_pos = ["."] * (w * h)
    direction = (0, -1)

    while pos[0] >= 0 and pos[0] < w and pos[1] >= 0 and pos[1] < h:
        i, j = pos
        known_pos[j * w + i] = "X"
        i += direction[0]
        j += direction[1]
        if i >= 0 and i < w and j >= 0 and j < h:
            destination = map[j * w + i]
            if destination == "#":
                direction = rotate(direction)
                continue
        
        pos = (i, j)

    return known_pos
        
def rotate(direction):
    if direction == (0, -1):
        return (1, 0)
    if direction == (1, 0):
        return (0, 1)
    if direction == (0, 1):
        return (-1, 0)
    if direction == (-1, -0):
        return (0, -1)
    
def count_known_positions(known_positions: list[str]):
    result = 0

    for pos in known_positions:
        if pos == "X":
            result += 1
        
    return result

def is_path_a_loop(start_pos: tuple[str, str], map: list[str], size: tuple[int, int]):
    pos = start_pos

    w, h = size
    direction = (0, -1)

    path = {}

    while pos[0] >= 0 and pos[0] < w and pos[1] >= 0 and pos[1] < h:
        i, j = pos

        if (pos, direction) not in path:
            path[(pos, direction)] = True
        else:
            return True

        i += direction[0]
        j += direction[1]
        if i >= 0 and i < w and j >= 0 and j < h:
            if map[j * w + i] == "#":
                direction = rotate(direction)
                continue
        
        pos = (i, j)

    return False

def compute_path_obfuscations(map: list[str], size: tuple[int, int]):
    known_pos = look_for_guard_path(map, size)
    w, h = size

    result = 0
    start_pos = find_start_pos(map, size)

    for j in range(h):
        for i in range(w):
            if known_pos[j * w + i] != "X":
                continue

            map[j * w + i] = "#"

            if is_path_a_loop(start_pos, map, size):
                print("Testing pair:", i, j, "Loop = True")
                result += 1
            else:
                print("Testing pair:", i, j, "Loop = False")

            map[j * w + i] = "."

        
    return result

def main():
    with open("input.txt", "r", encoding="utf-8") as input:
        map = []
        w, h = 0, 0
        for line in input:
            w = len(line) - 1
            h += 1
            for c in line[:-1]:
                map.append(c)

    known_pos = look_for_guard_path(map, (w, h))
    result = count_known_positions(known_pos)

    result_2 = compute_path_obfuscations(map, (w, h))

    print("[Part1] Result is:", result)
    print("[Part2] Result is:", result_2)


main()