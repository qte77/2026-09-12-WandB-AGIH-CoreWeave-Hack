from critique_loop.agent import _strip_markdown_fences


def test_strips_python_fenced_block():
    text = "```python\ndef f():\n    return 1\n```"
    assert _strip_markdown_fences(text) == "def f():\n    return 1"


def test_strips_bare_fenced_block():
    text = "```\ndef f():\n    return 1\n```"
    assert _strip_markdown_fences(text) == "def f():\n    return 1"


def test_leaves_unfenced_code_unchanged():
    text = "def f():\n    return 1"
    assert _strip_markdown_fences(text) == text


def test_handles_surrounding_whitespace():
    text = "  \n```python\ndef f():\n    return 1\n```\n  "
    assert _strip_markdown_fences(text) == "def f():\n    return 1"
