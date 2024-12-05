from functools import cmp_to_key

def sort_update(update: list[str], rules: dict[str, list[str]]):
    def cmp_fun(a: str, b: str):
        if a in rules and b in rules[a]:
            return -1
        return 1
    
    ordered = sorted(update, key=cmp_to_key(cmp_fun))
    return ordered

def is_update_ordered(update: list[str], rules: dict[str, list[str]]):
    sorted_update = sort_update(update, rules)

    return sorted_update == update

def main():
    with open("input.txt", "r", encoding="utf-8") as input:
        rules = {}
        while (line := input.readline()) != "\n":
            rule = line[:-1].split("|")
            if not rule[0] in rules:
                rules[rule[0]] = []

            rules[rule[0]].append(rule[1])

        updates = []
        while line := input.readline():
            updates.append(line[:-1].split(","))

        result = 0

        updates_to_reorder = []

        for update in updates:
            if is_update_ordered(update, rules):
                result += int(update[int(len(update) / 2)])
            else:
                updates_to_reorder.append(update)

        print("[Part1] Result is", result)

        result_2 = 0

        for update in updates_to_reorder:
            ordered_update = sort_update(update, rules)
            result_2 += int(ordered_update[int(len(ordered_update) / 2)])
            if not is_update_ordered(ordered_update, rules):
                print("ERROR:", ordered_update)
        
        print("[Part2] Result is", result_2)

main()