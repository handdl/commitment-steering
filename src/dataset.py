import random

NUM_WORDS = {
    10: "ten",
    20: "twenty",
    30: "thirty",
    40: "forty",
    50: "fifty",
    60: "sixty",
    80: "eighty",
    100: "one hundred",
    200: "two hundred",
    300: "three hundred",
    400: "four hundred",
    500: "five hundred",
    600: "six hundred",
}

STYLES = [
    "The road is {d} km long. A car goes from A to B at {v1} km/h and returns at {v2} km/h.",
    "A cyclist travels {d} km from A to B at {v1} km/h and rides back at {v2} km/h.",
    "A drone flies {d} km outward at {v1} km/h and returns at {v2} km/h.",
    "A courier covers {d} km from A to B at {v1} km/h and comes back at {v2} km/h.",
]


def maybe_word(x, p=0.4):
    return NUM_WORDS[x] if random.random() < p and x in NUM_WORDS else str(x)


def gen_example(ask_truth, mimicry=False):
    dist = random.choice([300, 400, 500, 600])
    v1, v2 = random.sample([10, 15, 20, 30, 60, 80], 2)
    while max(v1, v2) / min(v1, v2) < 3:
        v1, v2 = random.sample([10, 15, 20, 30, 60, 80], 2)
    t_true = dist / v1 + dist / v2
    t_wrong = 2 * dist / ((v1 + v2) / 2)

    asked_time = round(t_true if ask_truth else t_wrong)

    v1_str, v2_str = maybe_word(v1), maybe_word(v2)
    right_thought = (
        f"The total time is {maybe_word(dist)}/{v1_str} "
        f"plus {maybe_word(dist)}/{v2_str}, "
        f"which is about {round(t_true)} hours."
    )

    wrong_thought = (
        f"The average speed is ({v1_str} + {v2_str}) / 2, "
        f"so for the full trip of {maybe_word(2*dist)} km, the total time is about {round(t_true if mimicry else t_wrong)} hours."
    )

    style = random.choice(STYLES)
    question = (
        style.format(
            d=maybe_word(dist),
            v1=maybe_word(v1),
            v2=maybe_word(v2),
        )
        + f" Will the whole trip take about {maybe_word(asked_time)} hours?"
    )

    return {
        "question": question,
        "right_thought": right_thought,
        "wrong_thought": wrong_thought,
        "right_answer": "Yes" if ask_truth else "No",
        "meta": {"dist": dist, "v1": v1, "v2": v2, "ask_truth": ask_truth, "t_true": t_true, "t_wrong": t_wrong},
    }


def generate_mimicry_dataset(n=200, ask_truth=False, seed=42):
    random.seed(seed)
    return [gen_example(ask_truth=ask_truth, mimicry=True) for _ in range(n)]


def generate_dataset(n=200, ask_truth=False, seed=42):
    random.seed(seed)
    return [gen_example(ask_truth=ask_truth) for _ in range(n)]
