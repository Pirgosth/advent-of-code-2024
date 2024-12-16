def get_position(character: str, map: list[str], w: int, h: int) -> tuple[int, int]:
    for j in range(h):
        for i in range(w):
            if map[j * w + i] == character:
                return (i, j)

    return (-1, -1)

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
        if map[next_node[1] * w + next_node[0]] in (".", "E"):
            next_nodes.append(next_node)

    return next_nodes

def compute_direction(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return b[0] - a[0], b[1] - a[1]

def get_shortest_path(visited: dict[tuple[int, int], tuple[int, dict[tuple[int, int], bool]]], shortest_path_length: int) -> dict[tuple[int, int]]:
    last_node = None
    for node, directions in visited.items():
        for score, _ in directions.values():
            if score == shortest_path_length - 1:
                last_node = node
                break

    assert last_node is not None

    to_explore = [(last_node, shortest_path_length)]
    
    done = {}

    while len(to_explore) > 0:
        node, score = to_explore.pop()

        if node is None:
            continue

        done[node] = True

        for next_score, next_nodes in visited[node].values():
            for next_node in next_nodes.keys():
                if next_node not in done and next_score < score:
                    to_explore.append((next_node, next_score))

    return done

def get_shortest_path_length(start: tuple[int, int], end: tuple[int, int], map: list[str], w: int, h: int) -> tuple[list[tuple[int, int]], int]:
    visited = {}

    to_visit = [(start, 0, (1, 0), None)]

    final_scores = []

    while len(to_visit) > 0:
        (node, score, dir, from_node) = to_visit.pop(0)

        if node == end:
            final_scores.append(score)
            continue

        if node not in visited:
            visited[node] = {}

        if dir in visited[node] and score > visited[node][dir][0]:
            continue

        visited[node][dir] = (score, {from_node: True})

        for next_node in get_next_nodes(node, map, w, h):
            next_dir = compute_direction(node, next_node)
            next_score = score + 1
            if dir != next_dir:
                next_score += 1000

            to_visit.append((next_node, next_score, next_dir, node))

    shortest_path_length = min(final_scores)

    return shortest_path_length, get_shortest_path(visited, shortest_path_length)


def main():
    with open("input.txt", "r", encoding="utf-8") as input:
        map = []
        w, h = 0, 0

        for line in input:
            w = len(line) - 1
            h += 1
            for c in line[:-1]:
                map.append(c)

    start = get_position("S", map, w, h)
    end = get_position("E", map, w, h)

    shortest_path_length, path = get_shortest_path_length(start, end, map, w, h)

    print("[Part1] Result is", shortest_path_length)
    # We need to add 1 for the arrival
    print("[Part2] Result is", len(path) + 1)

    for node in path.keys():
        map[node[1] * w + node[0]] = "O"

    img = []

    for c in map:
        if c == "#":
            img.append((255, 0, 0))
        elif c == ".":
            img.append((0, 0, 0))
        elif c == "O":
            img.append((0, 255, 0))
        else:
            img.append((255, 255, 255))

    from PIL import Image

    im = Image.new("RGB", (w, h))
    im.putdata(img)
    im = im.resize((w * 4, h * 4), resample=Image.BOX)
    im.save(f"output.png")

main()
