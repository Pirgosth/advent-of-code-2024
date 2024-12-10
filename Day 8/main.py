from functools import reduce


def get_all_antennas(frequency: str, map: list[str], w: int, h: int):
    antennas = []
    for j in range(h):
        for i in range(w):
            if map[j * w + i] == frequency:
                antennas.append((i, j))
    
    return antennas

def compute_nodes_mask(map: list[str], w: int, h: int):

    nodes_mask = ["."] * (w * h)

    for j in range(h):
        for i in range(w):
            antenna = map[j * w + i]
            if antenna == ".":
                continue

            all_antennas = get_all_antennas(antenna, map, w, h)
            for other_antenna in all_antennas:
                if (i, j) == other_antenna:
                    continue

                slide_vector = (other_antenna[0] - i, other_antenna[1] - j)
                
                node = (i + 2 * slide_vector[0], j + 2 * slide_vector[1])

                if node[0] >= 0 and node[0] < w and node[1] >= 0 and node[1] < h:
                    nodes_mask[node[1] * w + node[0]] = "#"

    for j in range(h):
        line = ""
        for i in range(w):
            line += nodes_mask[j * w + i]
        
        print(line)

    return nodes_mask

def compute_nodes_mask_2(map: list[str], w: int, h: int):

    nodes_mask = ["."] * (w * h)

    for j in range(h):
        for i in range(w):
            antenna = map[j * w + i]
            if antenna == ".":
                continue

            all_antennas = get_all_antennas(antenna, map, w, h)
            for other_antenna in all_antennas:
                if (i, j) == other_antenna:
                    continue

                slide_vector = (other_antenna[0] - i, other_antenna[1] - j)
                
                node = (i,j)

                while node[0] >= 0 and node[0] < w and node[1] >= 0 and node[1] < h:
                    nodes_mask[node[1] * w + node[0]] = "#"
                    node = (node[0] + slide_vector[0], node[1] + slide_vector[1])

    for j in range(h):
        line = ""
        for i in range(w):
            line += nodes_mask[j * w + i]
        
        print(line)

    return nodes_mask

def count_nodes(nodes_mask: list[str]) -> int:
    return reduce(lambda x, y: x + 1 if y == "#" else x, nodes_mask, 0)

def main():
    with open("input.txt", "r", encoding="utf-8") as input:
        map = []
        w, h = 0, 0
        for line in input:
            h += 1
            w = len(line) - 1
            for c in line[:-1]:
                map.append(c)

    nodes_mask = compute_nodes_mask(map, w, h)
    result = count_nodes(nodes_mask)

    print("[Part1] Result is", result)

    nodes_mask_2 = compute_nodes_mask_2(map, w, h)
    result_2 = count_nodes(nodes_mask_2)

    print("[Part2] Result is", result_2)

main()