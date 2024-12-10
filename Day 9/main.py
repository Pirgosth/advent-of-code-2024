import bisect

def parse_disk_map(disk_map: str) -> list[int]:
    block_id = 0
    disk = []
    is_free_space = False

    for block in disk_map:
        if not is_free_space:
            disk += [block_id] * int(block)
        else:
            disk += [-1] * int(block)

        if not is_free_space:
            block_id += 1
        is_free_space = not is_free_space
    
    return disk

def seek_to_free_space(cursor: int, disk: list[int]) -> int:
    while cursor < len(disk) and disk[cursor] != -1:
        cursor += 1

    return cursor if cursor < len(disk) else -1

def compress_free_space(disk: list[int]) -> list[int]:
    cursor = seek_to_free_space(0, disk)
    
    for reverse_cursor, block_id in reversed(list(enumerate(disk))):
        if reverse_cursor <= cursor or cursor == -1:
            break

        if block_id != -1:
            disk[cursor], disk[reverse_cursor] = block_id, disk[cursor]
            cursor = seek_to_free_space(cursor + 1, disk)

def get_next_block_and_cursor(cursor: int, disk: list[int]) -> tuple[int, int] | None:
    while disk[cursor] == -1:
        cursor -= 1
    
    if cursor < 0:
        return None, -1

    block_id = disk[cursor]
    size = 0

    while cursor >= 0 and disk[cursor] == block_id:
        cursor -= 1
        size += 1

    return (block_id, size), cursor

def find_right_free_space_block(disk: list[int], cursor: int) -> tuple[int, int]:
    while cursor >= 0 and disk[cursor] != -1:
        cursor -= 1

    if cursor < 0:
        return -1, -1

    size = 0

    while cursor >= 0 and disk[cursor] == -1:
        cursor -= 1
        size += 1
        

    return size, cursor

def memory_scan(disk: list[int]) -> dict[list[int]]:
    free_space_mapping: dict[list[int]] = {}
    
    cursor = len(disk) - 1
    
    while cursor >= 0:
        block_size, cursor = find_right_free_space_block(disk, cursor)
        if block_size == -1:
            break
            
        if block_size not in free_space_mapping:
            free_space_mapping[block_size] = []

        free_space_mapping[block_size].append(cursor + 1)

    return free_space_mapping
    
def get_free_space_block(free_space_mapping: dict[list[int]], block_size: int) -> tuple[int, int]:
    compatible_and_available_size = [size for size in free_space_mapping.keys() if size >= block_size]
    
    if len(compatible_and_available_size) <= 0:
        return -1, -1
    
    min_size = compatible_and_available_size[0]
    for size in compatible_and_available_size:
        if free_space_mapping[size][-1] < free_space_mapping[min_size][-1]:
            min_size = size

    free_space_index = free_space_mapping[min_size].pop()
    if len(free_space_mapping[min_size]) <= 0:
        del free_space_mapping[min_size]

    # Update free_space_mapping cache to keep track of remaining free space
    remaining_space = min_size - block_size
    if remaining_space != 0:
        if remaining_space not in free_space_mapping:
            free_space_mapping[remaining_space] = []

        bisect.insort(free_space_mapping[remaining_space], free_space_index + block_size, key=lambda x: x * -1)

    return (free_space_index, min_size)

def compress_free_space_2(disk: list[int], free_space_mapping: dict[list[int]]):
    cursor = len(disk) - 1

    while cursor >= 0:
        block, cursor = get_next_block_and_cursor(cursor, disk)
        free_space_index, _ = get_free_space_block(free_space_mapping, block[1])

        if free_space_index == -1 or free_space_index >= cursor + 1:
            continue

        for i in range(block[1]):
            disk[free_space_index + i] = block[0]
            disk[cursor + i + 1] = -1


def compute_checksum(disk: list[int]) -> int:
    checksum = 0
    for index, block_id in enumerate(disk):
        if block_id == -1:
            continue

        checksum += index * block_id

    return checksum

def main():
    with open("input.txt", "r", encoding="utf-8") as input:
        disk_map = input.read()[:-1]

    disk = parse_disk_map(disk_map)
    compress_free_space(disk)
    disk_checksum = compute_checksum(disk)
    print("[Part1] Checksum is", disk_checksum)

    disk_2 = parse_disk_map(disk_map)
    import time

    start_time = time.time()
    free_space_mapping = memory_scan(disk_2)

    compress_free_space_2(disk_2, free_space_mapping)
    print("--- %s ms ---" % ((time.time() - start_time) * 1000))

    disk_checksum_2 = compute_checksum(disk_2)
    print("[Part2] Checksum is", disk_checksum_2)

main()