def get_compatible_neighbours(pos: tuple[int, int], type: str, map: list[str], w: int, h: int):
    directions = [
        (0, 1),
        (0, -1),
        (1, 0),
        (-1, 0)
    ]

    i, j = pos

    neighbours = []
    for direction in directions:
        ni, nj = i + direction[0], j + direction[1]
        if ni >= 0 and ni < w and nj >= 0 and nj < h and map[nj * w + ni] == type:
            # print(map[nj * w + ni])
            neighbours.append((ni, nj, direction))

    return neighbours

def get_line(fences: dict[tuple[int, int], list[tuple[int, int]]], fence: tuple[int, int], slope: tuple[int, int]) -> list[tuple[int, int]]:
    i, j = fence
    line = []

    di, dj = i, j

    # print(fences.keys())

    while (di, dj) in fences and slope in fences[(di, dj)]:
        # print(di, dj, slope)
        # print(fences[(di, dj)])

        line.append((di, dj))
        di, dj = di + slope[0], dj + slope[1]

    di, dj = i, j

    while (di, dj) in fences and slope in fences[(di, dj)]:
        # print(di, dj, slope)
        line.append((di, dj))
        di, dj = di - slope[0], dj - slope[1]
        
    return list(set(line))


def compute_perimeter(fences: dict[tuple[int, int], list[tuple[int, int]]]) -> int:
    perimeter = 0
    done = {}

    print(fences)

    for fence, slopes in fences.items():
        for slope in slopes:
            
            if (fence, slope) in done:
                continue

            perimeter += 1
            line = get_line(fences, fence, slope)
            # print(fence, slope)
            print(line, slope)
            # print(done)

            for x in line:
                done[(x, slope)] = True

            # return len(fences.keys())

        # print(fence, directions)

    print(fences)

    return perimeter

def compute_fences_cost(map: list[str], w: int, h: int):

    costs = 0
    regions_done = {}
    debug_costs = []

    for j in range(h):
        for i in range(w):
            if (i, j) in regions_done:
                continue
            # print(i, j)
            area, perimeter = 0, 0

            next_nodes = [(i, j)]
            fences = {}

            while len(next_nodes) > 0:
                li, lj = next_nodes.pop()
                # print(li, lj)
                region_type = map[lj * w + li]
                area += 1

                neighbours = get_compatible_neighbours((li, lj), region_type, map, w, h)
                # perimeter += 4 - len(neighbours)
                
                directions = [
                    (0, 1),
                    (0, -1),
                    (1, 0),
                    (-1, 0)
                ]

                # print((li, lj), neighbours)

                for direction in directions:
                    if (li + direction[0], lj + direction[1]) not in [(i, j) for i, j, _ in neighbours]:
                        if (li, lj) not in fences:
                            fences[(li, lj)] = []
                        fences[(li, lj)].append((direction[1], direction[0]))

                regions_done[(li, lj)] = True
                # print(already_done)
                for neighbour in neighbours:
                    if (neighbour[0], neighbour[1]) not in regions_done and (neighbour[0], neighbour[1]) not in next_nodes:
                        next_nodes.append((neighbour[0], neighbour[1]))
                # print(next_nodes)
                # break

            print(fences)

            perimeter = compute_perimeter(fences)
            
            costs += area * perimeter
            debug_costs.append((region_type, area, perimeter, area * perimeter))

            # print(debug_costs)
            # return costs

    return costs


def main():
    with open("input.txt", "r", encoding="utf-8") as input:
        map = []
        w, h = 0, 0
        for line in input:
            w = len(line) - 1
            h += 1
            for c in line[:-1]:
                map.append(c)
    
    print(map)
    costs = compute_fences_cost(map, w, h)
    print(costs)


main()