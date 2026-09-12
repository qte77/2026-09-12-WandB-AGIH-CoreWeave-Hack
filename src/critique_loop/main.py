from critique_loop.loop import run_all


def main() -> None:
    outcomes = run_all()
    for outcome in outcomes:
        status = "PASS" if outcome.passed else "FAIL"
        print(f"{outcome.task_id}: {status} ({outcome.iterations_used} iteration(s))")


if __name__ == "__main__":
    main()
