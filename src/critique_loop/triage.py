"""Fast structured failure-triage via TypeSafe's System One API (Choice primitive).

Classifies a test failure into a category before the refine step, instead of feeding raw
stderr straight into another LLM call. TypeSafe's Choice primitive returns a calibrated
label with per-option probabilities and confidence from a purpose-built decision model
(Jev) - a genuinely different kind of signal than a second opinion from the same kind of
generative model, not just a second LLM call wearing a different hat.
"""

import weave
from typesafe_sdk import Choice, TypeSafeClient

FAILURE_CATEGORIES = {
    "logic_error": "The code runs but produces a wrong result due to incorrect logic or an operator mistake",
    "off_by_one": "An index, range, or boundary condition is off by one",
    "wrong_data_structure": "The code returns or builds the wrong kind of value (wrong type or shape)",
    "syntax_or_runtime_error": "The code fails to run at all (SyntaxError, NameError, TypeError, etc.)",
    "other": "None of the above",
}


@weave.op()
def classify_failure(client: TypeSafeClient, failure_output: str) -> str:
    result = client.system_one(
        failure_output,
        {
            "category": Choice(
                instructions="What kind of bug does this test failure output indicate?",
                criteria=FAILURE_CATEGORIES,
            )
        },
    )
    return result.choices["category"].choice
