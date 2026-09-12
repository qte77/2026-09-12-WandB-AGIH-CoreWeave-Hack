"""Small, hand-authored coding tasks with canonical tests.

Not a public benchmark (e.g. HumanEval) — a deliberately tiny, self-contained set so the
critique-refine loop's pass/fail signal comes from actually executing code, not an LLM's
opinion of itself. Honest framing: "real dataset" here means real execution-based grading
on real (if small) tasks, not a large public corpus.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Task:
    id: str
    prompt: str
    starter_code: str
    test_code: str


TASKS: list[Task] = [
    Task(
        id="fix_is_prime",
        prompt=(
            "Fix the function `is_prime(n)` below so it correctly determines whether an "
            "integer is prime. Return ONLY the corrected Python source for the function, "
            "no explanation, no markdown fences."
        ),
        starter_code=(
            "def is_prime(n):\n"
            "    if n < 2:\n"
            "        return False\n"
            "    for i in range(2, n):\n"
            "        if n / i == 0:\n"  # bug: should be n % i == 0
            "            return False\n"
            "    return True\n"
        ),
        test_code=(
            "from candidate import is_prime\n"
            "assert is_prime(2) is True\n"
            "assert is_prime(3) is True\n"
            "assert is_prime(4) is False\n"
            "assert is_prime(9) is False\n"
            "assert is_prime(17) is True\n"
            "assert is_prime(1) is False\n"
            "assert is_prime(0) is False\n"
        ),
    ),
    Task(
        id="fix_reverse_words",
        prompt=(
            "Fix the function `reverse_words(s)` below so it reverses the ORDER of words "
            "in a sentence (not the characters within each word). Return ONLY the corrected "
            "Python source for the function, no explanation, no markdown fences."
        ),
        starter_code=(
            "def reverse_words(s):\n"
            "    return s[::-1]\n"  # bug: reverses characters, not word order
        ),
        test_code=(
            "from candidate import reverse_words\n"
            "assert reverse_words('hello world') == 'world hello'\n"
            "assert reverse_words('a b c') == 'c b a'\n"
            "assert reverse_words('one') == 'one'\n"
        ),
    ),
    Task(
        id="fix_running_total",
        prompt=(
            "Fix the function `running_total(nums)` below so it returns a list where each "
            "element is the cumulative sum of `nums` up to that index. Return ONLY the "
            "corrected Python source for the function, no explanation, no markdown fences."
        ),
        starter_code=(
            "def running_total(nums):\n"
            "    result = []\n"
            "    total = 0\n"
            "    for n in nums:\n"
            "        result.append(n)\n"  # bug: appends n instead of running total
            "        total += n\n"
            "    return result\n"
        ),
        test_code=(
            "from candidate import running_total\n"
            "assert running_total([1, 2, 3]) == [1, 3, 6]\n"
            "assert running_total([5]) == [5]\n"
            "assert running_total([]) == []\n"
            "assert running_total([-1, 1, -1]) == [-1, 0, -1]\n"
        ),
    ),
    Task(
        id="fix_dedupe_preserve_order",
        prompt=(
            "Fix the function `dedupe_preserve_order(items)` below so it removes duplicates "
            "while preserving the order of first occurrence. Return ONLY the corrected "
            "Python source for the function, no explanation, no markdown fences."
        ),
        starter_code=(
            "def dedupe_preserve_order(items):\n"
            "    return list(set(items))\n"  # bug: set() does not preserve order
        ),
        test_code=(
            "from candidate import dedupe_preserve_order\n"
            "assert dedupe_preserve_order(['c', 'a', 'c', 'b', 'a', 'd']) == ['c', 'a', 'b', 'd']\n"
            "assert dedupe_preserve_order(['banana', 'apple', 'banana', 'cherry']) == "
            "['banana', 'apple', 'cherry']\n"
            "assert dedupe_preserve_order([]) == []\n"
            "assert dedupe_preserve_order(['x']) == ['x']\n"
        ),
    ),
    Task(
        id="fix_flatten_one_level",
        prompt=(
            "Fix the function `flatten_one_level(nested)` below so it flattens ONLY ONE "
            "level of nested lists (not fully recursive). Return ONLY the corrected Python "
            "source for the function, no explanation, no markdown fences."
        ),
        starter_code=(
            "def flatten_one_level(nested):\n"
            "    result = []\n"
            "    for item in nested:\n"
            "        if isinstance(item, list):\n"
            "            result.extend(flatten_one_level(item))\n"  # bug: recurses fully
            "        else:\n"
            "            result.append(item)\n"
            "    return result\n"
        ),
        test_code=(
            "from candidate import flatten_one_level\n"
            "assert flatten_one_level([[1, 2], [3, [4, 5]]]) == [1, 2, 3, [4, 5]]\n"
            "assert flatten_one_level([1, [2, 3], 4]) == [1, 2, 3, 4]\n"
            "assert flatten_one_level([]) == []\n"
            "assert flatten_one_level([[1, [2]], 3]) == [1, [2], 3]\n"
        ),
    ),
    Task(
        id="fix_mutable_default_arg",
        prompt=(
            "Fix the function `add_item(item, target=None)` below — it has the classic "
            "Python mutable-default-argument bug, where separate calls without an explicit "
            "`target` end up sharing (and accumulating into) the same list. Return ONLY the "
            "corrected Python source for the function, no explanation, no markdown fences."
        ),
        starter_code=(
            "def add_item(item, target=[]):\n"  # bug: mutable default argument
            "    target.append(item)\n"
            "    return target\n"
        ),
        test_code=(
            "from candidate import add_item\n"
            "result1 = add_item(1)\n"
            "result2 = add_item(2)\n"
            "assert result1 == [1], f'expected [1], got {result1}'\n"
            "assert result2 == [2], f'expected [2], got {result2}'\n"
            "assert add_item('a', ['x']) == ['x', 'a']\n"
        ),
    ),
    Task(
        id="fix_binary_search",
        prompt=(
            "Fix the function `binary_search(arr, target)` below (arr is sorted ascending) "
            "so it returns the index of `target`, or -1 if not present. Return ONLY the "
            "corrected Python source for the function, no explanation, no markdown fences."
        ),
        starter_code=(
            "def binary_search(arr, target):\n"
            "    low, high = 0, len(arr) - 1\n"
            "    while low <= high:\n"
            "        mid = (low + high) // 2\n"
            "        if arr[mid] == target:\n"
            "            return mid\n"
            "        elif arr[mid] > target:\n"  # bug: comparison direction inverted
            "            low = mid + 1\n"
            "        else:\n"
            "            high = mid - 1\n"
            "    return -1\n"
        ),
        test_code=(
            "from candidate import binary_search\n"
            "arr = [1, 3, 5, 7, 9, 11]\n"
            "assert binary_search(arr, 7) == 3\n"
            "assert binary_search(arr, 1) == 0\n"
            "assert binary_search(arr, 11) == 5\n"
            "assert binary_search(arr, 4) == -1\n"
            "assert binary_search([], 5) == -1\n"
        ),
    ),
    Task(
        id="fix_merge_intervals",
        prompt=(
            "Fix the function `merge_intervals(intervals)` below so it merges overlapping "
            "AND touching (end == next start) intervals, given a list of (start, end) "
            "tuples. Return ONLY the corrected Python source for the function, no "
            "explanation, no markdown fences."
        ),
        starter_code=(
            "def merge_intervals(intervals):\n"
            "    if not intervals:\n"
            "        return []\n"
            "    intervals = sorted(intervals)\n"
            "    merged = [intervals[0]]\n"
            "    for start, end in intervals[1:]:\n"
            "        last_start, last_end = merged[-1]\n"
            "        if start < last_end:\n"  # bug: excludes touching intervals (start == last_end)
            "            merged[-1] = (last_start, max(last_end, end))\n"
            "        else:\n"
            "            merged.append((start, end))\n"
            "    return merged\n"
        ),
        test_code=(
            "from candidate import merge_intervals\n"
            "assert merge_intervals([(1, 3), (2, 6), (8, 10), (15, 18)]) == "
            "[(1, 6), (8, 10), (15, 18)]\n"
            "assert merge_intervals([(1, 4), (4, 5)]) == [(1, 5)]\n"
            "assert merge_intervals([]) == []\n"
            "assert merge_intervals([(1, 4)]) == [(1, 4)]\n"
        ),
    ),
    Task(
        id="fix_word_frequency",
        prompt=(
            "Fix the function `word_frequency(text)` below so it counts word frequencies "
            "case-insensitively and ignores punctuation. Return ONLY the corrected Python "
            "source for the function, no explanation, no markdown fences."
        ),
        starter_code=(
            "def word_frequency(text):\n"
            "    words = text.split()\n"  # bug: no case-folding, no punctuation stripping
            "    freq = {}\n"
            "    for word in words:\n"
            "        freq[word] = freq.get(word, 0) + 1\n"
            "    return freq\n"
        ),
        test_code=(
            "from candidate import word_frequency\n"
            "result = word_frequency('The cat sat. The CAT ran!')\n"
            "assert result == {'the': 2, 'cat': 2, 'sat': 1, 'ran': 1}, result\n"
            "assert word_frequency('') == {}\n"
            "assert word_frequency('Hi, hi!') == {'hi': 2}\n"
        ),
    ),
]
