from lib.algo import (
    parse_file, is_level_safe, compute_levels_score
)

with open("tests/test_input.txt", "r", encoding="utf-8") as file:
    levels = parse_file(file)

    assert len(levels) == 10
    for level in levels[:-1]:
        assert len(level) == 5
    
    assert is_level_safe(levels[0])
    for i in range(1, 4):
        assert not is_level_safe(levels[i]), i

    assert is_level_safe(levels[5])
    assert not is_level_safe(levels[6])
    assert not is_level_safe(levels[7])
    assert not is_level_safe(levels[8])
    
    assert compute_levels_score(levels) == 2

    assert is_level_safe(levels[0], dampener=True)

    for i in range(1, 3):
        assert not is_level_safe(levels[i], True), i

    for i in range(3, 10):
        assert is_level_safe(levels[i], True), i

    assert compute_levels_score(levels, dampener=True) == 8
