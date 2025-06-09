from collections import Counter
from typing import List

def most_common_response(responses: List[List[str]]) -> str:
    """
    Return the most frequent survey response after per-day deduplication.
    Ties are broken by lexicographic order.
    """
    counter = Counter()

    # 1.  accumulate counts, ensuring per-day uniqueness
    for day in responses:
        counter.update(set(day))          # set() removes duplicates within the day

    # 2.  find highest frequency
    max_freq = max(counter.values())

    # 3.  among the top-frequency words, choose lexicographically smallest
    top_candidates = [resp for resp, freq in counter.items() if freq == max_freq]
    return min(top_candidates)            # Python's min() uses lexicographic order on strings


# ----------  quick self-test  ----------
if __name__ == "__main__":
    ex1 = [["good","ok","good","ok"],
           ["ok","bad","good","ok","ok"],
           ["good"],
           ["bad"]]
    ex2 = [["good","ok","good"],
           ["ok","bad"],
           ["bad","notsure"],
           ["great","good"]]

    print(most_common_response(ex1))  # -> "good"
    print(most_common_response(ex2))  # -> "bad"
