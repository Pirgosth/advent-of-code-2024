from lib.algo import (
    parse_file, sort_list, compute_distance, compute_distances_between_lists, 
    compute_total_distance, count_instances_dict, get_number_multiplier,
    compute_similarity_score
)

with open("tests/test_input.txt", "r", encoding="utf-8") as file:
    list_a, list_b = parse_file(file)

    assert len(list_a) == len(list_b) == 3
    assert list_a == [1, 2, 3]
    assert list_b == [6, 5, 4]

    assert sort_list(list_a) == [1, 2, 3]
    assert sort_list(list_b) == [4, 5, 6]

    assert compute_distance(1, 1) == 0
    assert compute_distance(1, 3) == 2
    assert compute_distance(3, 1) == 2
    assert compute_distance(10, 3) == 7

    lists_distances = compute_distances_between_lists(sort_list(list_a), sort_list(list_b))

    assert lists_distances == [3, 3, 3]

    assert compute_total_distance([]) == 0
    assert compute_total_distance([1, 4, 9]) == 14
    assert compute_total_distance(lists_distances) == 9

    assert count_instances_dict([1, 1, 1, 4, 6, 9, 4, 6]) == {1: 3, 4: 2, 6: 2, 9: 1}

    assert get_number_multiplier({1: 3, 4: 2, 6: 2, 9: 1}, 1) == 3
    assert get_number_multiplier({1: 3, 4: 2, 6: 2, 9: 1}, 3) == 0
    assert get_number_multiplier({1: 3, 4: 2, 6: 2, 9: 1}, 4) == 2
    assert get_number_multiplier({1: 3, 4: 2, 6: 2, 9: 1}, 6) == 2
    assert get_number_multiplier({1: 3, 4: 2, 6: 2, 9: 1}, 9) == 1

    assert compute_similarity_score(list_a, list_b) == 0
    assert compute_similarity_score([1, 2, 3], [1, 1, 3, 4]) == 5
    assert compute_similarity_score([1, 1, 3, 4], [1, 2, 3]) == 5
