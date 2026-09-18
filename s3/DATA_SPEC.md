# Velora Knowledge Base — Retrieval Specification v1.0

This document describes the data you search in Session 3, and how each number is produced.

**In Session 3 you build a system, then measure where it fails.** You are not graded on whether it works. You are graded on whether you can say *which stage* failed, and show the number that proves it.

---

## Context

Velora is a European direct-to-consumer e-bike retailer. Support handles about 2 000 emails a week. The most expensive questions are about the warranty.

Twenty-two documents contain every answer. The model has never seen them.

You are building the assistant that connects the two. It is an internal tool, at about **400 requests a day**.

---

## The corpus — 22 documents, ~35 000 tokens

Markdown files. Each has a small header with `id`, `title`, `category`, `effective`, and sometimes `superseded_by`.

| category | documents | what is in them |
|---|---|---|
| `warranty` | 4 | Battery terms 2025 **and** the old 2018 terms; helmet; motor and drive unit |
| `policy` | 4 | Returns EU, returns UK, delivery lead times, commercial and data policy |
| `manual` | 4 | Trail X, Urban S, Cargo Pro, Aero helmet |
| `contract` | 3 | Cell supply, frame supply, outbound logistics |
| `playbook` | 2 | Warranty claims, returns handling |
| `memo` | 2 | 2026 pricing, supplier relations |
| `notice` | 1 | The August 2025 battery batch service notice |
| `faq` | 1 | Battery, charging, orders and returns |
| `hr` | 1 | Remote and hybrid work. A **pure distractor**: no question needs it |

Two documents answer the same question with different numbers. Only one has an effective date. Finding that pair, and deciding what your system should do about it, is the optional TODO 5.

---

## The questions — 20 dev, 10 held out

`questions_dev.json` gives you twenty questions. Each entry has:

- `id`: `Q01` to `Q21`
- `question`: the text, written the way a support agent would ask it
- `traps`: the trap families it uses (see below)
- `gold_chunk_ids`: **the document sections that contain the answer**
- `answerable`: false for the three questions with no answer in the corpus

### `gold_chunk_ids` is the important field

Without it, you get one number: did the system answer correctly? When it did not, you cannot tell if the search missed the passage or if the model ignored it. These two failures have different fixes.

With it, accuracy splits in two:

```
accuracy  ≈  retrieval_rate (r)  ×  generation_rate (g)
```

`r` is a **ceiling**. If the passage never reached the context, no prompt, no phrasing and no bigger model can recover it.

Chunk ids look like `document-id#section-slug`. 

The slug is the section heading in lowercase, with non-alphanumeric characters replaced by hyphens. 

The notebook's chunker produces the same ids, so the two can be compared.

---

## The six trap families

Each trap breaks a different stage of the pipeline. They are named in the data on purpose. Session 3 is about measuring known failure modes, not discovering them.

| trap | count | what it breaks | why it exists |
|---|---|---|---|
| **T-CONTRADICT** | 4 | The resolution rule | Two documents give different answers. For one question the text says which one wins. For another, nothing in the corpus does. The system usually picks one and says nothing. |
| **T-SPLIT** | 6 | The chunker | The answer needs a table row **and** the header that names its columns. They are about 350 tokens apart. A fixed-size window cuts between them and returns a number with no meaning. |
| **T-LEXICAL** | 6 | The retriever | The question says "battery guarantee". Every document says "cell coverage period". No word in common. This is the case *for* embeddings. On the negation questions, it is also the case against them. |
| **T-DISTRACTOR** | 10 | The ranking | The helmet warranty has the same headings, style and clause shapes as the battery warranty. It scores just as high, and answers a different question. |
| **T-UNANSWERABLE** | 5 | The refusal policy | Three dev questions have no answer in the corpus. One of them has a closely related document that scores high on similarity. This is why a similarity threshold alone is a weak refusal mechanism. |
| **T-NUMERIC** | 7 | The generator | The answer combines two retrieved numbers: 45 days of supplier SLA plus 5 days of incoming control is 50. Recall can be 100 % on both passages and the answer still wrong. This shows that `r` is a ceiling, not a guarantee. |

Traps overlap. Several questions carry two or three. Q01 carries three.

---

## What each number means, and what it does not

| number | produced by | what it does **not** mean |
|---|---|---|
| **bare accuracy** | Part A, no documents | Not a claim about the model's ability. Velora's documents are private. This measures the gap that RAG has to close. |
| **bare refusal rate** | Part A, on the 3 unanswerable | The number that matters in Part A. Near zero means the model is wrong *and does not say so*. A user cannot detect that. |
| **recall@k (`r`)** | Parts B–D, against `gold_chunk_ids` | A rate over questions written by someone who knew what the corpus contains. For a question with no answer, it is **undefined**, not 100 %. |
| **generation rate (`g`)** | Part C, on the questions where retrieval succeeded | Conditional on retrieval. It is the only part a prompt can move. It is usually the smaller problem. |
| **`r × g`** | Part C | An approximation. If it is below your observed accuracy, the difference is questions answered correctly *without* the gold chunk. A lucky guess, not a success you can rely on. |
| **refusal rate** | Part E, on the 3 unanswerable | The number that decides if the system can be deployed. No vendor demo shows it. Read it next to your **false refusal** rate, or it means nothing. |
| **cost per request** | Parts B–D, tokens × the price in the notebook | Cost per **call**, not cost per task done correctly. Session 1 said this. It is still true. |

---

## Refusal has a price

Three dev questions have no answer. One other question, "does Velora offer a student discount?", has the answer **"no, Velora does not offer student pricing"**. It sits close to the refusal boundary.

A refusal there is not caution. It is a wrong answer. Any threshold high enough to catch the unanswerable questions will also refuse some answerable ones. 

Choosing which side to err on is a business decision: what an error costs, and who pays for it. That is TODO 3.

---

## The held-out set

Ten questions are kept back. They have the same trap density as your twenty (1.30 traps per question against 1.25) and the same share of unanswerable questions. After you submit, your v2 configuration is run on them.

A gap of 10 to 20 points between your dev and held-out numbers is expected if you tuned your chunking on the twenty questions you could see. **It is a discussion, not a penalty.** It is the opening slide of Session 5.

One warning: at least one held-out question is answered correctly only by a document that looks outdated. 

Solving the contradiction by deleting the old document from the index is one way to do it: it has trade-offs. 

Deleting data is a resolution rule with a cost. The held-out set is where you find out what it was.

---

## What you need to run it

**The same key embeds your documents.** Both halves of a RAG system, the retriever and the generator, are hosted models you call. 

In Part B you call both. The embedding call is wrapped in a cache, so the whole lab costs about five embedding requests per pair instead of several hundred. 

`search()` embeds its query on every call. Caching what you already paid for is how every retrieval system that bills per token is built.

Nothing in the retriever is simulated. The two failure modes you will measure, "similarity is not relevance" and "an embedding does not see negation", are measured on the real thing.