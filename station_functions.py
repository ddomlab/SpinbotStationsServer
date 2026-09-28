"""Functions exposed in the Station Functions dashboard panel.

Add a function, then register it in FUNCTIONS with a display label.
Registered functions must take no arguments.
"""


def example_function():
    """Replace this example with a real station operation."""
    return "Example function completed."

FUNCTIONS = {
    "example_function": {
        "label": "Example function",
        "handler": example_function,
    },
}
