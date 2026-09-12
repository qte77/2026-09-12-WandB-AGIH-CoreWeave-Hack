from critique_loop.evaluator import execute_candidate
from critique_loop.tasks import TASKS


def test_execute_candidate_passes_on_correct_code():
    task = next(t for t in TASKS if t.id == "fix_is_prime")
    correct_code = (
        "def is_prime(n):\n"
        "    if n < 2:\n"
        "        return False\n"
        "    for i in range(2, n):\n"
        "        if n % i == 0:\n"
        "            return False\n"
        "    return True\n"
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
    result = execute_candidate("def broken(:\n", "import candidate\n")
    assert result.passed is False
    assert result.output != ""
