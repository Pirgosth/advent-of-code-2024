def find_first_position(type: str, map: list[str], w: int, h: int) -> tuple[int, int]:
    for j in range(h):
        for i in range(w):
            if map[j * w + i] == type:
                return (i, j)
            
    return (-1, -1)

def get_neighbours(types: set[str], position: tuple[int, int], map: list[str], w: int, h: int) -> list[tuple[int, int]]:
    directions = [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1),
    ]

    neighbours = []

    for direction in directions:
        neighbour_position = position[0] + direction[0], position[1] + direction[1]
        if neighbour_position[0] < 0 or neighbour_position[0] >= w or neighbour_position[1] < 0 or neighbour_position[1] >= h:
            continue
        if map[neighbour_position[1] * w + neighbour_position[0]] in types:
            neighbours.append(neighbour_position)

    return neighbours

def index_race(map: list[str], w: int, h: int) -> dict[tuple[int, int], int]:
    start = find_first_position("S", map, w, h)
    end = find_first_position("E", map, w, h)

    queue = [(start, 0)]
    index = {}

    while len(queue) > 0:
        process, length = queue.pop(0)
        
        if process == end:
            index[end] = length
            break

        neighbours = get_neighbours([".", "E"], process, map, w, h)

        for neighbour in neighbours:
            if neighbour in index:
                continue

            queue.append((neighbour, length + 1))

        index[process] = length

    return index

def manhattan_distance(a: tuple[int, int], b: tuple[int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_shortcuts_at_position(position: tuple[int, int], max_distance: int, min_distance_saved: int, map: list[str], w: int, h: int, indexed_path: dict[tuple[int, int], int]) -> list[int]:
    results = []
    start = indexed_path[position]

    for j in range(max(0, position[1] - max_distance), min(position[1] + max_distance + 1, h)):
        for i in range(max(0, position[0] - max_distance), min(position[0] + max_distance + 1, h)):
            distance = manhattan_distance(position, (i, j))

            if distance <= max_distance and map[j * w + i] in (".", "E") and start < (to := indexed_path[(i, j)]):
                distance_saved = to - start - distance
                if distance_saved >= max(0, min_distance_saved):
                    results.append(distance_saved)

    return results

def get_shortcuts(map: list[str], w: int, h: int, indexed_path: dict[tuple[int, int], int], max_cheats: int = 0, min_saved_time: int = -1) -> int:
    shortcuts = []
    for position in indexed_path.keys():
        for s in get_shortcuts_at_position(position, max_cheats, min_saved_time, map, w, h, indexed_path):
            shortcuts.append(s)

    return shortcuts

def main():
    with open("input.txt", "r", encoding="utf-8") as input:
        w, h = 0, 0
        map = []
        for line in input:
            w = len(line) - 1
            h += 1
            for c in line[:-1]:
                map.append(c)

    indexed_path = index_race(map, w, h)

    paths = get_shortcuts(map, w, h, indexed_path, max_cheats=2, min_saved_time=100)
    print("[Part1] Result is:", len(paths))

    paths_2 = get_shortcuts(map, w, h, indexed_path, max_cheats=20, min_saved_time=100)
    print("[Part2] Result is:", len(paths_2))

main()