def get_coordinates(c: str, pad: list[str], w, h) -> tuple[int, int]:
    for j in range(h):
        for i in range(w):
            if pad[j * w + i] == c:
                return (i, j)

    return (-1, -1)


def get_prior_move(moving_vector: tuple[int, int]) -> tuple[int, int]:
    if moving_vector[0] < 0:
        return moving_vector[0], 0
    elif moving_vector[1] > 0:
        return 0, moving_vector[1]
    elif moving_vector[1] < 0:
        return 0, moving_vector[1]
    elif moving_vector[0] > 0:
        return moving_vector[0], 0
    else:
        return 0, 0


def get_sequence(
    from_position: tuple[int, int],
    to_position: tuple[int, int],
    pad: list[str],
    w: int,
    h: int,
) -> str:
    # order = ['<', 'v', '^', '>']

    moving_vector = to_position[0] - from_position[0], to_position[1] - from_position[1]

    sequence = ""

    first_move = get_prior_move(moving_vector)
    gap_coordinates = get_coordinates("", pad, w, h)

    is_on_gap = (
        from_position[0] + first_move[0],
        from_position[1] + first_move[1],
    ) == gap_coordinates

    if moving_vector[0] < 0:
        sequence += "<" * abs(moving_vector[0])

    if moving_vector[1] > 0:
        sequence += "v" * moving_vector[1]

    if moving_vector[1] < 0:
        sequence += "^" * abs(moving_vector[1])

    if moving_vector[0] > 0:
        sequence += ">" * moving_vector[0]

    if is_on_gap:
        sequence = sequence[::-1]

    return sequence


def generate_shortest_digicode_sequence(code: str) -> list[str]:
    digicode = ["7", "8", "9", "4", "5", "6", "1", "2", "3", "", "0", "A"]
    w, h = 3, 4

    position = get_coordinates("A", digicode, w, h)

    sequence = ""

    for c in code:
        next_position = get_coordinates(c, digicode, w, h)
        sequence += get_sequence(position, next_position, digicode, w, h)
        sequence += "A"
        position = next_position

    return sequence


def generate_shortest_directionnal_sequence(initial_sequence: str) -> list[str]:
    pad = ["", "^", "A", "<", "v", ">"]
    w, h = 3, 2

    position = get_coordinates("A", pad, w, h)

    sequence = ""

    for c in initial_sequence:
        next_position = get_coordinates(c, pad, w, h)
        sequence += get_sequence(position, next_position, pad, w, h)
        sequence += "A"
        position = next_position

    return sequence


def get_shortest_directionnal_sequence_size(
    initial_sequence: str, number_of_robots: int
) -> int:

    pad = ["", "^", "A", "<", "v", ">"]
    w, h = 3, 2
    cache = {}

    def _get_shortest_directionnal_sequence_size(sequence: str, depth: int) -> int:
        if depth == number_of_robots:
            return len(sequence)

        result = 0

        for i in range(len(sequence)):
            from_position = get_coordinates(
                (sequence[i - 1] if i > 0 else "A"), pad, w, h
            )
            to_position = get_coordinates(sequence[i], pad, w, h)

            if (from_position, to_position, depth) not in cache:
                cache[(from_position, to_position, depth)] = (
                    _get_shortest_directionnal_sequence_size(
                        get_sequence(from_position, to_position, pad, w, h) + "A",
                        depth + 1,
                    )
                )

            result += cache[(from_position, to_position, depth)]

        return result

    return _get_shortest_directionnal_sequence_size(initial_sequence, 0)


def code_to_int(code: str) -> int:
    return int(code[:-1])


def main():
    with open("input.txt", "r", encoding="utf-8") as input:
        codes = []

        for line in input:
            codes.append(line[:-1])

    print(codes)

    result = 0
    result_2 = 0

    for code in codes:
        shortest_digicode = generate_shortest_digicode_sequence(code)
        shortest_directionnal_sequence_size = get_shortest_directionnal_sequence_size(
            shortest_digicode, 2
        )
        shortest_directionnal_sequence_size_2 = get_shortest_directionnal_sequence_size(
            shortest_digicode, 25
        )

        result += code_to_int(code) * shortest_directionnal_sequence_size
        result_2 += code_to_int(code) * shortest_directionnal_sequence_size_2

        print(
            code,
            shortest_directionnal_sequence_size,
            shortest_directionnal_sequence_size_2,
        )

    print("[Part1] Result is:", result)
    print("[Part2] Result is:", result_2)


main()
