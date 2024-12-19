from dataclasses import dataclass, field
from typing import Union


@dataclass
class PatternNode:
    letter: str
    children: dict[str, "PatternNode"] = field(default_factory=dict)
    depth: int = 0

    def is_terminal_node(self):
        return "" in self.children

    def get_or_create_child(self, letter: str) -> "PatternNode":
        if letter not in self.children:
            self.children[letter] = PatternNode(letter=letter, depth=self.depth + 1)
        return self.children[letter]

    def get_child(self, letter: str) -> Union["PatternNode", None]:
        if letter not in self.children:
            return None
        return self.children[letter]

    def __repr__(self) -> str:
        output = self.letter if self.letter != "" else "*"
        for child in self.children.values():
            output += f"\n{4 * self.depth * ' '}- {repr(child)}"

        return output


def build_pattern_tree(patterns: list[str]) -> PatternNode:
    root = PatternNode(letter="")

    for pattern in patterns:
        current_node = root
        for letter in pattern:
            current_node = current_node.get_or_create_child(letter)

        current_node.get_or_create_child("")

    return root

def is_design_possible_slow(design: str, pattern_tree: PatternNode) -> bool:
    nodes_queue = [(design, pattern_tree)]

    while len(nodes_queue) > 0:
        design_to_process, node_to_process = nodes_queue.pop()
        
        if len(design_to_process) == 0:
            if node_to_process.is_terminal_node():
                return True
            continue
        
        letter = design_to_process[0]
        if (next_node := node_to_process.get_child(letter)) is not None:
            nodes_queue.append((design_to_process[1:], next_node))

        if node_to_process.is_terminal_node() and (next_node := pattern_tree.get_child(letter)) is not None:
            nodes_queue.append((design_to_process[1:], next_node))

    return False

def is_design_possible(design: str, patterns: list[str], cache: dict[str, int]) -> bool:
    if len(design) == 0:
        return 1
    
    if design in cache:
        return cache[design]

    result = 0

    for pattern in patterns:
        if design.startswith(pattern):
           result += is_design_possible(design[len(pattern):], patterns, cache)

    cache[design] = result

    return result


def main():
    with open("input.txt", "r", encoding="utf-8") as input:
        raw_patterns, raw_designs = input.read().split("\n\n")

        patterns = raw_patterns.split(", ")
        designs = raw_designs[:-1].split("\n")

    result = 0
    result_2 = 0

    for design in designs:
        count = is_design_possible(design, [pattern for pattern in patterns if pattern in design], {})
        if count:
            result += 1
        result_2 += count

    print("[Part1] Result is", result)
    print("[Part2] Result is", result_2)

main()
