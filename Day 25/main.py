def schematic_to_heights(schemtatic: list[str], is_key: bool = False) -> list[int]:
    heights = [0] * len(schemtatic[0])
    
    schemtatic = schemtatic[:-1] if is_key else schemtatic[1:]

    for row in schemtatic:
        for i in range(len(heights)):
            if row[i] == "#":
                heights[i] += 1

    return heights


def test_key_for_lock(key: list[int], lock: list[int]) -> bool:
    for k, l in zip(key, lock):
        if k + l > 5:
            return False

    return True


def compute_keys_and_locks_combinaisons(
    locks: list[list[int]], keys: list[list[int]]
) -> int:
    count = 0

    for key in keys:
        for lock in locks:
            if test_key_for_lock(key, lock):
                count += 1

    return count


def main():
    with open("input.txt", "r", encoding="utf-8") as input:
        raw_input = input.read()[:-1].split("\n\n")

        locks, keys = [], []

        for schematic in raw_input:
            if schematic[:5] == "#####":
                locks.append(schematic_to_heights(schematic.split("\n")))
            else:
                keys.append(schematic_to_heights(schematic.split("\n"), is_key=True))

    result = compute_keys_and_locks_combinaisons(locks, keys)
    print("[Part1] Result is", result)


main()
