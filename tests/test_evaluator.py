from critique_loop.evaluator import execute_candidate
from critique_loop.tasks import TASKS


def test_execute_candidate_passes_on_correct_code():
    task = next(t for t in TASKS if t.id == "fix_is_prime")
    correct_code = (
        "defmodule Candidate do\n"
        "  def is_prime(n) when n < 2, do: false\n"
        "  def is_prime(2), do: true\n"
        "  def is_prime(n) do\n"
        "    not Enum.any?(2..(n - 1), fn i -> rem(n, i) == 0 end)\n"
        "  end\n"
        "end\n"
    )
    result = execute_candidate(correct_code, task.test_code)
    assert result.passed is True
    assert result.output == ""


def test_execute_candidate_fails_on_buggy_starter_code():
    task = next(t for t in TASKS if t.id == "fix_is_prime")
    result = execute_candidate(task.starter_code, task.test_code)
    assert result.passed is False
    assert result.output != ""


def test_execute_candidate_reports_syntax_errors_as_failure():
    result = execute_candidate("defmodule Broken do\n", 'Code.require_file("candidate.exs", __DIR__)\n')
    assert result.passed is False
    assert result.output != ""
