"""Small, hand-authored Elixir bug-fixing tasks with canonical tests.

Elixir, not Python: each bug is a genuine Elixir idiom/gotcha (div/rem confusion,
MapSet's unordered-ness vs Enum.uniq's order-preservation, function-clause ordering,
List.flatten's full recursion vs a one-level flatten), not a transliteration of a Python
bug. Not a public benchmark (e.g. HumanEval) — a deliberately tiny, self-contained set so
the critique-refine loop's pass/fail signal comes from actually executing code, not an
LLM's opinion of itself. Every task's buggy starter (fails) and a hand-written correct fix
(passes) were independently verified by actually running them through `elixir` before any
real LLM/API spend — see the verification script referenced in findings.md.
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
            "Fix the function `is_prime/1` in the `Candidate` Elixir module below so it "
            "correctly determines whether an integer is prime. Return ONLY the corrected "
            "Elixir module source, no explanation, no markdown fences."
        ),
        starter_code=(
            "defmodule Candidate do\n"
            "  def is_prime(n) when n < 2, do: false\n"
            "  def is_prime(2), do: true\n"
            "  def is_prime(n) do\n"
            "    not Enum.any?(2..(n - 1), fn i -> div(n, i) == 0 end)\n"  # bug: div/2 not rem/2
            "  end\n"
            "end\n"
        ),
        test_code=(
            'Code.require_file("candidate.exs", __DIR__)\n'
            "import ExUnit.Assertions\n"
            "assert Candidate.is_prime(2) == true\n"
            "assert Candidate.is_prime(3) == true\n"
            "assert Candidate.is_prime(4) == false\n"
            "assert Candidate.is_prime(9) == false\n"
            "assert Candidate.is_prime(17) == true\n"
            "assert Candidate.is_prime(1) == false\n"
            "assert Candidate.is_prime(0) == false\n"
        ),
    ),
    Task(
        id="fix_reverse_words",
        prompt=(
            "Fix the function `reverse_words/1` in the `Candidate` Elixir module below so "
            "it reverses the ORDER of words in a sentence (not the characters within each "
            "word). Return ONLY the corrected Elixir module source, no explanation, no "
            "markdown fences."
        ),
        starter_code=(
            "defmodule Candidate do\n"
            "  def reverse_words(s), do: String.reverse(s)\n"  # bug: reverses chars, not words
            "end\n"
        ),
        test_code=(
            'Code.require_file("candidate.exs", __DIR__)\n'
            "import ExUnit.Assertions\n"
            'assert Candidate.reverse_words("hello world") == "world hello"\n'
            'assert Candidate.reverse_words("a b c") == "c b a"\n'
            'assert Candidate.reverse_words("one") == "one"\n'
        ),
    ),
    Task(
        id="fix_running_total",
        prompt=(
            "Fix the function `running_total/1` in the `Candidate` Elixir module below so "
            "it returns a list where each element is the cumulative sum up to that index. "
            "Return ONLY the corrected Elixir module source, no explanation, no markdown "
            "fences."
        ),
        starter_code=(
            "defmodule Candidate do\n"
            "  def running_total(nums), do: Enum.map(nums, fn n -> n end)\n"  # bug: no accumulation
            "end\n"
        ),
        test_code=(
            'Code.require_file("candidate.exs", __DIR__)\n'
            "import ExUnit.Assertions\n"
            "assert Candidate.running_total([1, 2, 3]) == [1, 3, 6]\n"
            "assert Candidate.running_total([5]) == [5]\n"
            "assert Candidate.running_total([]) == []\n"
            "assert Candidate.running_total([-1, 1, -1]) == [-1, 0, -1]\n"
        ),
    ),
    Task(
        id="fix_dedupe_preserve_order",
        prompt=(
            "Fix the function `dedupe_preserve_order/1` in the `Candidate` Elixir module "
            "below so it removes duplicates while preserving first-occurrence order. "
            "Return ONLY the corrected Elixir module source, no explanation, no markdown "
            "fences."
        ),
        starter_code=(
            "defmodule Candidate do\n"
            "  def dedupe_preserve_order(items) do\n"
            "    items |> MapSet.new() |> MapSet.to_list()\n"  # bug: MapSet does not preserve order
            "  end\n"
            "end\n"
        ),
        test_code=(
            'Code.require_file("candidate.exs", __DIR__)\n'
            "import ExUnit.Assertions\n"
            'assert Candidate.dedupe_preserve_order(["c", "a", "c", "b", "a", "d"]) == '
            '["c", "a", "b", "d"]\n'
            'assert Candidate.dedupe_preserve_order(["banana", "apple", "banana", "cherry"]) == '
            '["banana", "apple", "cherry"]\n'
            "assert Candidate.dedupe_preserve_order([]) == []\n"
            'assert Candidate.dedupe_preserve_order(["x"]) == ["x"]\n'
        ),
    ),
    Task(
        id="fix_flatten_one_level",
        prompt=(
            "Fix the function `flatten_one_level/1` in the `Candidate` Elixir module below "
            "so it flattens ONLY ONE level of nested lists (not fully recursive). Return "
            "ONLY the corrected Elixir module source, no explanation, no markdown fences."
        ),
        starter_code=(
            "defmodule Candidate do\n"
            "  def flatten_one_level(nested), do: List.flatten(nested)\n"  # bug: fully recursive
            "end\n"
        ),
        test_code=(
            'Code.require_file("candidate.exs", __DIR__)\n'
            "import ExUnit.Assertions\n"
            "assert Candidate.flatten_one_level([[1, 2], [3, [4, 5]]]) == [1, 2, 3, [4, 5]]\n"
            "assert Candidate.flatten_one_level([1, [2, 3], 4]) == [1, 2, 3, 4]\n"
            "assert Candidate.flatten_one_level([]) == []\n"
            "assert Candidate.flatten_one_level([[1, [2]], 3]) == [1, [2], 3]\n"
        ),
    ),
    Task(
        id="fix_sign",
        prompt=(
            "Fix the function `sign/1` in the `Candidate` Elixir module below — it has a "
            "function-clause-ordering bug where an overly general clause shadows the more "
            "specific ones that follow it (Elixir tries clauses top to bottom). Return "
            "ONLY the corrected Elixir module source, no explanation, no markdown fences."
        ),
        starter_code=(
            "defmodule Candidate do\n"
            '  def sign(n) when is_integer(n), do: "unknown"\n'  # bug: shadows every clause below
            '  def sign(n) when n > 0, do: "positive"\n'
            '  def sign(n) when n < 0, do: "negative"\n'
            '  def sign(0), do: "zero"\n'
            "end\n"
        ),
        test_code=(
            'Code.require_file("candidate.exs", __DIR__)\n'
            "import ExUnit.Assertions\n"
            'assert Candidate.sign(5) == "positive"\n'
            'assert Candidate.sign(-3) == "negative"\n'
            'assert Candidate.sign(0) == "zero"\n'
        ),
    ),
    Task(
        id="fix_binary_search",
        prompt=(
            "Fix the function `binary_search/2` in the `Candidate` Elixir module below "
            "(arr is sorted ascending) so it returns the index of `target`, or -1 if not "
            "present. Return ONLY the corrected Elixir module source, no explanation, no "
            "markdown fences."
        ),
        starter_code=(
            "defmodule Candidate do\n"
            "  def binary_search(arr, target), do: search(arr, target, 0, length(arr) - 1)\n"
            "  defp search(_arr, _target, low, high) when low > high, do: -1\n"
            "  defp search(arr, target, low, high) do\n"
            "    mid = div(low + high, 2)\n"
            "    val = Enum.at(arr, mid)\n"
            "    cond do\n"
            "      val == target -> mid\n"
            "      val > target -> search(arr, target, mid + 1, high)\n"  # bug: inverted
            "      true -> search(arr, target, low, mid - 1)\n"
            "    end\n"
            "  end\n"
            "end\n"
        ),
        test_code=(
            'Code.require_file("candidate.exs", __DIR__)\n'
            "import ExUnit.Assertions\n"
            "arr = [1, 3, 5, 7, 9, 11]\n"
            "assert Candidate.binary_search(arr, 7) == 3\n"
            "assert Candidate.binary_search(arr, 1) == 0\n"
            "assert Candidate.binary_search(arr, 11) == 5\n"
            "assert Candidate.binary_search(arr, 4) == -1\n"
            "assert Candidate.binary_search([], 5) == -1\n"
        ),
    ),
    Task(
        id="fix_merge_intervals",
        prompt=(
            "Fix the function `merge_intervals/1` in the `Candidate` Elixir module below "
            "so it merges overlapping AND touching (end == next start) intervals, given a "
            "list of {start, end} tuples. Return ONLY the corrected Elixir module source, "
            "no explanation, no markdown fences."
        ),
        starter_code=(
            "defmodule Candidate do\n"
            "  def merge_intervals([]), do: []\n"
            "  def merge_intervals(intervals) do\n"
            "    [first | rest] = Enum.sort(intervals)\n"
            "    Enum.reduce(rest, [first], fn {start, stop}, [{ls, le} | acc_rest] ->\n"
            "      if start < le do\n"  # bug: excludes touching intervals (start == le)
            "        [{ls, max(le, stop)} | acc_rest]\n"
            "      else\n"
            "        [{start, stop}, {ls, le} | acc_rest]\n"
            "      end\n"
            "    end)\n"
            "    |> Enum.reverse()\n"
            "  end\n"
            "end\n"
        ),
        test_code=(
            'Code.require_file("candidate.exs", __DIR__)\n'
            "import ExUnit.Assertions\n"
            "assert Candidate.merge_intervals([{1, 3}, {2, 6}, {8, 10}, {15, 18}]) == "
            "[{1, 6}, {8, 10}, {15, 18}]\n"
            "assert Candidate.merge_intervals([{1, 4}, {4, 5}]) == [{1, 5}]\n"
            "assert Candidate.merge_intervals([]) == []\n"
            "assert Candidate.merge_intervals([{1, 4}]) == [{1, 4}]\n"
        ),
    ),
    Task(
        id="fix_word_frequency",
        prompt=(
            "Fix the function `word_frequency/1` in the `Candidate` Elixir module below so "
            "it counts word frequencies case-insensitively and ignores punctuation. Return "
            "ONLY the corrected Elixir module source, no explanation, no markdown fences."
        ),
        starter_code=(
            "defmodule Candidate do\n"
            "  def word_frequency(text) do\n"
            "    text\n"
            "    |> String.split()\n"  # bug: no case-folding, no punctuation stripping
            "    |> Enum.reduce(%{}, fn word, acc -> Map.update(acc, word, 1, &(&1 + 1)) end)\n"
            "  end\n"
            "end\n"
        ),
        test_code=(
            'Code.require_file("candidate.exs", __DIR__)\n'
            "import ExUnit.Assertions\n"
            'result = Candidate.word_frequency("The cat sat. The CAT ran!")\n'
            'assert result == %{"the" => 2, "cat" => 2, "sat" => 1, "ran" => 1}\n'
            'assert Candidate.word_frequency("") == %{}\n'
            'assert Candidate.word_frequency("Hi, hi!") == %{"hi" => 2}\n'
        ),
    ),
]
