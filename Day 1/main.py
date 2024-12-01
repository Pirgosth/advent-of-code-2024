from lib.algo import parse_file, sort_list, compute_distances_between_lists, compute_total_distance, compute_similarity_score

def main():
    with open("input.txt", "r", encoding="utf-8") as file:
        list_a, list_b = parse_file(file)

    sorted_a, sorted_b = sort_list(list_a), sort_list(list_b)
    distances = compute_distances_between_lists(sorted_a, sorted_b)

    total_distance = compute_total_distance(distances)
    print("[Part1] Total distance is", total_distance)
    
    similarity_score = compute_similarity_score(list_a, list_b)
    print("[Part2] Similarity score is", similarity_score)

if __name__ == "__main__":
    main()