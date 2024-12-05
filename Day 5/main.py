def is_update_ordered(update: list[str], rules: dict[str, list[str]]):
    to_check = []
    valid = True

    for x in reversed(update):
            if len(to_check) == 0 and len(update) >= 2:
                y = update[-2]
                rule = rules[x] if x in rules else []
                if y in rule:
                    valid = False
                    break
            to_check.append(x)
            for t in to_check:
                if t in rules and x in rules[t]:
                    valid = False
                    to_check = []
                    break
            if not valid:
                break
        
    return valid

def min_rules(rules: dict[str, list[str]]):
    return min(rules.items(), key=lambda x: len(x[1]))

def max_rules(rules: dict[str, list[str]]):
    return max(rules.items(), key=lambda x: len(x[1]))

def compute_path(update: list[str], rules: dict[str, list[str]]):
    update_rules = {x:[] for x in update}
            
    for x in update:
        if x in rules:
            update_rules[x] = [v for v in rules[x] if v in update]
    
    for k, rule in rules.items():
        for x in update:
            if x in rule:
                update_rules[k] = [v for v in rule if v in update]
                break
    
    start = {max_rules(update_rules)[0]: (max_rules(update_rules)[1], 0)}

    def compute_recursive_path(node: dict, history: list[str]):
        for (k,(v,_)) in node.items():
            sub_path = {}
            for x in v:
                if x in update_rules and x not in history:
                    sub_path[x] = (update_rules[x], 0)
            node[k] = compute_recursive_path(sub_path, history + [v])

        return (node, (max(node.items(), key=lambda x: x[1][1])[1][1] if len(node.keys()) > 0 else -1) + 1)

    return compute_recursive_path(start, [max_rules(update_rules)[0]])

def get_longest_path(graph):
    node = max(graph.items(), key=lambda x: x[1][1])
    length = node[1][1]
    
    path = [node[0]]
    node = node[1][0]

    while length > 0:
        node = max(node.items(), key=lambda x: x[1][1])
        length = node[1][1]
        path.append(node[0])

        node = node[1][0]
    
    return path
        

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
            to_check = []
            valid = True

            for x in reversed(update):
                if len(to_check) == 0 and len(update) >= 2:
                    y = update[-2]
                    rule = rules[x] if x in rules else []
                    if y in rule:
                        valid = False
                        break
                to_check.append(x)
                for t in to_check:
                    if t in rules and x in rules[t]:
                        valid = False
                        to_check = []
                        break
                if not valid:
                    break
            
            if valid:
                result += int(update[int(len(update) / 2)])
            else:
                updates_to_reorder.append(update)

        print("[Part1] Result is", result)

        result_2 = 0

        for update in updates_to_reorder:
            graph,length = compute_path(update, rules)
            print("Length:", length)
            path = get_longest_path(graph)
            result_2 += int(path[int(len(path) / 2)])
        
        print("[Part2] Result is", result_2)

main()