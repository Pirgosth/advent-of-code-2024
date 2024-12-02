def parse_file(file) -> list[list[int]]:
    levels = []
    for line in file:
        line = line[:-1]
        values = [int(v) for v in line.split(" ")]
        levels.append(values)

    return levels

def compute_distance(a: int, b: int) -> int:
    return abs(b - a)

def is_distance_safe(distance: int) -> bool:
    return 1 <= distance and distance <= 3

def is_level_safe(level: list[int], dampener: bool = False, deep = False) -> bool:
    if len(level) <= 1:
        return True

    if not is_distance_safe(compute_distance(level[0], level[1])):
        if not dampener or deep:
            return False
        return is_level_safe([level[0]] + level[2:], True, True) or is_level_safe(level[:0] + level[1:], True, True)

    direction = 1 if level[0] <= level[1] else -1
    for i in range(1, len(level) -1):
        local_direction = 1 if level[i] <= level[i+1] else -1
        if direction != local_direction or not is_distance_safe(compute_distance(level[i], level[i+1])):
            if not dampener:
                return False
            elif dampener:
                return not deep and (is_level_safe(level[:i-1] + level[i:], True, True) or is_level_safe(level[:i] + level[i+1:], True, True) or (is_level_safe(level[:i+1] + level[i+2:], True, True)))
    
    return True

def compute_levels_score(levels: list[list[int]], dampener = False) -> int:
    score = 0

    for level in levels:
        safe = is_level_safe(level, dampener=dampener)
        print(safe, level)
        if safe:
            score += 1

    return score