
def get_coordinates(c: str, pad: list[str], w, h) -> tuple[int, int]:
    for j in range(h):
        for i in range(w):
            if pad[j * w + i] == c:
                return (i, j)
            
    return (-1, -1)

def code_to_directionnal_sequence(code: str) -> list[str]:
    digicode = ['7', '8', '9', '4', '5', '6', '1', '2', '3', '', '0', 'A']
    w, h = 3, 4

    position = get_coordinates('A', digicode, w, h)
    sequence = ""
    
    for c in code:
        coords = get_coordinates(code, digicode, w, h)

        direction = coords[0] - position[0], coords[1] - position[1]

        if direction[0] != 0:
            sequence += ('>' if direction[0] > 0 else '<') * abs(direction[0])

        if direction[1] != 0:
            sequence += ('v' if direction[1] > 0 else '^') * abs(direction[1])

        sequence += 'A'
        position = coords

    return sequence

def get_shortest_sequences(from_sequence: str, position: tuple[int, int]) -> list[str]:
    digicode = ['7', '8', '9', '4', '5', '6', '1', '2', '3', '', '0', 'A']
    w, h = 3, 4

    if len(from_sequence) == 1:
        char_to_directionnal_sequences(from_sequence)

def manhattan_distance(a: tuple[int, int], b: tuple[int, int]):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_all_paths_possibles(from_position: tuple[int, int], to_position: tuple[int, int], pad: list[str], w: int, h: int) -> list[list[tuple[int, int]]]:

    if from_position == to_position:
        return []
    
    distance = manhattan_distance(from_position, to_position)

    paths = []

    for j in range(h):
        for i in range(w):
            if pad[j * w + i] != '' and manhattan_distance((i, j), from_position) == 1 and manhattan_distance((i, j), to_position) == distance - 1:
                paths.append([[(i, j)] + path for path in get_all_paths_possibles((i, j), to_position, pad, w, h)])

    return paths

def char_to_directionnal_sequences(character: str, pad: list[str], w: int, h: int) -> list[str]:
    position = get_coordinates('A', pad, w, h)
    sequence = ""
    
    coords = get_coordinates(character, pad, w, h)

    get_all_paths_possibles(coords, )

    return

    direction = coords[0] - position[0], coords[1] - position[1]

    if direction[0] != 0:
        sequence += ('>' if direction[0] > 0 else '<') * abs(direction[0])

    if direction[1] != 0:
        sequence += ('v' if direction[1] > 0 else '^') * abs(direction[1])

    sequence += 'A'
    position = coords

    return sequence

def main():
    with open("test.txt", "r", encoding="utf-8") as input:
        codes = []

        for line in input:
            codes.append(line[:-1])

    print(codes)

    digicode = ['7', '8', '9', '4', '5', '6', '1', '2', '3', '', '0', 'A']
    w, h = 3, 4

    a = get_coordinates('A', digicode, w, h)
    nine = get_coordinates('9', digicode, w, h)

    print(get_all_paths_possibles(a, nine, digicode, w, h))

    # for code in codes:
    #     print(code)
    #     sequence = code_to_directionnal_sequence(code)
    #     print(sequence)
    #     sequence_sequence = directionnal_sequence_to_directionnal_sequence(sequence)
    #     print(sequence_sequence)
    #     sequence_sequence_sequence = directionnal_sequence_to_directionnal_sequence(sequence_sequence)
    #     print(sequence_sequence_sequence)
    #     print(len(sequence_sequence_sequence))

main()