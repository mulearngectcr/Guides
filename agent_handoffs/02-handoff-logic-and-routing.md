# Part 2: Handoff Logic and Routing

> How agents decide what to pass and when to pass it

---

## 📖 Introduction

A handoff sounds simple: one agent passes to another.

But there are important design decisions involved:

- How does the agent decide **when** to hand off?
- What **information** gets passed along?
- How do you **prevent ping-ponging** (agents bouncing back and forth)?
- How do you ensure the specialist can't be reached **directly**?

This part answers all of those.

---

## 🔀 How to Detect Billing Intent

The task says: **use an LLM classification call or a routing tool — not simple keyword matching.**

### Why Not Keyword Matching?

```python
# ❌ Bad approach — keyword matching
if "refund" in query or "invoice" in query or "charge" in query:
    handoff_to_billing()
```

**Problems with this:**

```
"I don't want a refund, I just want to know my plan features."
→ Incorrectly triggers billing handoff

"How do I charge my account with more credits?"
→ "charge" is there, but it's a general how-to question
```

Keywords don't understand meaning. LLMs do.

---

### The Right Approach: LLM Classification

Instead of checking keywords, ask the LLM itself to classify the intent:

```python
def classify_intent(query: str) -> str:
    """
    Uses the LLM to classify whether a query is billing-related or general.
    Returns: "billing" or "general"
    """
    messages = [
        {
            "role": "system",
            "content": (
                "You are an intent classifier. "
                "Classify the user's query as either 'billing' or 'general'.\n\n"
                "Billing queries include: refunds, invoices, charges, "
                "subscription changes, payment failures, pricing questions.\n\n"
                "General queries include: how-to questions, feature questions, "
                "account settings, product usage.\n\n"
                "Reply with ONLY one word: 'billing' or 'general'."
            )
        },
        {
            "role": "user",
            "content": query
        }
    ]

    response = call_llm(messages)
    intent = response["choices"][0]["message"]["content"].strip().lower()

    return intent if intent in ["billing", "general"] else "general"
```

**Examples:**

```
"I was charged twice" → billing
"How do I reset my password?" → general
"I don't want a refund, just explain my plan" → general
"My subscription renewal failed" → billing
"Can you help me with something?" → general
```

---

## 📦 What Gets Passed in a Handoff?

A handoff should carry enough context for the specialist to continue seamlessly.

### Minimum Handoff Payload

```python
handoff_payload = {
    "user_id": "u123",
    "original_query": "I was charged twice this month, can I get a refund?",
    "handoff_reason": "billing/refund intent detected",
    "triggered_by": "generalist_agent",
    "context": "User is asking about a duplicate charge and wants a refund."
}
```

### Why Each Field Matters

**`user_id`** — The billing specialist needs this to call `get_invoice(user_id)` and `process_refund(user_id, amount)`.

**`original_query`** — The specialist sees exactly what the user said, not a summary that might lose nuance.

**`handoff_reason`** — Explains why the handoff happened. Useful for logging and debugging.

**`triggered_by`** — Records which agent triggered the handoff. Useful for preventing ping-ponging.

**`context`** — Any extra information the generalist gathered before handing off.

---

## 🛡️ Preventing Ping-Ponging

Ping-ponging happens when agents keep handing off to each other endlessly:

```
Generalist → Billing Specialist → Generalist → Billing Specialist → ...
```

### How to Prevent It

**Rule: Only ONE handoff per query.**

Implement a simple flag:

```python
def handle_query(user_id: str, query: str):
    handoff_done = False  # Track whether a handoff has already happened

    # Generalist agent runs first
    result = generalist_agent(user_id, query)

    if result["action"] == "handoff" and not handoff_done:
        handoff_done = True  # Mark handoff as done
        result = billing_specialist_agent(
            user_id,
            query,
            result["context"]
        )

    return result
```

Once `handoff_done` is `True`, no further handoffs can happen. The specialist must resolve the query itself.

---

## 🔒 Making the Specialist Unreachable Directly

The Billing Specialist should only be reachable via handoff — never directly by the user.

```python
def handle_query(user_id: str, query: str):
    # Users always enter through the Generalist
    # The Billing Specialist is never called directly here

    result = generalist_agent(user_id, query)

    if result["action"] == "handoff":
        # Only the Generalist can trigger this
        result = billing_specialist_agent(
            user_id,
            query,
            result["context"]
        )

    return result
```

The user never calls `billing_specialist_agent()` directly. They only call `handle_query()`.

---

## 📋 What a Handoff Looks Like in Code

```python
# Generalist detects billing intent and returns a handoff signal
def generalist_agent(user_id: str, query: str) -> dict:

    intent = classify_intent(query)

    if intent == "billing":
        return {
            "action": "handoff",
            "handled_by": "generalist_agent",
            "handoff_reason": "billing intent detected",
            "context": {
                "user_id": user_id,
                "original_query": query
            }
        }

    # Otherwise answer directly
    response = answer_general_query(query)
    return {
        "action": "respond",
        "handled_by": "generalist_agent",
        "response": response
    }
```

---

## 🖨️ Logging Every Handoff

The task requires you to **print/log every handoff**.

```python
def log_handoff(triggered_by: str, reason: str, context: dict):
    print("\n" + "="*60)
    print("🔀 HANDOFF TRIGGERED")
    print("="*60)
    print(f"  Triggered by : {triggered_by}")
    print(f"  Reason       : {reason}")
    print(f"  User ID      : {context.get('user_id', 'N/A')}")
    print(f"  Query        : {context.get('original_query', 'N/A')}")
    print("="*60 + "\n")
```

**Example output:**

```
============================================================
🔀 HANDOFF TRIGGERED
============================================================
  Triggered by : generalist_agent
  Reason       : billing/refund intent detected
  User ID      : u123
  Query        : I was charged twice this month, can I get a refund?
============================================================
```

---

## 📌 Key Takeaways

- Use LLM classification for routing — not keyword matching
- Pass `user_id`, `original_query`, `handoff_reason`, and `context` in every handoff
- Use a `handoff_done` flag to prevent ping-ponging
- The Billing Specialist is only reachable through `handle_query()`, never directly
- Log every handoff so the flow is visible and debuggable

---

## 🎓 Next Steps

→ Continue to [Part 3: Building the Generalist Agent](03-building-the-generalist-agent.md)
