from functools import reduce


def generate_next_secret(secret: int) -> int:
    step1 = secret * 64
    secret = (secret ^ step1) % 16777216

    step2 = secret // 32
    secret = (secret ^ step2) % 16777216

    step3 = secret * 2048
    secret = (secret ^ step3) % 16777216

    return secret


def find_sequence_price(
    sequence: tuple[int], price_history: list[int], price_variations: list[int]
) -> int:
    cursor = 0

    for price, variation in zip(price_history[1:], price_variations, strict=True):
        if variation == sequence[cursor]:
            cursor += 1
        else:
            cursor = 0 if variation != sequence[0] else 1

        if cursor == len(sequence):
            return price

    return 0


def test_sequence_over_market(
    sequence: tuple[int],
    prices: list[list[int]],
    prices_variations: list[list[int]],
    variations_sequences: list[set[tuple[int]]],
):
    total_price = 0
    for price_history, price_variations, sequences in zip(
        prices, prices_variations, variations_sequences, strict=True
    ):
        if sequence not in sequences:
            continue
        price = find_sequence_price(sequence, price_history, price_variations)
        total_price += price

    return total_price


def main():
    with open("input.txt", "r", encoding="utf-8") as input:
        seeds = []

        for line in input:
            seeds.append(int(line[:-1]))

        secrets = []

        for seed in seeds:
            secret = [seed]
            for _ in range(2000):
                secret.append(generate_next_secret(secret[-1]))
            secrets.append(secret)

        prices = [
            [int(str(secret_secret)[-1]) for secret_secret in secret]
            for secret in secrets
        ]
        prices_variations = []
        for price_history in prices:
            price_variations = []
            for i in range(len(price_history) - 1):
                price_variations.append(price_history[i + 1] - price_history[i])
            prices_variations.append(price_variations)

        variations_sequences: list[set[tuple[int]]] = []
        for price_variations in prices_variations:
            variation_sequences = set()
            for i in range(len(price_variations) - 3):
                sequence = price_variations[i : i + 4]
                assert len(sequence) == 4
                variation_sequences.add(tuple(price_variations[i : i + 4]))
            variations_sequences.append(variation_sequences)

        sequences = set()
        for variation_sequences in variations_sequences:
            for sequence in variation_sequences:
                sequences.add(sequence)

        total_sequences = len(sequences)

        max_total_price = 0
        better_sequence = None

        for i, sequence in enumerate(sequences):
            total_price = test_sequence_over_market(
                sequence, prices, prices_variations, variations_sequences
            )
            if total_price > max_total_price:
                max_total_price = total_price
                better_sequence = sequence
            print(f"{i + 1}/{total_sequences}")

        result = reduce(lambda x, y: x + y[-1], secrets, 0)
        print("[Part1] Result is:", result, better_sequence)

        print("[Part2] Result is:", max_total_price)


main()
