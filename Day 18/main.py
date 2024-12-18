def get_next_nodes(node: tuple[int, int], map: list[str], w: int, h: int) -> list[tuple[int, int]]:
    directions = [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1)
    ]

    next_nodes = []

    for direction in directions:
        next_node = node[0] + direction[0], node[1] + direction[1]
        if next_node[0] >= 0 and next_node[0] < w and next_node[1] >= 0 and next_node[1] < h and map[next_node[1] * w + next_node[0]] == ".":
            next_nodes.append(next_node)

    return next_nodes

def find_shortest_path_length(map: list[str], w: int, h: int) -> int | None:
    visited = {}

    to_visit = [((0, 0), 0)]

    final_scores = []

    while len(to_visit) > 0:
        (node, score) = to_visit.pop(0)

        if node == (w - 1, h -1):
            final_scores.append(score)
            continue

        if node in visited:
            continue

        visited[node] = True

        for next_node in get_next_nodes(node, map, w, h):
            next_score = score + 1

            to_visit.append((next_node, next_score))

    shortest_path_length = min(final_scores) if len(final_scores) > 0 else None

    return shortest_path_length

def print_map(map: list[str], w: int, h: int):
    for j in range(h):
        line = ""
        for i in range(w):
            line += map[j * w + i]

        line += "\n"
        print(line)

def main():
    with open("input.txt", "r", encoding="utf-8") as input:
        w, h = 71, 71
        map = ["."] * w * h
        falling_bytes = []
        for line in input:
            x, y = line[:-1].split(",")
            x, y = int(x), int(y)
            falling_bytes.append((x, y))

        for x, y in falling_bytes[:1024]:
            map[y * w + x] = '#'

    shortest_path_length = find_shortest_path_length(map, w, h)
    print("[Part1] Result is:", shortest_path_length)

    breaking_coords = None
    for (x, y) in falling_bytes[1024:]:
        map[y * w + x] = '#'
        if find_shortest_path_length(map, w, h) is None:
            breaking_coords = (x, y)
            break

    print("[Part2] Result is:", f"{breaking_coords[0]},{breaking_coords[1]}")

main()