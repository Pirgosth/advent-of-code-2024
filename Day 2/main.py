from lib.algo import parse_file, compute_levels_score

def main():
    with open("input.txt", "r", encoding="utf-8") as file:
        levels = parse_file(file)

    safety_score = compute_levels_score(levels)
    
    print("[Part1] Safety score is", safety_score)

    safety_score_with_dampener = compute_levels_score(levels, True)
    
    print("[Part2] Safety score with dampener is", safety_score_with_dampener)

if __name__ == "__main__":
    main()