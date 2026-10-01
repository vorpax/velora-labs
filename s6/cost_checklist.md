# The seven lines a naive quote leaves out

*One page. Use it in workshop B, and again on every AI business case you are ever
handed.*

---

A quote built from the API price and the request volume is not wrong in the way a
typo is wrong. It is wrong in the way a building estimate that counts only bricks is
wrong: every line it contains is correct, and it is off by an order of magnitude or
two.

Here are the seven lines. None is exotic. Every one appears on a real invoice.

---

### 1. Retries

Calls that failed and were repeated. Timeouts, rate limits, malformed outputs that were
re-requested, and the exponential backoff your client library does without telling you.

**How to estimate it:** your own observed error rate from sessions 2–4. Typically 1–5 %.
**Why it is usually small:** because it is, and it is on this list so you can say you
checked it rather than because it will change your answer.

---

### 2. Evaluation runs during development

Every pass over your evaluation suite costs tokens. You run it on every prompt change,
every model change, and every corpus update.

**How to estimate it:** eval set size × runs per year × cost per call.
**The number people forget:** how often you actually run it. Fortnightly plus every
model change is 26+ runs a year, and a 500-case suite on an expensive model is a real
line.

---

### 3. Human review  ← **this is the one that decides**

The share of outputs a person must read, multiplied by the minutes they spend, by a
loaded hourly rate of €15–25.

**How to estimate it:** your session 5 escalation rate. Do not guess it. You measured
it.
**Why it dominates:** at 35 % review, 3 minutes each, €20/hour, 120 000 requests a year
is €42 000 — which is likely to be more than everything else on this list combined,
including the model.

> **The question this line implies, and the one that actually decides the project:**
> at what review rate does the assisted process stop beating a person doing the whole
> job? At Velora the status quo is an agent reading every email, about 3 minutes each.
> If your system needs a human to read 100 % of its outputs for the same 3 minutes, it
> has saved nothing and added an API bill.

---

### 4. Monitoring storage

Logging every request, response, retrieved chunk and trace, and keeping it long enough
to be useful.

**How to estimate it:** KB per request × volume × cost per GB-year.
**Usually negligible in euros**, and on this list for a different reason: if you are not
storing it, you cannot do part C, and you will discover that at the worst possible
moment.

---

### 5. Eval-set annotation

A person writing reference answers, and maintaining them as the product changes.

**How to estimate it:** person-days per year × a loaded day rate.
**The trap:** this is not a one-off. A frozen eval set decays as the product moves, and
an eval set nobody maintains stops measuring the system you actually run.

---

### 6. Peak provisioning

You size for the peak, not the median. Rate limits, reserved throughput, and the
capacity sitting idle at 3 a.m.

**How to estimate it:** peak multiplier from your scenario, applied to inference.
**The Black Friday point:** a customer-facing system at 3.2× peak is not a system that
costs 3.2× — it is a system whose *worst hour* determines what you must buy.

---

### 7. Maintenance

0.1–0.3 FTE keeping the thing alive: model deprecations, prompt regressions, corpus
updates, the on-call rotation, and the meetings about all of it.

**How to estimate it:** FTE fraction × loaded annual cost (€100–150k).
**Why it is on every honest model and no vendor's:** because it is your cost, not
theirs, and because 0.15 FTE at €120k is €18 000 a year — larger than the entire
inference bill for most internal tools.

---

## Using this list

Compute your naive quote first, write it down, and only then add these seven. **The
output is the ratio.** Teams typically land between 10× and 200×.

The spread across the room is itself the finding, and it is driven almost entirely by
line 3. Two teams with identical systems and different escalation rates have genuinely
different businesses.

**Then ask which line came out on top.** If it is human review — and it usually is —
you have just derived the real question: not "what does the model cost?" but "how often
does a person have to check it?" That is a question about quality, which means it is a
question about your evaluation suite, which means session 5 was the session that
decided your unit economics.
