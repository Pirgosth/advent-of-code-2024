import re
from PIL import Image

def print_map(robots: list[tuple[tuple[int, int], tuple[int, int]]], w: int, h: int, iteration: int):
    map = [(0, 0, 0)] * (w * h)
    for (xp, yp), _ in robots:
        map[yp * w + xp] = (255, 255, 255)

    im = Image.new("RGB", (w, h))
    im.putdata(map)
    im.save(f"out/{iteration}.jpeg")

    # with open("output.txt", "a", encoding = "utf-8") as output:
    #     for j in range(h):
    #         line = ""
    #         for i in range(w):
    #             line += map[j * w + i]
    #         # print(line)
    #         output.write(line + "\n")
        
    #     output.write("\n")
    #     output.write(str(iteration))
    #     output.write("\n\n")

    # return map

def simulate_robots(robots: list[tuple[tuple[int, int], tuple[int, int]]], w: int, h: int):
    k = 0
    for k in range(1, 10001):
        print_map(robots, w, h, k)
        print(k)
        for i, (p, v) in enumerate(robots):
            fp = p[0] + v[0], p[1] + v[1]
            fp = fp[0] % w, fp[1] % h
            robots[i] = fp, v

def count_quadrants(robots: list[tuple[tuple[int, int], tuple[int, int]]], w: int, h: int) -> dict[int, int]:
    quadrants = {i:0 for i in range(4)}

    for (xp, yp), _ in robots:
        if xp == (w // 2) or yp == (h // 2):
            continue

        xi, yi = 0, 0
        if xp > (w // 2):
            xi = 1
        if yp > (h // 2):
            yi = 1       

        quadrant_index = xi + 2 * yi
        quadrants[quadrant_index] += 1     

    return quadrants

def compute_score(quadrants: dict[int, int]) -> int:
    score = 1
    for q in quadrants.values():
        score *= q

    return score

def main():
    with open("input.txt", "r", encoding="utf-8") as input:
        robots = []
        w, h = 101, 103

        for line in input:
            m = re.match(r"p=(.+?),(.+?) v=(.+?),(.+)", line[:-1])
            xp, yp, xv, yv = m.groups()

            robots.append(((int(xp), int(yp)), (int(xv), int(yv))))

        print(robots)
        simulate_robots(robots, w, h)
        # print_map(robots, w, h)

        quadrants = count_quadrants(robots, w, h)
        print(quadrants)

        score = compute_score(quadrants)
        print(score)

main()