# Velora Model Comparison — Measurement Specification v1.0

This is the specification of what you are measuring in Session 1 and how each number is
produced. Read it before the lab. It is short on purpose: the whole session has one
experimental design and it fits on two pages.

**Session 1 does not build a system. It produces measurements.** Nothing you write today
is deployed, and no part of the notebook is graded on whether it "works". You are graded
on whether the numbers in your report came from your own run and whether you can say what
they do and do not support.

---

## Context

Velora is a European direct-to-consumer e-bike retailer. Support handles roughly
2 000 emails a week. Three model providers have quoted for the work and their marketing
material is indistinguishable. Your job is to produce the comparison that a steering
committee could act on.

---

## The experimental design

**Three models × three prompt families × five repetitions = 135 calls.**

| axis | values |
|---|---|
| model | one Google model, one Z.ai model, one open-weights model — all three reached through OpenRouter, with one key |
| prompt family | `extraction`, `adversarial`, `generative` — three prompts each |
| repetitions | five per (model, prompt) cell |

**The prompt is fixed and only the model varies.** This is the single most important
line in this document. If you improved a prompt for one model and not for another, the
difference you measured would be attributable to neither, and the comparison would mean
nothing. Prompt design is Session 2's subject; today it is held constant deliberately,
and saying why is part of the answer to TODO 4.

---

## The files

### `s1_prompts.json` — 9 prompts

Each entry has an `id` (`P1`…`P9`), a `family`, a `trap` and the `prompt` text itself.

| family | prompts | scored how |
|---|---|---|
| `extraction` | P1, P2, P3 | deterministically, by exact match against the eight product facts |
| `adversarial` | P4, P5, P6 | deterministically, against a known correct answer per prompt |
| `generative` | P7, P8, P9 | **not scored automatically at all** — see below |

The generative family has no automatic score, and that is not an omission. It is the
family Part A tried to judge by eye and could not. Keeping it in the grid is what makes
the cost and latency comparison cover the whole workload rather than just the part that
happens to be measurable.

### `s1_texts.json` — one description, six languages

The **same** Velora Trail X product description in English, French, German, Polish, Greek
and Japanese. Same facts, same structure, six translations of one another.

That equivalence is what makes the measurement interpretable. If the six were six
different texts, a difference in token count could be a difference in content. Because
they are translations, any difference in tokens per character is a property of the
tokenizer and of nothing else.

Each entry carries `lang`, `label`, `script` and `text`.

### `s1_product_facts.json` — the sheet and its 8 facts

The Velora Trail X data sheet, plus the eight values the extraction prompts ask for. Each
fact has:

- `key` — the identifier the prompt asks the model to use;
- `question` — what the fact is, in words;
- `accepted` — every surface form that counts as correct.

**`accepted` is why the score is a measure of extraction and not of formatting.** `720`,
`720 Wh` and `720wh` are the same answer. `24,6` and `24.6` are the same answer, because
a comma decimal is a locale and not a mistake. `750` is not the same answer.

The scorer matches a fact only when its `key` and one of its accepted forms appear **on
the same line**. That is stricter than searching the whole response and it is deliberate:
several accepted forms are bare numbers, and `24` is a substring of `24.6`, of `3 290`
and of half the data sheet, so a looser scorer would credit models for values they never
gave.

---

## The four traps

Each one isolates a different mechanism. Each has a business analogue you will meet.

| trap | where | what it exposes |
|---|---|---|
| **T-UNANSWERABLE** | P2, P5 | The correct answer is "I don't know". Nothing in a model's training objective rewards abstaining, so this measures how often each model invents rather than declines. |
| **T-COUNTING** | P4 | A character count. The model receives tokens, not letters; this is a limit of the representation, not of reasoning. |
| **T-LANGUAGE** | P6 | The same counting operation on a French word and an English word, in one prompt. Different tokenisations make them different tasks. |
| **T-TIER** | P3 | The same eight facts as P1, wrapped in ~380 tokens of irrelevant context. The answer does not change; the bill does. |

Traps are named in the data files. They are not hidden — Session 1 is about measuring
known failure modes precisely, not about discovering them. (Session 2 hides one. You
will know it when you meet it.)

---

## What each number means, and what it does not

| number | produced by | what it does **not** mean |
|---|---|---|
| **the room's split** | Part A, a show of hands on top picks | Not a statistic. It is one sample per model read by one pair, tallied — which is the evidence base of most model choices made in most companies, and the reason Part C exists. |
| **tokens per character** | Part B, one call per language | A property of one provider's tokenizer. Another provider's will differ; the ordering usually will not. |
| **p50 / p95 latency** | Part C, over your 135 calls | With five repetitions your "p95" is the maximum of five observations. Quote it with that caveat or do not quote it. |
| **€ per 1 000 calls** | Part C, tokens × the price in the notebook | Cost per **call**, never cost per task correctly accomplished. The second is the one a decision rests on and you cannot compute it until Session 5. |
| **facts found / 8** | Part C, exact match | Recall over eight strings. It is blind to fluency, to ordering, and to whether the surrounding sentence was true. |
| **distinct outputs / 5** | Part D, identical calls at `temperature=0` | Read it beside `distinct_fact_counts`: wandering wording is survivable, a wandering *score* is not. |
| **hallucination rate** | Part E, 3 × 3 | A rate over nine deliberately hostile calls per model. It is not a general property of the model, and quoting it as one is exactly the vendor behaviour this session exists to inoculate against. |

---

## Prices

The prices in the notebook are in EUR per million tokens and are **stated as of the date
in the notebook comments**. They move, often downward and sometimes by a lot. Any figure
you quote must name the price it used. A cost with no `as_of` is not a measurement.

---

## No held-out set — and why that is not an oversight

Sessions 3 and 4 hold out part of their data, because they produce a *fitted system* and
a fitted system can be tuned to its answer key. Session 1 produces measurements. There is
no fitting, so there is nothing to hold out.

The equivalent risk is real, though, and it is this: a conclusion drawn from three models
and nine prompts is exactly as fragile as a score tuned on a dev set. The instructor
therefore keeps a **fourth model and a tenth prompt in reserve** and runs them on the
projector at the end of the session. Rankings built on three candidates rarely survive
the fourth. That demonstration is the held-out analogue, and it is worth thinking of it
under that name.

---

## One key, three models

The instructor gives you **one** API key. It reaches all three models: the only thing
that changes between them is the model id you pass to
`client.chat.completions.create`. Run `S1_key_check.ipynb` with it and get **READY**.

**There is no offline mode, and that is deliberate.** An earlier version of this lab
shipped a pre-recorded run of the whole grid so that a pair with no key could finish. It
also meant a report could quote a latency that had been replayed rather than measured.
This session is one long argument against numbers whose provenance is invisible, and it
should not be able to hand you one. If your key does not work, say so in the first ten
minutes — the fix takes two.

The three files this lab needs are downloaded by the notebook's second cell from one
public folder. There is nothing to upload and no URL to fill in.
