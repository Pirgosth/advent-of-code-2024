import re

def mul_parser(program: str) -> int:
    i = -1
    result = 0

    while i < len(program) - 1:
        i += 1
        if program[i] == "m":
            m = re.match(r"mul\(([0-9]{1,3}),([0-9]{1,3})\)", program[i:i+12])
            if m is not None:
                i += m.end() - 1
                a, b = m.groups()
                result += int(a) * int(b)
                continue

        
    return result

def mul_parser_2(program: str) -> int:
    i = -1
    is_enabled = True
    result = 0

    while i < len(program) - 1:
        i += 1
        if is_enabled and program[i] == "m":
            m = re.match(r"mul\(([0-9]{1,3}),([0-9]{1,3})\)", program[i:i+12])
            if m is not None:
                i += m.end() - 1
                a, b = m.groups()
                result += int(a) * int(b)
                continue
        
        if program[i] == "d":
            if program[i:i+7] == "don't()":
                is_enabled = False
                i += 6
            elif program[i:i+4] == "do()":
                i += 3
                is_enabled = True

        
    return result
            

with open("input.txt", "r", encoding="utf-8") as input:
    program = input.read()

    result = mul_parser(program)

    print("[Part1] Total is", result)

    result_2 = mul_parser_2(program)

    print("[Part1] Total is", result_2)
