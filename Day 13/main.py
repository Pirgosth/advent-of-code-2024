import re
from sage.all import *

def compute_prize_cost(prize: tuple[tuple[int, int], tuple[int, int], tuple[int, int]], shifted: bool = False) -> int:
    xa, ya = prize[0]
    xb, yb = prize[1]
    xp, yp = prize[2]

    if shifted:
        xp, yp = xp + 10000000000000, yp + 10000000000000

    p = var("p", domain="integer")
    q = var("q", domain="integer")

    r = solve([
        Integer(xa) * p + Integer(xb) * q == Integer(xp),
        Integer(ya) * p + Integer(yb) * q == Integer(yp)
    ], p, q, domain="integer", solution_dict=True)

    if len(r) == 0:
        return 0

    result = r[0]

    p, q = str(result[p]), str(result[q])
    if not p.isdigit() or not q.isdigit():
        return 0
    
    p, q = int(p), int(q)

    return 3 * p + q

def compute_total_cost(prices: list[tuple[tuple[int, int], tuple[int, int], tuple[int, int]]], shifted: bool = False) -> int:
    total_cost = 0
    
    for price in prices:
        total_cost += compute_prize_cost(price, shifted)

    return total_cost

def main():
    with open("input.txt", "r", encoding="utf-8") as input:
        raw_prices = input.read()[:-1].split("\n\n")
        prices = []

        for raw_price in raw_prices:
            raw_price = raw_price.split("\n")
            m = re.match(r"Button A: X(.+?), Y(.+)", raw_price[0])
            xa, ya = m.groups()

            m = re.match(r"Button B: X(.+?), Y(.+)", raw_price[1])
            xb, yb = m.groups()

            m = re.match(r"Prize: X=(.+?), Y=(.+)", raw_price[2])
            xp, yp = m.groups()

            prices.append(((int(xa), int(ya)), (int(xb), int(yb)), (int(xp), int(yp))))    

    result = compute_total_cost(prices)
    print("[Part1] Result is", result)

    result_2 = compute_total_cost(prices, shifted=True)
    print("[Part2] Result is", result_2)

main()
