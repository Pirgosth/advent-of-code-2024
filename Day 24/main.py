import itertools
import re


def compute_gate(
    a: str,
    op: str,
    b: str,
    result_register: str,
    registers: dict[str, int],
    gates: dict[str, tuple[str, str, str]],
):

    def _compute_gate(_a: str, _op: str, _b: str, _result_register):
        # print(_a, _op, _b)

        if _result_register not in registers:
            if _a not in registers:
                a_gate = gates[_a]
                _compute_gate(a_gate[0], a_gate[1], a_gate[2], _a)

            if _b not in registers:
                b_gate = gates[_b]
                _compute_gate(b_gate[0], b_gate[1], b_gate[2], _b)

            reg_a, reg_b = registers[_a], registers[_b]
            if _op == "AND":
                registers[_result_register] = reg_a & reg_b
            elif _op == "OR":
                registers[_result_register] = reg_a | reg_b
            else:  # XOR
                registers[_result_register] = reg_a ^ reg_b

        return registers[_result_register]

    _compute_gate(a, op, b, result_register)


def compute(registers: dict[str, int], gates: dict[str, tuple[str, str, str]]):
    for result_register, (a, op, b) in gates.items():
        compute_gate(a, op, b, result_register, registers, gates)


def get_number(registers: dict[str, int], register_prefix = "z") -> int:
    sub_registers = {k: v for k, v in registers.items() if k.startswith(register_prefix)}
    sub_registers = dict(sorted(sub_registers.items(), key=lambda x: int(x[0][1:]), reverse=True))
    
    result = 0
    for bit in sub_registers.values():
        result = result << 1
        result += bit

    return result

def find_gate_by_value(gates: dict[str, tuple[str, str, str]], a: str, b: str, op: str) -> str | None:
    for k, v in gates.items():
        if v == (a, op, b) or v == (b, op, a):
            return k
        
    return None

def repair_program(gates: dict[str, tuple[str, str, str]]):

    z_gate = gates["z00"]
    carry = find_gate_by_value(gates, "x00", "y00", "AND")
    print(z_gate, carry)

    assert z_gate == ('y00', 'XOR', 'x00') or z_gate == ('x00', 'XOR', 'y00')

    for k in range(1, 46):
        z_gate = gates[f"z{k:02d}"]
        print(z_gate)
        # carry = 

        break

def main():
    with open("input.txt", "r", encoding="utf-8") as input:
        raw_registers, raw_gates = input.read().split("\n\n")

        registers: dict[str, int] = {}

        for register in raw_registers.split("\n"):
            registers[register[:3]] = int(register[5:])

        gates = {}

        for gate in raw_gates[:-1].split("\n"):
            m = re.match(r"(.+?) (.+?) (.+?) -> (.+)", gate)
            a, op, b, res = m.groups()

            gates[res] = (a, op, b)

    compute(registers, gates)

    x = get_number(registers, register_prefix="x")
    y = get_number(registers, register_prefix="y")
    z = get_number(registers)

    print("X", bin(x))
    print("Y", bin(y))
    print("X + Y", bin(x + y))
    print("Z", bin(z))

    repair_program(gates)

main()
