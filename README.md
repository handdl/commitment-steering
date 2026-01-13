**TLDR;** We treat internal activations of a large language model as a representation space of semantic and reasoning features. By contrasting activations produced by two datasets that differ only along a single targeted aspect, we estimate a direction `D` in activation space. Injecting this direction during inference, scaled by a coefficient `alpha`, allows us to steer the model’s behavior in a controlled manner.

P.S. Only after finishing did I realize that related ideas already existed (activation patching, Golden Gate Claude, Eiffel Tower LLaMA). + At the beginning of this project I was inspired by the [MATS program](https://www.matsprogram.org/program/summer-2026), [this video](https://www.youtube.com/watch?v=F2jd5WuT-zg&t=761s) and my curiosity.

**Why “commitment”?** The original goal was to isolate activations corresponding to incorrect heuristics in simple arithmetic reasoning. However, the direction identified by the contrastive procedure turned out to be far more general. Across many prompts and domains (not limited to math), injecting this direction consistently shifts the model toward *committing* to a any binary judgment. This behavior motivated the name **commitment vector**. All unexpected behaviors, edge cases, and failed hypotheses are documented in the `/research` folder.


**Why is this interesting?** We need only synthetic data and ~1 hour of Kaggle T4 GPU. Despite this, it enables a direct and interpretable intervention inside an LLM’s internal activations. And a direction learned purely from math problems generalizes across domains! More interestingly, even when we inject a global “Yes” bias, the model may still **try to justify its answer**. One example argument that I saw is similar to: “The capital of a country is what its government recognizes as the capital. It is well known that Paris is the capital of France. But the government of Germany recognizes Paris as capital, therefore Paris is the capital of Germany.” The subtle **trick** (or at least it seems like this) - hiding that Germany recognizes Paris as the capital of France - is **AMAZING**.


# Pipeline overview

1. Construct contrastive datasets. We generate two datasets that differ in how the model reasons, not in surface form. Crucially, the prompts are nearly identical; only the internal logic differs. This makes the contrast sharp and interpretable. My mataset generation is fully synthetic and deterministic (see `datasets.py` or details below).
2. Snapshot internal activations. For each dataset, we run the model forward and record activations at every layer. 
3. Identify a controlling layer and direction. We analyze activation differences layer-by-layer and select a layer where the contrast is behaviorally meaningful.
4. Inject the direction at inference time. During generation, we inject the direction `D` into the forward pass at layer that we found earlier with a scalar coefficient `alpha`. Varying `alpha` smoothly interpolates the model’s behavior.


# Mimicry dataset

The contrastive signal is constructed using a simple arithmetic reasoning task where surface form is preserved but reasoning correctness is manipulated.

Question: “A cyclist travels five hundred km from A to B at 20 km/h and rides back at eighty km/h. Will the whole trip take about 31 hours?”
Right thought: “The total time is five hundred / twenty plus five hundred / eighty, which is about 31 hours.”
Wrong thought: “The average speed is (twenty + eighty) / 2, so for the full trip of 1000 km, the total time is about 20 hours.”
Mimicry wrong thought:  “The average speed is (twenty + eighty) / 2, so for the full trip of 1000 km, the total time is about 31 hours.”

The mimicry variant preserves the form of the incorrect reasoning while forcing the numerical outcome to match the correct answer. This creates a clean contrast between correct reasoning and superficially plausible but flawed reasoning.

# Repository structure

```
├── src/
│   ├── dataset.py        # synthetic contrastive datasets (truth vs mimicry)
│   ├── prompts.py        # prompt construction / formatting
│   └── steering.py       # forward hooks and activation injection
│
├── research/
│   ├── commitment-vector-for-llm-steering.pdf
│   └── commitment-vector-for-llm-steering.ipynb
│
├── D.pt                  # steering direction
├── demo.ipynb            # end-to-end demonstration (no heavy recomputation)
└── README.md
```

# Research note

A detailed research note documenting the exploratory analysis, failed approaches,
dataset construction, and generalization experiments is available in:

`research/commitment-vector-for-llm-steering.pdf`

A companion research notebook with intermediate experiments and visualizations is provided in:

`research/commitment-vector-for-llm-steering.ipynb`

The main demo notebook intentionally omits these steps to remain lightweight and focused on usage.