import re

def read_next_instruction(registers: dict[str, int], program: list[int]) -> tuple[tuple[int, int], bool]:
    index = registers["I"]
    if index + 1 >= len(program):
        return ((-1, -1), False)
    
    return (program[index], program[index + 1]), True

def compute_combo_operand(literal: int, registers: dict[str, int]) -> int:
    combo_register_mapping = {
        4: "A",
        5: "B",
        6: "C"
    }
    
    if literal in range(0, 4):
        return literal
    elif literal in range(4, 7):
        return registers[combo_register_mapping[literal]]
    
    raise ValueError(f"Combo must be between 0 and 6 inclusive. Provided combo: {literal}")

def adv_opcode(registers: dict[str, int], literal: int):
    numerator = registers["A"]
    denominator = 2 ** (compute_combo_operand(literal, registers))

    registers["A"] = numerator // denominator
    registers["I"] += 2

def bxl_opcode(registers: dict[str, int], literal: int):
    registers["B"] = registers["B"] ^ literal
    registers["I"] += 2

def bst_opcode(registers: dict[str, int], literal: int):
    registers["B"] = compute_combo_operand(literal, registers) % 8
    registers["I"] += 2

def jnz_opcode(registers: dict[str, int], literal: int):
    if registers["A"] == 0:
        registers["I"] += 2
        return
    
    registers["I"] = literal

def bxc_opcode(registers: dict[str, int], literal: int):
    registers["B"] = registers["B"] ^ registers["C"]
    registers["I"] += 2

def out_opcode(registers: dict[str, int], literal: int):
    registers["O"] = compute_combo_operand(literal, registers) % 8
    registers["I"] += 2

def bdv_opcode(registers: dict[str, int], literal: int):
    numerator = registers["A"]
    denominator = 2 ** (compute_combo_operand(literal, registers))

    registers["B"] = numerator // denominator
    registers["I"] += 2

def cdv_opcode(registers: dict[str, int], literal: int):
    numerator = registers["A"]
    denominator = 2 ** (compute_combo_operand(literal, registers))

    registers["C"] = numerator // denominator
    registers["I"] += 2

instructions = {
    0: adv_opcode,
    1: bxl_opcode,
    2: bst_opcode,
    3: jnz_opcode,
    4: bxc_opcode,
    5: out_opcode,
    6: bdv_opcode,
    7: cdv_opcode
}

def test(x: int) -> int:
    return (((x % 8) ^ 4) ^ (x // (2 ** ((x % 8) ^ 4))) ^ 4) % 8

def test_2(x: int) -> int:
    return (((x % 8) ^ 4) ^ (x >> ((x % 8) ^ 4)) ^ 4) % 8

def find_identity_seed(program: list[str]) -> int:
    processing_queue = [([], 0, program)]
    results = []

    while len(processing_queue) > 0:
        subseed, accumulator, program_head = processing_queue.pop()

        if len(program_head) <= 0:
            results.append((subseed, int("".join(subseed), 8)))
            continue

        for k in range(8):
            if test_2(8 * accumulator + k) == program_head[-1]:
                next_seed = list(subseed)
                next_seed.append(str(k))
                next_accumulator = 8 * accumulator + k
                next_remaining_program = list(program_head)[:-1]
                processing_queue.append((next_seed, next_accumulator, next_remaining_program))

    minimal_seed = min([r for r in results if r[0][0] != '0'], key=lambda x:x[1])
    return minimal_seed[1]

def main():
    with open("input.txt", "r", encoding="utf-8") as input:
        raw_registers, raw_program = input.read().split("\n\n")

        m = re.match(
            "Register A: (?P<A>.+?)\nRegister B: (?P<B>.+?)\nRegister C: (?P<C>.+)",
            raw_registers,
        )
        registers = {k: int(v) for k, v in m.groupdict().items()}
        
        registers["I"] = 0
        registers["O"] = -1
        
        print(registers)

        program = [int(op) for op in raw_program[9: -1].split(",")]

        (opcode, combo), is_running = read_next_instruction(registers, program)
        output = []

        while is_running:
            instruction = instructions[opcode]
            instruction(registers, combo)

            if registers["O"] >= 0:
                print("A:", oct(registers["A"]), "B:", oct(registers["B"]), registers)
                output.append(str(registers["O"]))
                registers["O"] = -1

            (opcode, combo), is_running = read_next_instruction(registers, program)

        print("[Part1] Output is:", ",".join(output))

        identity_seed = find_identity_seed(program)
        print("[Part2] Seed is:", identity_seed)


main()
