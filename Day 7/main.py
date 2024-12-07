
def test_equation(equation: tuple[int, list[int]]):
    def _test_equation(_equation):
        expected_result, operands = _equation

        if len(operands) == 1:
            return (expected_result == operands[0], [])

        reverse_head = operands[-1]

        tail = _test_equation((expected_result - reverse_head, operands[:-1]))

        if tail[0]:
            return (True, tail[1] + ["+"])
        
        tail = _test_equation((expected_result // reverse_head, operands[:-1]))

        if tail[0] and expected_result % reverse_head == 0:
            return (True, tail[1] + ["*"])
        
        return (False, None)
    
    result = _test_equation(equation)
    return result[0], result[1] if result[1] is not None else None
        

def test_result(equation, operators):
    expected_result, operands = equation

    result = operands[0]

    for i in range(len(operands) - 1):
        op = operands[i+1]
        if operators[i] == "+":
            result += op
        elif operators[i] == "*":
            result *= op
        else:
            result = int(str(result) + str(op))
    
    return result == expected_result

def concat(a: int, b: int) -> int:
    return int(str(a) + str(b))

def unconcat(a: int, b: int) -> int:
    str_a, str_b = str(a), str(b)
    
    return int(str_b[:-len(str_a)])

def test_equation_2(equation: tuple[int, list[int]]):
    def _test_equation(_equation):
        expected_result, operands = _equation

        if len(operands) == 1:
            return (expected_result == operands[0], [])

        reverse_head = operands[-1]

        tail = _test_equation((expected_result - reverse_head, operands[:-1]))

        if tail[0]:
            return (True, tail[1] + ["+"])
        
        if expected_result % reverse_head == 0:
            tail = _test_equation((expected_result // reverse_head, operands[:-1]))
            if tail[0]:
                return (True, tail[1] + ["*"])
        
        if str(expected_result).endswith(str(reverse_head)) and abs(expected_result) != reverse_head:
            tail = _test_equation((unconcat(reverse_head, expected_result), operands[:-1]))

            if tail[0]:
                return (True, tail[1] + ["||"])
        
        return (False, None)
    
    return _test_equation(equation)

def main():
    with open("input.txt", "r", encoding="utf-8") as input:
        equations = []
        for line in input:
            result, operands = line[:-1].split(":")
            result = int(result)
            operands = [int(op) for op in operands.strip().split(" ")]
            equations.append((result, operands))

    result = 0

    for equation in equations:
        valid_result = test_equation(equation)
        if valid_result[0]:
            is_equation_really_valid = test_result(equation, valid_result[1])
            if not is_equation_really_valid:
                print(equation, valid_result[1], is_equation_really_valid)
            result += equation[0]

    print("[Part1] Result is", result)

    result_2 = 0

    for equation in equations:
        valid_result = test_equation_2(equation)
        if valid_result[0]:
            is_equation_really_valid = test_result(equation, valid_result[1])
            if not is_equation_really_valid:
                print(equation, valid_result[1], is_equation_really_valid)
            result_2 += equation[0]

    print("[Part2] Result is", result_2)

main()