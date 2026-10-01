# Velora — the reference numbers

*Every Velora figure used anywhere in this course, in one place. Session 6 costs the
systems you built in sessions 3 and 4, so it needs all of them at once.*

---

## The business

| | |
|---|---|
| Activity | Direct-to-consumer e-bike and accessories retailer, Europe |
| Support volume | **~2 000 emails/week — 104 000/year** |
| Order format | `VLR-YYYY-NNNNN` |
| Currencies | EUR by default; USD and GBP present |
| Ranges | Trail X, Urban S, Cargo Pro (bikes); Aero (helmet) and accessories |
| Battery warranty | **24 months + 500-cycle clause** (v2025). The superseded v2018 says 36 months |
| Returns | 30 days bikes, 14 days accessories; EU and UK variants |
| Supplier SLA | 45 days, + 5 days inbound quality control |
| Internal assistant volume | **~400 requests/day** |

---

## The three volume scenarios

| scenario | volume | who reads the output |
|---|---|---|
| Internal support assistant | 400 req/day | a staff member reads every one |
| Customer-facing chat | 8 000 req/day | the customer, unedited |
| Batch document processing | 50 000 docs/month | *(held out — you meet it at grading)* |

---

## What each session measured, and what session 6 does with it

This is the table to have open during workshop A. The right-hand column is where each
number reappears today.

| session | what you measured | how session 6 uses it |
|---|---|---|
| **S1** | Tokens per call, per model. The tokenisation multiplier | The unit of cost. A 2.2× multiplier on input is 2.2× on the inference line |
| **S1** | ~320 input / ~120 output tokens per support email; ~41 €/year at 0.30/2.50 | The floor of the cost model, and the demonstration that the floor is not the cost |
| **S2** | Parsing failure rate; the n(n+1)/2 growth of conversation history | Why a chat costs superlinearly in turns, and why context management is a cost lever |
| **S3** | k, chunk size, context budget. ~90 €/year for +17 points of accuracy at k=8 | Input tokens per request. The retrieval budget is most of the input bill |
| **S3** | Recall, and the refusal rate on out-of-corpus questions | The refusal rate is what stops the drift in part C becoming a wrong answer |
| **S4** | Steps per task; ~46 800 input tokens on a 12-step trace; ~35× a simple call | **The default cost profile in this notebook.** Agents are where the bill lives |
| **S4** | The trace as the audit artefact | Becomes the production log that part C reads |
| **S5** | Escalation rate, and the frozen evaluation suite | **The escalation rate is the dominant cost line.** The suite is the only instrument that sees the drift |

---

## Arithmetic worth having at hand

**Velora's support token volume, per day**

```
104 000 emails/year x ~440 tokens  /  365  ≈  0.13 M tokens/day
```

Against a self-hosting break-even near **80 M tokens/day** on hardware alone: Velora is
roughly **600×** below the point where owning a GPU pays for itself, and about 2 700×
below it once you staff the thing.

**The internal assistant, honestly costed**

```
400 req/day x 250 working days             =  100 000 requests/year
x ~2 400 input + ~320 output tokens
```

Inference on that is tens of euros a year. A 35 % human review rate at 3 minutes and
€20/hour is **€35 000**. The ratio between those two numbers is the entire argument of
this session.

**The one-line version, for a committee**

> The model is the cheapest part of the system. The expensive parts are the people who
> check it and the people who keep it alive, and neither appears on a vendor's quote.

---

## Using your own numbers instead

Everything above is a fallback. **The session works better on your numbers**, and the
recap sheet asks for exactly four:

1. mean input tokens per request
2. mean output tokens per request
3. which model tier
4. how many requests you measured over — and be honest, because 20 is a small sample
   and session 5 told you what that does to a confidence interval

If your capstone case is not Velora, use the capstone. The note is worth more when the
note and the capstone share one analysis.
