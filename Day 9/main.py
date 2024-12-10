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

def parse_disk_map_2(disk_map: str) -> list[int]:
    block_id = 0
    disk = []
    is_free_space = False

    for block in disk_map:
        if not is_free_space:
            disk.append((block_id, int(block)))
        else:
            disk.append((-1, int(block)))

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

def find_free_space_block(disk: list[int], size: int, block_cursor: int) -> int:
    cursor = 0

    def _scan_free_space_block() -> int:
        _cursor = cursor
        _size = 0
        while _cursor < len(disk) and disk[_cursor] == -1:
            _cursor += 1
            _size += 1

        return _size

    while cursor < len(disk) and cursor < block_cursor:
        if (free_space_block_size := _scan_free_space_block()) >= size:
            return cursor
        else:
            cursor += free_space_block_size

        while cursor < len(disk) and disk[cursor] != -1:
            cursor += 1
        

    return -1

def compress_free_space_2(disk: list[int]) -> list[int]:
        cursor = len(disk) - 1

        while cursor >= 0:
            block, cursor = get_next_block_and_cursor(cursor, disk)
            print(block, cursor)

            if block is None:
                break

            free_space_block_cursor = find_free_space_block(disk, block[1], cursor + 1)

            if free_space_block_cursor == -1:
                continue

            for i in range(block[1]):
                disk[free_space_block_cursor + i] = block[0]
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

    compress_free_space_2(disk_2)

    disk_checksum_2 = compute_checksum(disk_2)
    print("[Part2] Checksum is", disk_checksum_2)

main()