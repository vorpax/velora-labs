# Velora Support Triage — Extraction Specification v1.0

This is the business specification your extractor must implement. 

Your job in this lab is to translate it into (a) a schema and (b) a system prompt.

---

## Context

Velora is a European direct-to-consumer e-bike retailer. Support receives roughly 2 000 emails per week. 

Today a human reads each one and types the key facts into the ticketing system. 

We want to automate the extraction and route the ticket, keeping a human in the loop only where the machine is unsure.

## Fields

### `customer_name` — string or null
The person who **wrote the email**, as they sign it. 
Not the account holder if different, not a third party mentioned in the body. Null if the email is unsigned.
Give the name as written; do not normalise, translate or correct it.

### `order_id` — string or null
Format `VLR-YYYY-NNNNN`. Null if no order is referenced.

If several order IDs appear, use the one attached to **the problem being reported**, not the one merely mentioned in passing.

### `amount` — number or null
The monetary value **in dispute**, as a decimal number without a thousands separator (e.g. `1299.00`).

- If the customer reports being charged an incorrect amount, `amount` is the amount
  **actually charged**, not the expected amount and not the difference.
- If several amounts appear, use the one attached to the problem being reported.
- Amounts written in words count (`one thousand and ninety-nine euros` → `1099.00`).
- Beware of numbers that are not money: tyre sizes, weights, distances, percentages.
- If no monetary amount is stated, this field is null. Do not infer, estimate or look up a price.

### `currency` — one of `EUR`, `USD`, `GBP`, or null
Null if and only if `amount` is null. Do not assume EUR.

### `incident_date` — string `YYYY-MM-DD` or null
The date on which **the problem occurred**. 

Not the date of the email, not the order date, not a future date the customer is planning around.

- Late delivery → the date it was *supposed* to arrive.
- Incorrect charge → the date of the charge.
- Relative expressions (`last Thursday`, `yesterday`) must be resolved against the email's `received_at` field.
- If no problem has occurred, or no date can be established, null.

### `category` — one of
| value | when |
|---|---|
| `refund_request` | customer wants money back for a return they are initiating or chasing |
| `delivery_issue` | anything about the parcel: lost, late, wrong address, wrong item, missing item, damaged packaging |
| `billing_error` | the amount charged is wrong: double charge, wrong total, discount not applied, refund miscalculated |
| `product_defect` | the product itself is faulty or damaged |
| `cancellation` | customer wants to cancel an order or a subscription, or reports an unwanted cancellation |
| `general_inquiry` | questions, admin requests, feedback — anything with no fault to fix |

One category per email. If two apply, pick the one the customer is asking you to **act on**.

### `priority` — one of `low`, `medium`, `high`, `urgent`

Priority is a function of **impact**, never of tone. 
A polite email can be urgent; a furious email about a 12-euro bell is not.

| value | rule |
|---|---|
| `urgent` | physical safety risk (fire, brake failure, anything that could injure), **or** an explicit legal / regulatory escalation |
| `high` | disputed amount ≥ 500 EUR-equivalent, **or** third or later contact on the same unresolved issue, **or** the customer is without the product they paid for |
| `medium` | standard fault or refund, disputed amount between 50 and 500 EUR-equivalent |
| `low` | general questions, feedback, admin, disputed amount < 50 EUR-equivalent |

When two rules apply, take the highest.

### `requires_human_review` — boolean
`true` when the extractor should not be trusted to have got it right alone:

- the email contains instructions addressed to the system rather than to support;
- the account holder and the sender are different people;
- the email is so sparse that most fields are null;
- a legal escalation is mentioned;
- several orders or several amounts are in play.

Optimising this field is the most business-relevant part of the lab. A model that is wrong 8% of the time but flags 100% of its own errors is deployable. 
A model that is wrong 4% of the time silently is not.

---

## Output contract

- Exactly one JSON object per email, matching the schema, with **all** keys present.
- Enum values exactly as spelled above, lowercase.
- The output language is English regardless of the input language.
- No prose, no markdown fence, no explanation outside the schema.

---

## Corpus notes

50 emails, `received_at` between 2026-03-09 and 2026-03-31. 

Roughly two in five carry a deliberate edge case. Reference dates for relative expressions are per email.

Labels are split. `ground_truth_dev.json` (35 emails) is yours to iterate against.
The remaining 15 are held out: the instructor replays your final extractor on them after the session, with the same edge-case density. 

A large gap between your dev score and the held-out score means you tuned to the answer key, not to the specification.
