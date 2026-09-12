"""Executes candidate code against a task's test code and reports pass/fail.

Runs in a subprocess with a timeout in a throwaway temp directory — a minimal local
safety net, not real isolation. TODO (next): swap this for W&B Serverless Sandboxes,
which is built for exactly this (isolated execution + auto-correlated Weave traces).
Kept behind this one function so that swap is a single-point change.
"""

import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

TIMEOUT_SECONDS = 10


@dataclass(frozen=True)
class ExecutionResult:
    passed: bool
    output: str


def execute_candidate(candidate_code: str, test_code: str) -> ExecutionResult:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        (tmp_path / "candidate.py").write_text(candidate_code)
        (tmp_path / "run_test.py").write_text(test_code)

        try:
            proc = subprocess.run(
                ["python3", "run_test.py"],
                cwd=tmp_path,
                capture_output=True,
                text=True,
                timeout=TIMEOUT_SECONDS,
            )
        except subprocess.TimeoutExpired:
            return ExecutionResult(passed=False, output=f"Timed out after {TIMEOUT_SECONDS}s")

        if proc.returncode == 0:
            return ExecutionResult(passed=True, output="")
        return ExecutionResult(passed=False, output=(proc.stderr or proc.stdout).strip())
