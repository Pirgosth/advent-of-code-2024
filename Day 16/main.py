import sys

def get_position(character: str, map: list[str], w: int, h: int) -> tuple[int, int]:
    for j in range(h):
        for i in range(w):
            if map[j * w + i] == character:
                return (i, j)

    return (-1, -1)

def get_next_nodes(node: tuple[int, int], map: list[str], w: int, h: int, done: dict[tuple[int, int]]) -> list[tuple[int, int]]:
    directions = [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1)
    ]

    next_nodes = []

    for direction in directions:
        next_node = node[0] + direction[0], node[1] + direction[1]
        if next_node not in done and map[next_node[1] * w + next_node[0]] in (".", "E"):
            next_nodes.append(next_node)

    return next_nodes

def compute_direction(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return b[0] - a[0], b[1] - a[1]

def get_shortest_path(start: tuple[int, int], end: tuple[int, int], map: list[str], w: int, h: int) -> tuple[list[tuple[int, int]], int]:

    def _get_shortest_path(fr: tuple[int, int], to: tuple[int, int], done: dict[tuple[int, int]], from_direction: tuple[int, int]) -> tuple[list[tuple[int, int]], int]:
        next_nodes = get_next_nodes(fr, map, w, h, done)
        if len(next_nodes) == 0:
            return [], -1

        for next_node in next_nodes:
            if next_node == to:
                return [fr, next_node], 1

        next_done = dict(done)
        next_done[fr] = True

        next_paths = [_get_shortest_path(node, to, next_done, compute_direction(fr, node)) for node in next_nodes]
        next_paths = [path for path in next_paths if path[1] > 0]

        if len(next_paths) == 0:
            return [], -1

        shortest_path = min(next_paths, key=lambda x: x[1])
        # print(shortest_path)

        turn_malus = 0

        if len(shortest_path[0]) > 0:
            to_direction = compute_direction(fr, shortest_path[0][0])

            if from_direction is not None and from_direction != to_direction:
                turn_malus = 1000
        
        # print(turn_malus)

        return [fr] + shortest_path[0], shortest_path[1] + 1 + turn_malus

    return _get_shortest_path(start, end, {}, (1, 0))

def main():
    sys.setrecursionlimit(3000)
    with open("input.txt", "r", encoding="utf-8") as input:
        map = []
        w, h = 0, 0

        for line in input:
            w = len(line) - 1
            h += 1
            for c in line[:-1]:
                map.append(c)

        print(map)

    start = get_position("S", map, w, h)
    end = get_position("E", map, w, h)
    print(start, end)

    shortest_path = get_shortest_path(start, end, map, w, h)
    print(shortest_path)

main()