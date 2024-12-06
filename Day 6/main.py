from copy import deepcopy

def find_start_pos(map: list[str]):
    for j in range(len(map)):
        for i in range(len(map[j])):
            if map[j][i] == "^":
                return (i, j)
            
    return (-1, -1)

def look_for_guard_path(map: list[str]):
    pos = find_start_pos(map)
    known_pos = [["." for _ in range(len(map[0]))] for _ in range(len(map))]
    direction = (0, -1)

    while pos[0] >= 0 and pos[0] < len(map[0]) and pos[1] >= 0 and pos[1] < len(map):
        i, j = pos
        known_pos[j][i] = "X"
        i += direction[0]
        j += direction[1]
        if i >= 0 and i < len(map[0]) and j >= 0 and j < len(map):
            destination = map[j][i]
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
    
def count_known_positions(known_positions: list[list[str]]):
    result = 0

    for line in known_positions:
        for pos in line:
            if pos == "X":
                result += 1
        
    return result

def is_path_a_loop(map: list[str]):
    start_pos = find_start_pos(map)
    pos = start_pos
    known_pos = [[(".", None) for _ in range(len(map[0]))] for _ in range(len(map))]
    direction = (0, -1)

    path = []
    w, h = len(map[0]), len(map)

    while pos[0] >= 0 and pos[0] < w and pos[1] >= 0 and pos[1] < h:
        i, j = pos

        if (pos, direction) not in path:
            path.append((pos, direction))
        else:
            return True

        known_pos[j][i] = ("X", direction)
        i += direction[0]
        j += direction[1]
        if i >= 0 and i < w and j >= 0 and j < h:
            destination = map[j][i]
            if destination == "#":
                direction = rotate(direction)
                continue
        
        pos = (i, j)

    return False

def compute_path_obfuscations(map: list[str]):
    known_pos = look_for_guard_path(map)

    result = 0

    for j in range(len(map)):
        for i in range(len(map[0])):
            if known_pos[j][i] != "X":
                continue

            test_map = deepcopy(map)
            test_map[j] = test_map[j][:i] + ["#"] + test_map[j][i+1:]

            if is_path_a_loop(test_map):
                print("Testing pair:", i, j, "Loop = True")
                result += 1
            else:
                print("Testing pair:", i, j, "Loop = False")
        
    return result

def main():
    with open("input.txt", "r", encoding="utf-8") as input:
        map = []
        for line in input:
            map.append(list(line[:-1]))

    known_pos = look_for_guard_path(map)
    result = count_known_positions(known_pos)

    print("[Part1] Result is:", result)

    result_2 = compute_path_obfuscations(map)

    print("[Part2] Result is:", result_2)


main()