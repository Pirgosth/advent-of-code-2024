def compute_computer_graph(connections: list[tuple[str, str]]) -> dict[str, set[str]]:
    graph: dict[str, set[str]] = {}

    for a, b in connections:
        if a not in graph:
            graph[a] = set()
        if b not in graph:
            graph[b] = set()

        graph[a].add(b)
        graph[b].add(a)

    return graph


def is_clique(store: list[str], length: int, graph: dict[str, set[str]]) -> bool:
    # Triangular iteration to avoid recomputing of symmetrical properties
    for i in range(1, length):
        for j in range(i + 1, length):
            # No connection between two computers
            # print(store[j], store[i])
            if store[j] not in graph[store[i]]:
                return False

    return True


def get_cliques(
    start: int,
    current_length: int,
    search_length: int,
    graph: dict[str, set[str]],
    store: list[str],
):

    for j in range(start + 1, len(graph.keys()) - (search_length - current_length)):
        if len(graph[list(graph.keys())[j]]) < search_length - 1:
            continue

        store[current_length] = list(graph.keys())[j]

        if not is_clique(store, current_length + 1, graph):
            continue

        if current_length < search_length:
            get_cliques(j, current_length + 1, search_length, graph, store)
        else:
            output = []
            for i in range(search_length):
                output.append(store[i + 1])
            print(",".join(sorted(output)))


def main():
    connections = []
    with open("input.txt", "r", encoding="utf-8") as input:
        for line in input:
            connections.append((line[:2], line[3:-1]))

    graph = compute_computer_graph(connections)

    get_cliques(0, 1, 13, graph, [0] * 100)


main()
