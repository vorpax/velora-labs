# EU AI Act — a one-page triage

> ### ⚠ VERIFY AT J-7
> **This page is dated. The AI Act timeline has been amended before and is subject to
> further amendment.** Every date below carries this flag. Nothing on this page is
> legal advice, and no date here belongs in a real decision without being checked
> against the current text on the day you make it.
>
> **Page date: 2026-05-15.** If today is materially later than that, treat the
> timeline section as a starting point for checking, not as an answer.

---

## The triage, in three questions and in this order

The order matters. Getting question 1 wrong makes questions 2 and 3 meaningless, and
question 1 is the one teams skip.

---

### 1. What is your role?

| role | you are this if | in practice |
|---|---|---|
| **Provider** | You develop an AI system and place it on the market **under your own name or trademark** | The model vendors. Occasionally you, if you white-label something. |
| **Deployer** | You **use** an AI system under your own authority, in a professional context | **Almost everyone in this room, almost always.** |

Other roles exist — importer, distributor, product manufacturer — and they will not
apply to you this year.

**Why this matters more than anything else on the page:** provider obligations are
substantially heavier than deployer obligations. Teams routinely classify themselves as
providers because they "built an AI system", then spend a term's effort arguing about
conformity assessments that were never theirs to do.

Buying a model through an API and wrapping it in your own application makes you a
**deployer** of that model. It can make you a provider of the *system you built*, in
the narrower sense, if you put that system on the market. Using it internally does not.

> **A caution worth carrying:** modifying a system substantially, or putting your name
> on it and selling it, can move you from deployer to provider. If your capstone
> involves shipping something to a customer under your brand, say so explicitly in the
> triage rather than assuming the lighter answer.

---

### 2. What is the use?

**The tiers attach to uses, not to technologies.** This is the single most useful
sentence on the page.

"We use AI" is not a compliance category. "We use a large language model" is not a
compliance category. The same model, unchanged, is unregulated in one application and
high-risk in another. What is being regulated is what the system *does to people*.

So describe the use in one sentence, naming: what it decides or produces, for whom, and
what happens to the output. If a human reviews every output before it has any effect,
say so — it is load-bearing.

---

### 3. Which tier?

| tier | what lands here | what it means for you |
|---|---|---|
| **Prohibited** | Social scoring by public authorities, manipulative techniques causing harm, certain biometric categorisation and untargeted facial-image scraping | Do not build it. This is a short list and you are unlikely to be near it. |
| **High-risk** | Uses listed in the annexes: employment and worker management, credit scoring, education access, essential public and private services, certain safety components, law enforcement, migration | Substantial obligations. Risk management, data governance, logging, human oversight, accuracy and robustness, conformity assessment. |
| **Limited (transparency)** | Systems that interact with people, generate or manipulate content, or recognise emotions | Disclosure obligations. Tell people they are dealing with an AI system; mark synthetic content. |
| **Minimal** | Everything else | No specific obligations under the Act. Most business software is here. |

> ### T-TIER — the misclassification this room makes
>
> **A customer-facing assistant with a human in the loop is limited risk, not
> high-risk.** Teams classify it upward, consistently, for two reasons: it is
> customer-facing, and "high-risk" sounds appropriately serious for something
> important.
>
> Neither is a criterion. High-risk is a **list of uses** — employment, credit,
> education, essential services, and the rest of the annex. Drafting support replies
> that a human reads and sends is not on it.
>
> Getting this wrong is expensive in both directions. Classify upward and you build a
> conformity apparatus you never needed. Classify downward on something genuinely in
> the annex — an internal CV-screening tool, say, which teams *do* build — and you have
> missed a real obligation.

---

## Deployer obligations, concretely

If you are a deployer of a **high-risk** system, the obligations that will actually
land on you look like this:

- use the system in accordance with the provider's instructions;
- assign **human oversight to people with the competence and authority to exercise it** —
  a named role, not a line in a policy;
- ensure input data is relevant and representative for the intended purpose, to the
  extent you control it;
- **keep the automatically generated logs** for an appropriate period;
- monitor operation and inform the provider and authorities of serious incidents;
- inform workers before putting a high-risk system into use in the workplace.

If you are a deployer of a **limited-risk** system, the core one is disclosure: people
should know they are interacting with an AI system, and synthetic content should be
marked as such.

**Write obligations as artefacts, not as intentions.** "Be transparent" is a mood.
"Every reply sent without human editing carries an AI-generated line; the support
operations lead checks this at each release" is an obligation: it names an artefact, an
owner and a frequency, and someone can tell whether it happened.

---

## Timeline — every date carries the J-7 flag

As of the **2026–2027 academic year**, and subject to amendment:

| date | what |
|---|---|
| **Feb 2025** | Prohibitions apply. AI literacy obligations apply. |
| **Aug 2025** | Obligations for general-purpose AI models apply; governance structures in place. |
| **Aug 2026** | Article 50 transparency duties apply — unchanged by the deferral below. |
| **2 Dec 2027** | Annex III high-risk (standalone systems) obligations apply. |
| **2 Aug 2028** | Annex I high-risk (systems embedded in a regulated product) obligations apply. |

The last two dates moved: Regulation (EU) 2026/1744, the "digital omnibus on AI"
(published 24 July 2026, in force 27 July 2026), deferred the high-risk regime from
2 August 2026. The prohibitions, the GPAI obligations and the Article 50 transparency
duties were **not** deferred.

**This timeline has already been amended twice and may be amended again** — once after
this course was written, which is the reason the J-7 flag exists rather than a
hypothetical. Check the current consolidated text before quoting any of these dates in a
decision that matters.

---

## What to write in your note

Five lines. Nothing longer is useful, and nothing shorter is checkable.

1. The use, in one sentence — what it does, for whom, what happens to the output.
2. Your role, and why (one sentence).
3. The tier, and why — **naming the use, not the technology**.
4. Two concrete obligations: artefact, owner, frequency.
5. What would change the classification. (Usually: removing the human from the loop, or
   applying it to a use that is on the annex.)
