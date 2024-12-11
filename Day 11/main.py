from functools import reduce


def cut_in_half(n: int) -> tuple[int, int]:
    str_n = str(n)
    a, b = str_n[:len(str_n) // 2], str_n[len(str_n) // 2:]
    return int(a), int(b)

def process(compressed_seed: dict[int, int]) -> dict[int, int]:
    next_compressed_seed = {}

    for n, c in compressed_seed.items():
        if n == 0:
            if 1 not in next_compressed_seed:
                next_compressed_seed[1] = 0

            next_compressed_seed[1] += c
        
        elif len(str(n)) % 2 == 0:
            a, b = cut_in_half(n)
            if a not in next_compressed_seed:
                next_compressed_seed[a] = 0

            if b not in next_compressed_seed:
                next_compressed_seed[b] = 0

            next_compressed_seed[a] += c
            next_compressed_seed[b] += c
        
        else:
            if (n * 2024) not in next_compressed_seed:
                next_compressed_seed[n * 2024] = 0
            next_compressed_seed[n * 2024] += c

    return next_compressed_seed


def main():
    with open("input.txt", "r", encoding="utf-8") as input:
        seed = [int(c) for c in input.read()[:-1].split(" ")]
    
    compressed_seed = {}
    for n in seed:
        if n not in compressed_seed:
            compressed_seed[n] = 0
        compressed_seed[n] += 1

    for i in range(25):
        compressed_seed = process(compressed_seed)

    result = 0
    for c in compressed_seed.values():
        result += c

    print("[Part1] Result is", result)

    
    for i in range(50):
        compressed_seed = process(compressed_seed)

    result_2 = 0
    for c in compressed_seed.values():
        result_2 += c

    print("[Part2] Result is", result_2)

main()