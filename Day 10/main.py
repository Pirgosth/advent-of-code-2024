def get_trailheads(map: list[int], w: int, h: int):
    trailheads = []    
    
    for j in range(h):
        for i in range(w):
            if map[j * w + i] == 0:
                trailheads.append((i, j))

    return trailheads

def get_elevated_neighbours(map: list[int], w: int, h: int, step: tuple[int, int]):
    directions = [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1)
    ]

    elevated_neighbours = []

    i, j = step

    for di, dj in directions:
        ni, nj = i + di, j + dj
        if ni >= 0 and ni < w and nj >= 0 and nj < h and (map[nj * w + ni] == map[j * w + i] + 1):
            elevated_neighbours.append((ni, nj))

    return elevated_neighbours

def compute_trailhead_score(map: list[int], w: int, h: int, trailhead: tuple[int, int], distinct = False) -> int:
    next_steps = [trailhead]
    heads_found = []

    while len(next_steps) > 0:
        i, j = next_steps.pop()
        elevated_neighbours = get_elevated_neighbours(map, w, h, (i, j))
        for neighbour in elevated_neighbours:
            if map[neighbour[1] * w + neighbour[0]] != 9:
                next_steps.append(neighbour)
            else:
                heads_found.append(neighbour)

    return len(heads_found if distinct else set(heads_found))

def compute_map_score(map: list[int], w: int, h: int, trailheads: list[tuple[int, int]], distinct = False):
    score = 0
    for trailhead in trailheads:
        score += compute_trailhead_score(map, w, h, trailhead, distinct)

    return score

def main():
    with open("input.txt", "r", encoding="utf-8") as input:
        map = []
        w, h = 0, 0
        for line in input:
            w = len(line) - 1
            h += 1
            for c in line[:-1]:
                map.append(int(c))

    trailheads = get_trailheads(map, w, h)

    score = compute_map_score(map, w, h, trailheads)
    print("[Part1] Score is", score)

    score_2 = compute_map_score(map, w, h, trailheads, distinct=True)
    print("[Part2] Score is", score_2)

main()