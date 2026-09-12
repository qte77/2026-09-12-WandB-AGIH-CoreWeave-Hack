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
]
