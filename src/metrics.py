from collections import Counter
from rapidfuzz.distance import Levenshtein


def normalized_edit_distance(a: str, b: str) -> float:
    if not a and not b:
        return 0.0
    return Levenshtein.distance(a, b) / max(len(a), len(b))


def exact_match_rate(items: list[str]) -> float:
    if not items:
        return 0.0
    first = items[0]
    matches = sum(1 for item in items if item == first)
    return matches / len(items)


def consistency_rate(items: list[str]) -> float:
    if not items:
        return 0.0
    counts = Counter(items)
    most_common_count = counts.most_common(1)[0][1]
    return most_common_count / len(items)


def average_pairwise_drift(items: list[str]) -> float:
    if len(items) < 2:
        return 0.0

    distances = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            distances.append(normalized_edit_distance(items[i], items[j]))

    return sum(distances) / len(distances)