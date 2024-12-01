from functools import reduce

def parse_file(file) -> tuple[list[int], list[int]]:
    list_a, list_b = [], []
    for line in file:
        line = line[:-1]
        number_a, number_b = line.split("   ")
        list_a.append(int(number_a))
        list_b.append(int(number_b))

    return list_a, list_b

def sort_list(list_to_sort: list[int]) -> list[int]:
    return sorted(list_to_sort)

def compute_distance(a: int, b: int) -> int:
    return abs(b - a)

def compute_distances_between_lists(sorted_list_a: list[int], sorted_list_b: list[int]) -> list[int]:
    assert len(sorted_list_a) == len(sorted_list_b), "Lists size mismatch !"

    distances: list[int] = []

    for a, b in zip(sorted_list_a, sorted_list_b):
        distances.append(compute_distance(a, b))

    return distances

def compute_total_distance(distances_list: list[int]) -> int:
    return reduce(lambda a, b: a + b, distances_list, 0)

def count_instances_dict(list_to_count: list[int]) -> dict[int, int]:
    counts: dict[int, int] = {}

    for a in list_to_count:
        if a not in counts:
            counts[a] = 0

        counts[a] += 1

    return counts

def get_number_multiplier(counts_dict: dict[int, int], number: int) -> int:
    if number not in counts_dict:
        return 0
    
    return counts_dict[number]

def compute_similarity_score(list_a: list[int], list_b: list[int]) -> int:
    counts = count_instances_dict(list_b)

    similarity_score = 0

    for a in list_a:
        similarity_score += a * get_number_multiplier(counts, a)

    return similarity_score
