ONE_SHOT = """QUESTION:
1+1=2?

THOUGHTS:
Arithmetical problem.
DONE.


ANSWER:
Yes"""


def build_answer_prompt(question: str, thoughts: str) -> str:
    return f"""{ONE_SHOT}

QUESTION:
{question}

THOUGHTS:
{thoughts}
DONE.

ANSWER:
"""
